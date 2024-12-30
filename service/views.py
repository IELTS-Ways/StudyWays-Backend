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

    def clean_text(self, text, characters_to_remove):
        return re.sub(f"[{re.escape(characters_to_remove)}]", "", text.replace('.', '. '))

    def get(self, *args, **kwargs):
        service = Service.objects.get(id=self.kwargs["id"])


        characters_to_remove = ",!#$%@*.?/"
        service_file_script = self.clean_text(service.file.script, characters_to_remove)
        service_text = self.clean_text(service.text, characters_to_remove)

        student_text = service_text
        original_text = service_file_script

        token = "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"

        try:
            client = OpenAI(api_key=token)
            # Replace 'token' with your actual OpenAI API key

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": "You are an expert text analyzer specializing in identifying differences between texts and highlighting them in HTML."},
                    {"role": "user", "content": f"""
                        Compare a text typed by the user with the reference text and accurately identify the differences between the two. 
                        Deliver the differences highlighted in HTML using the following color coding:
                        - Misspelled words: gray color (indicate with <span style='color:gray'>).
                        - Correct form of misspelled words from the reference text: red color (indicate with <span style='color:red'>).
                        - Missing words (present in reference text but not in user text): blue color (indicate with <span style='color:blue'>).
                        - Extra words (present in user text but not in reference text): purple color (indicate with <span style='color:purple'>).

                        Student Text: {student_text}
                        Reference Text: {original_text}
                    """},
                ],
                max_tokens=1500,  # Adjust as needed for longer responses
                stop=None,
                temperature=0.7
            )
            response_dict = response.model_dump()
            message_content = response_dict['choices'][0]['message']['content']
            # The variable `message_content` now contains the HTML response with the highlighted differences
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
        substitutions = {
            "i'm": "i am",
            "you're": "you are",
            "he's": ["he is", "he has"],
            "she's": ["she is", "she has"],
            "it's": ["it is", "it has"],
            "we're": "we are",
            "they're": "they are",
            "can't": "cannot",
            "don't": "do not",
            "didn't": "did not",
            "won't": "will not",
            "haven't": "have not",
            "hadn't": "had not",
            "couldn't": "could not",
            "shouldn't": "should not",
            "wouldn't": "would not",
            "doesn't": "does not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "hasn't": "has not",
            "you'd": ["you had", "you would"],
            "he'd": ["he had", "he would"],
            "she'd": ["she had", "she would"],
            "it'd": ["it had", "it would"],
            "we'd": ["we had", "we would"],
            "they'd": ["they had", "they would"],
            "that's": ["that is", "that has"],
            "there's": ["there is", "there has"],
            "who's": ["who is", "who has"],
            "what's": ["what is", "what has"],
            "where's": ["where is", "where has"],
            "when's": ["when is", "when has"],
            "why's": ["why is", "why has"],
            "here's": "here is",
            # other
        }

        def normalize_text(text):
            words = text.split()
            normalized_words = []
            for i, word in enumerate(words):
                if word in substitutions:
                    value = substitutions[word]
                    if isinstance(value, list):
                        previous_word = words[i-1] if i > 0 else ''
                        next_word = words[i+1] if i < len(words)-1 else ''
                        if previous_word in ["he", "she", "it", "who", "what", "where", "when", "why", "that", "there"]:
                            normalized_words.append(value[0])
                        elif next_word in ["been", "gone"]:
                            normalized_words.append(value[1])
                        else:
                            normalized_words.append(value[0])
                    else:
                        normalized_words.append(value)
                else:
                    normalized_words.append(word)
            return " ".join(normalized_words)

        original = normalize_text(original.lower())
        revised = normalize_text(revised.lower())

        differ = Differ()
        seq_match = SequenceMatcher(None, original, revised)
        ratio = seq_match.ratio()
        similarity_percentage = ratio * 100

        original_words = original.split()
        revised_words = revised.split()

        diff_result = list(differ.compare(original_words, revised_words))

        highlight_parts = []
        missing_words = []
        misspelled_words = []
        misspelled_words_correct = []

        irrelevant_words = set([
            "a", "an", "the", "i", "you", "your", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
            "in", "on", "at", "by", "to", "from", "with", "about", "for", "of", "after", "before",
            "and", "but", "or", "so", "yet", "nor", "for",
            "is", "are", "am", "was", "were", "be", "being", "been", "do", "does", "did", "have", "has", "had",
            "will", "would", "shall", "should", "can", "could", "may", "might", "must",
            "very", "too", "also", "just", "now", "then", "here", "there", "when", "where", "why", "how",
            "this", "that", "these", "those", "some", "any", "each", "every", "no", "many", "few", "all", "both", "half"
        ])

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
        swapped_indices = set()

        for idx, part in enumerate(highlight_parts):
            if skip_next:
                skip_next = False
                continue

            if (
                "color:#3a62c6" in part
                and idx + 1 < len(highlight_parts)
                and "color:#d34040" in highlight_parts[idx + 1]
                and idx not in swapped_indices
            ):
                blue_word = part.split("(<b>")[1].split("</b>)")[0]
                red_word = highlight_parts[idx + 1].split(">", 1)[1].split("<")[0]
                misspelled_words.append(red_word)
                if blue_word.lower() not in irrelevant_words:
                    misspelled_words_correct.append(blue_word)
                final_parts.append(
                    f"<span style='color:#868585'>(<b>{red_word}</b>)</span> <span style='color:#d34040'>{blue_word}</span>"
                )
                swapped_indices.add(idx + 1)
                skip_next = True
            else:
                final_parts.append(part)

        final_highlight = []
        for part in final_parts:
            if "color:#d34040" in part and "color:#868585" not in part:
                red_word = part.split(">", 1)[1].split("<")[0]
                final_highlight.append(
                    f"<span style='color:#9940d3;text-decoration:line-through'>({red_word})</span>"
                )
            else:
                final_highlight.append(part)

        highlight = " ".join(final_highlight)

        return {
            'similarity_percentage': similarity_percentage,
            'missing_words': missing_words,
            'misspelled_words': misspelled_words,
            'misspelled_words_correct': misspelled_words_correct,
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
            # Break the loop if we reach the end of the user's text
            if j1 >= len(user_text):
                break

            if tag == 'equal':
                highlighted_text += user_text[j1:j2]
            elif tag == 'replace':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    if j >= len(user_text):  # Stop processing if beyond user text
                        break
                    if original_text[i].isupper() and not user_text[j].isupper():
                        highlighted_text += f'<mark style="background-color:#f54c5a; color:white;">{original_text[i]}</mark>'
                    elif not original_text[i].isupper() and user_text[j].isupper():
                        highlighted_text += f'<mark style="background-color:#f54c5a; color:white;">{original_text[i]}</mark>'
                    elif user_text[j] in punctuation_marks:
                        highlighted_text += f'<span style="color:blue;">{user_text[j]}</span>'
                    else:
                        highlighted_text += user_text[j]
            elif tag == 'delete':
                for i in range(i1, i2):
                    if i >= len(user_text):  # Stop processing if beyond user text
                        break
                    if original_text[i] in punctuation_marks:
                        highlighted_text += f'<span style="color:blue;">{original_text[i]}</span>'
            elif tag == 'insert':
                for j in range(j1, j2):
                    if j >= len(user_text):  # Stop processing if beyond user text
                        break
                    if user_text[j] in punctuation_marks:
                        highlighted_text += f'<span style="color:blue;">{user_text[j]}</span>'
                    else:
                        highlighted_text += user_text[j]

        return highlighted_text




    def get(self, request, *args, **kwargs):
        try:
            service = get_object_or_404(Service, id=self.kwargs["id"])
            serializer = self.serializer_class(service)

            characters_to_remove = ",!#$%@*.?/"
            service_file_script = self.clean_text(service.file.script, characters_to_remove)
            service_text = self.clean_text(service.text, characters_to_remove)
            
            multiple_spellings = {item.US: [item.US, item.UK] for item in MultipleSpellings.objects.all()}
            hyphenated_adjectives = list(HyphenatedAdjectives.objects.values_list('US', flat=True))

            differences = self.compare_texts(service_file_script, service_text)
            punctuation_result = self.compare_punctuation(service.text, service.file.script)

            multiple_spellings_found = self.find_multiple_spellings(service_text, multiple_spellings)
            hyphenated_adjectives_found = self.find_hyphenated_adjectives(service_file_script, hyphenated_adjectives)

            UK = []
            US = []
            for MS_item in MultipleSpellings.objects.all():
                for item in multiple_spellings_found:
                    if item == MS_item.UK:
                        UK.append(item)
                        US.append(MS_item.US)
                    elif item == MS_item.US:
                        US.append(item)
                        UK.append(MS_item.UK)
            multiple_spellings_full = {"UK":UK,"US":US}

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

