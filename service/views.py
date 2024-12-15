from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service.serializers import ServiceSerializer, HyphenatedAdjectivesSerializer, FeedbackSerializer
from service.models import Service, MultipleSpellings, HyphenatedAdjectives
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent
from accounts.models import InstituteProfile, StudentProfile
from accounts.serializers import StudentProfileSerializer
from file.serializers import FileSerializer
import difflib
from difflib import SequenceMatcher, unified_diff, get_close_matches, HtmlDiff, ndiff
import re
from spellchecker import SpellChecker
import string
from termcolor import colored
from django.http import JsonResponse
from openai import OpenAI
from difflib import SequenceMatcher, Differ
from django.shortcuts import get_object_or_404


class FeedbackView(APIView):
    permission_classes = [IsStudent]
    serializer_class = FeedbackSerializer
    def post(self, *args, **kwargs):
        data = self.request.data
        student = StudentProfile.objects.get(user=self.request.user)
        data["user"] = student.id
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class Services(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get(self, *args, **kwargs):
        try:
            user = self.request.user
            if user.user_type == "student":
                student = StudentProfile.objects.get(user=user)
            else:
                student = StudentProfile.objects.get(id=203)

            service = Service.objects.filter(user=student)
            serializer = self.serializer_class(service, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Service not found or something went wrong, try again",status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):
        data = self.request.data.copy()
        user = self.request.user
        if user.user_type == "student":
            student = StudentProfile.objects.get(user=user)
        else:
            student = StudentProfile.objects.get(id=203)

        data["user"] = student.id
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class ServicesItem(APIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            service = Service.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(service)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("service not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)






class ServicesCorrectionAI(APIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        service = Service.objects.get(id=self.kwargs["id"])

        student_text = service.text
        original_text = service.file.script

        characters_to_remove = ",!#$%@*.?/:"
        service_file_script = re.sub(f"[{re.escape(characters_to_remove)}]", "", service.file.script.replace('.', '. '))
        service_text = re.sub(f"[{re.escape(characters_to_remove)}]", "", service.text.replace('.', '. '))

        assistant = "As a marker, compare and contrast student_text and original_text based on the following commands: \n " \
                    "1. Indicate any missing words from the original_text in red html color compared to the student_text. \n " \
                    "2. Indicate any extra words in the student_text that are not in the original_text in green html color. \n " \
                    "3. Strike through misspelled words and write the correct form in brackets next to them. \n  " \
                    "4. Show any missing punctuation in the student_text compared to the original_text. \n " \
                    "Highlight the comparison of the student_text and the original_text with different colors and show the output as HTML."

        try:
            client = OpenAI(api_key="token")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"student_text:{service_text} \n original_text:{service_file_script}"},
                    {"role": "system", "content": assistant},
                ],
                max_tokens=150,  # Adjust as needed
                stop=None,
                temperature=0.7)
            # final_response = response.choices[0].message['content']
            response_dict = response.model_dump()
            message_content = response_dict['choices'][0]['message']['content']
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(message_content, status=status.HTTP_200_OK)




class ServicesCorrection(APIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        try:
            service = Service.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(service)

            characters_to_remove = ",!#$%@*.?/:"
            service_file_script = re.sub(f"[{re.escape(characters_to_remove)}]", "", service.file.script.replace('.', '. '))
            service_text = re.sub(f"[{re.escape(characters_to_remove)}]", "", service.text.replace('.', '. '))

            multiple_spellings = MultipleSpellings.objects.all()
            multiple_spellings_list = {}
            for item in multiple_spellings:
                multiple_spellings_list[item.US] = [item.US, item.UK]

            hyphenated_adjectives_list = HyphenatedAdjectives.objects.values_list('US', flat=True)

            def compare_texts(original, revised):

                seq_match = SequenceMatcher(None, original, revised)
                ratio = seq_match.ratio()
                similarity_percentage = ratio*100

                original_words = original.split()
                revised_words = revised.split()

                differ = difflib.Differ()
                diff = list(differ.compare(original_words, revised_words))

                spell = SpellChecker()
                missing_word = None  # Initialize missing_word with a default value
                missing_words = []
                misspelled_words = []
                misspelled_words_correct = []
                new_words = []
                highlight = " "

                for line in diff:
                    if line.startswith('- '):
                        missing_word = line[2:]
                        missing_words.append(missing_word.strip())
                        highlight += f"<span style='color:#dc0202e6'> <b>{missing_word.strip()}</b> </span> "

                    elif line.startswith('+ '):
                        new_word = line[2:]
                        if new_word.strip() not in spell:
                        #if spell.unknown(new_word.strip()):
                            misspelled_words.append(new_word.strip())
                            if missing_word:
                                misspelled_words_correct.append(missing_word.strip())

                            highlight += f"<span style='color:#414547'> ( <del>{new_word.strip()}</del> ) </span> "
                        else:
                            new_words.append(new_word.strip())
                            highlight += f"<span style='color:#414547'> ( <del>{new_word.strip()}</del> ) </span> "

                    else:
                        word = line[2:]
                        if word.strip() not in {"^", "--", "-"}:
                            highlight += f"<span style='color:black'>{word}</span> "


                differences = {'similarity_percentage':similarity_percentage,
                               'missing_words': missing_words,
                               'misspelled_words': misspelled_words,
                               'misspelled_words_correct':misspelled_words_correct,
                               #'new_words': new_words,
                               'highlight':highlight}

                return differences

            differences = compare_texts(service_file_script, service_text)



            def find_multiple_spellings(text, spellings):
                words = text.split()
                found_words = []
                for word in words:
                    for key, variants in spellings.items():
                        if word.lower() in variants:
                            found_words.append(word)
                return found_words

            multiple_spellings = find_multiple_spellings(service_text, multiple_spellings_list)

            def find_hyphenated_adjectives(text, hyphenatedadjectives):
                words = text.split()
                found_words = []
                for word in words:
                    for key in hyphenatedadjectives:
                        if key in word.lower():
                            found_words.append(key)
                return found_words

            hyphenated_adjectives = find_hyphenated_adjectives(service_file_script, hyphenated_adjectives_list)

            UK = []
            US = []
            for MS_item in MultipleSpellings.objects.all():
                for item in multiple_spellings:
                    if item == MS_item.UK:
                        UK.append(item)
                        US.append(MS_item.US)
                    elif item == MS_item.US:
                        US.append(item)
                        UK.append(MS_item.UK)
            multiple_spellings_full = {"UK":UK,"US":US}

            not_missing_words = []
            for miss in differences['missing_words']:
                for MS_item in MultipleSpellings.objects.all():
                    if miss == MS_item.UK:
                        if MS_item.US in differences['misspelled_words']:
                            not_missing_words.append(miss)
                    elif miss == MS_item.US:
                        if MS_item.UK in differences['misspelled_words']:
                            not_missing_words.append(miss)
                if miss.lower() in [item.lower() for item in differences['misspelled_words']]:
                    not_missing_words.append(miss)
            missing_words_final = [item for item in differences['missing_words'] if item not in not_missing_words]


            def compare_punctuation(user_text, original_text):
                characters_to_remove = "$%@*#/"
                original_text = re.sub(f"[{re.escape(characters_to_remove)}]", "", original_text)
                user_text = re.sub(f"[{re.escape(characters_to_remove)}]", "", user_text)

                punctuation_marks = ",!#$%@*.?-—;"
                highlighted_text = ""
                matcher = difflib.SequenceMatcher(None, original_text, user_text, autojunk=False)

                for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                    if tag == 'equal':
                        for char in user_text[j1:j2]:
                            if char.isupper():
                                highlighted_text += f'<span style="color:orange;">{char}</span>'
                            elif char in punctuation_marks:
                                highlighted_text += f'<span style="color:blue;">{char}</span>'
                            else:
                                highlighted_text += char
                    elif tag == 'replace' or tag == 'delete':
                        for i in range(i1, i2):
                            if original_text[i].isupper():
                                highlighted_text += f'<mark style="background-color:#f54c5a;">{original_text[i]}</mark>'
                            elif original_text[i] in punctuation_marks:
                                highlighted_text += f'<mark style="background-color:#f54c5a;">{original_text[i]}</mark>'
                        for j in range(j1, j2):
                            if user_text[j].isupper():
                                highlighted_text += f'<span style="color:orange;">{user_text[j]}</span>'
                            elif user_text[j] in punctuation_marks:
                                highlighted_text += f'<span style="color:green;">{user_text[j]}</span>'
                    elif tag == 'insert':
                        for j in range(j1, j2):
                            if user_text[j].isupper():
                                highlighted_text += f'<span style="color:orange;">{user_text[j]}</span>'
                            elif user_text[j] in punctuation_marks:
                                highlighted_text += f'<span style="color:green;">{user_text[j]}</span>'

                return highlighted_text

            punctuation_result = compare_punctuation(service.text, service.file.script)

            correction_data = {"file_user": StudentProfileSerializer(service.user).data,
                               "file_data": FileSerializer(service.file).data,
                               "file_script": service.file.script,
                               "student_text":service_text,
                               "differences":differences,
                               "missing_words_final":missing_words_final,
                               "multiple_spellings":multiple_spellings,
                               "multiple_spellings_full": multiple_spellings_full,
                               "hyphenated_adjectives":hyphenated_adjectives,
                               "punctuation":punctuation_result}

            data = {"service_data":serializer.data, "correction_data":correction_data}
            service.full_result = data
            service.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"service not found or something went wrong, try again. Error:{e}", status=status.HTTP_400_BAD_REQUEST)



class ServicesCorrectionV2(APIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def clean_text(self, text, characters_to_remove):
        return re.sub(f"[{re.escape(characters_to_remove)}]", "", text.replace('.', '. '))

    def find_multiple_spellings(self, text, spellings):
        words = text.split()
        return [word for word in words if any(word.lower() in variants for variants in spellings.values())]

    def find_hyphenated_adjectives(self, text, adjectives):
        return [word for word in text.split() if any(adj in word.lower() for adj in adjectives)]
    
    def compare_texts(self, original, revised):
        differ = Differ()
        
        seq_match = SequenceMatcher(None, original, revised)
        ratio = seq_match.ratio()
        similarity_percentage = ratio*100
        
        original_words = original.split()
        revised_words = revised.split()

        diff_result = list(differ.compare(original_words, revised_words))

        highlight_parts = []
        missing_words = []
        misspelled_words = []
        misspelled_words_correct = []
        
        for diff in diff_result:
            if diff.startswith('- '):  
                missing_word = diff[2:]
                missing_words.append(missing_word.strip())
                highlight_parts.append(f"<span style='color:#3a62c6'>(<b>{missing_word}</b>)</span>")

            elif diff.startswith('+ '): 
                extra_word = diff[2:]
                highlight_parts.append(f"<span style='color:#d34040'>{extra_word}</span>")
                

            elif diff.startswith('  '): 
                unchanged_word = diff[2:]
                highlight_parts.append(unchanged_word)

        final_parts = []
        skip_next = False
        for idx, part in enumerate(highlight_parts):
            if skip_next:
                skip_next = False
                continue

            if (
                "color:#3a62c6" in part
                and idx + 1 < len(highlight_parts)
                and "color:#d34040" in highlight_parts[idx + 1]
            ):
                blue_word = part.split("(<b>")[1].split("</b>)")[0]
                red_word = highlight_parts[idx + 1].split(">", 1)[1].split("<")[0]
                misspelled_words.append(red_word)
                misspelled_words_correct.append(blue_word)
                final_parts.append(
                    f"<span style='color:#868585;text-decoration:line-through'>({red_word})</span> <span style='color:#d34040'>{blue_word}</span>"
                )
                skip_next = True
            else:
                final_parts.append(part)

        corrected_parts = []
        for idx, part in enumerate(final_parts):
            if (
                "color:#d34040" in part
                and idx + 1 < len(final_parts)
                and "color:#3a62c6" in final_parts[idx + 1]
            ):
                red_word = part.split(">", 1)[1].split("<")[0]
                blue_word = final_parts[idx + 1].split("(<b>")[1].split("</b>)")[0]
                print(blue_word)
                corrected_parts.append(
                    f"<span style='color:#868585;text-decoration:line-through'>({red_word})</span> <span style='color:#d34040'>{blue_word}</span>"
                )
                skip_next = True
            else:
                corrected_parts.append(part)

        highlight = " ".join(corrected_parts)

        return {
            'similarity_percentage':similarity_percentage,
            'missing_words': missing_words,
            'misspelled_words': misspelled_words,
            'misspelled_words_correct':misspelled_words_correct,
            'highlight': highlight.strip()
        }


    def compare_punctuation(self, user_text, original_text):
        characters_to_remove = "$%@*#/"
        original_text = re.sub(f"[{re.escape(characters_to_remove)}]", "", original_text)
        user_text = re.sub(f"[{re.escape(characters_to_remove)}]", "", user_text)

        punctuation_marks = ",!#$%@*.?-—;:'"
        highlighted_text = ""
        matcher = SequenceMatcher(None, original_text, user_text, autojunk=False)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for char in user_text[j1:j2]:
                    if char.isupper():
                        highlighted_text += f'<span style="color:orange; font-weight:bold;">{char}</span>'
                    elif char in punctuation_marks:
                        highlighted_text += f'<span style="color:blue;">{char}</span>'
                    else:
                        highlighted_text += char
            elif tag == 'replace' or tag == 'delete':
                for i in range(i1, i2):
                    if original_text[i].isupper():
                        highlighted_text += f'<mark style="background-color:#f54c5a; color:white;">{original_text[i]}</mark>'
                    elif original_text[i] in punctuation_marks:
                        highlighted_text += f'<mark style="background-color:#f54c5a; color:white;">{original_text[i]}</mark>'
                for j in range(j1, j2):
                    if user_text[j].isupper():
                        highlighted_text += f'<span style="color:orange; font-weight:bold;">{user_text[j]}</span>'
                    elif user_text[j] in punctuation_marks:
                        highlighted_text += f'<span style="color:green;">{user_text[j]}</span>'
            elif tag == 'insert':
                for j in range(j1, j2):
                    if user_text[j].isupper():
                        highlighted_text += f'<span style="color:orange; font-weight:bold;">{user_text[j]}</span>'
                    elif user_text[j] in punctuation_marks:
                        highlighted_text += f'<span style="color:green;">{user_text[j]}</span>'

        return highlighted_text

    def get(self, request, *args, **kwargs):
        try:
            service = get_object_or_404(Service, id=self.kwargs["id"])
            serializer = self.serializer_class(service)

            characters_to_remove = ",!#$%@*.?/"
            service_file_script = self.clean_text(service.file.script, characters_to_remove)
            service_text = self.clean_text(service.text, characters_to_remove)
            
            print(service_file_script)

            multiple_spellings = {item.US: [item.US, item.UK] for item in MultipleSpellings.objects.all()}
            hyphenated_adjectives = list(HyphenatedAdjectives.objects.values_list('US', flat=True))

            differences = self.compare_texts(service_file_script, service_text)
            punctuation_result = self.compare_punctuation(service.text, service.file.script)

            multiple_spellings_found = self.find_multiple_spellings(service_text, multiple_spellings)
            hyphenated_adjectives_found = self.find_hyphenated_adjectives(service_file_script, hyphenated_adjectives)

            multiple_spellings_full = {
                "UK": [item.UK for item in MultipleSpellings.objects.filter(US__in=multiple_spellings_found)],
                "US": [item.US for item in MultipleSpellings.objects.filter(UK__in=multiple_spellings_found)]
            }

            missing_words_final = [
                word for word in differences['missing_words']
                if word.lower() not in (w.lower() for w in differences['misspelled_words'])
            ]

            correction_data = {
                "file_user": StudentProfileSerializer(service.user).data,
                "file_data": FileSerializer(service.file).data,
                "file_script": service.file.script,
                "student_text": service_text,
                "differences": differences,
                "missing_words_final": missing_words_final,
                "multiple_spellings": multiple_spellings_found,
                "multiple_spellings_full": multiple_spellings_full,
                "hyphenated_adjectives": hyphenated_adjectives_found,
                "punctuation": punctuation_result
            }

            data = {"service_data": serializer.data, "correction_data": correction_data}
            service.full_result = data
            service.save()

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Service not found or something went wrong. Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)


