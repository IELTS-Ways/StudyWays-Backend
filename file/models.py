from django.db import models


class File(models.Model):
    language_type_choices = (
        ("English", "English"),
        ("German", "German"),
        ("Arabic", "Arabic"),
        ("French", "French"),
        ("Turkish", "Turkish"),
        ("Afrikaans", "Afrikaans"),
        ("Albanian", "Albanian"),
        ("Amharic", "Amharic"),
        ("Armenian", "Armenian"),
        ("Azerbaijani", "Azerbaijani"),
        ("Basque", "Basque"),
        ("Belarusian", "Belarusian"),
        ("Bengali", "Bengali"),
        ("Bosnian", "Bosnian"),
        ("Bulgarian", "Bulgarian"),
        ("Catalan", "Catalan"),
        ("Cebuano", "Cebuano"),
        ("Chinese", "Chinese"),
        ("Corsican", "Corsican"),
        ("Croatian", "Croatian"),
        ("Czech", "Czech"),
        ("Danish", "Danish"),
        ("Dutch", "Dutch"),
        ("Esperanto", "Esperanto"),
        ("Estonian", "Estonian"),
        ("Farsi", "Farsi"),
        ("Finnish", "Finnish"),
        ("French", "French"),
        ("Frisian", "Frisian"),
        ("Galician", "Galician"),
        ("Georgian", "Georgian"),
        ("Greek", "Greek"),
        ("Gujarati", "Gujarati"),
        ("Haitian Creole", "Haitian Creole"),
        ("Hausa", "Hausa"),
        ("Hawaiian", "Hawaiian"),
        ("Hebrew", "Hebrew"),
        ("Hindi", "Hindi"),
        ("Hmong", "Hmong"),
        ("Hungarian", "Hungarian"),
        ("Icelandic", "Icelandic"),
        ("Igbo", "Igbo"),
        ("Indonesian", "Indonesian"),
        ("Irish", "Irish"),
        ("Italian", "Italian"),
        ("Japanese", "Japanese"),
        ("Javanese", "Javanese"),
        ("Kannada", "Kannada"),
        ("Kazakh", "Kazakh"),
        ("Khmer", "Khmer"),
        ("Kinyarwanda", "Kinyarwanda"),
        ("Korean", "Korean"),
        ("Kurdish", "Kurdish"),
        ("Kyrgyz", "Kyrgyz"),
        ("Lao", "Lao"),
        ("Latvian", "Latvian"),
        ("Lithuanian", "Lithuanian"),
        ("Luxembourgish", "Luxembourgish"),
        ("Macedonian", "Macedonian"),
        ("Malagasy", "Malagasy"),
        ("Malay", "Malay"),
        ("Malayalam", "Malayalam"),
        ("Maltese", "Maltese"),
        ("Maori", "Maori"),
        ("Marathi", "Marathi"),
        ("Mongolian", "Mongolian"),
        ("Myanmar", "Myanmar"),
        ("Nepali", "Nepali"),
        ("Norwegian", "Norwegian"),
        ("Nyanja", "Nyanja"),
        ("Odia", "Odia"),
        ("Pashto", "Pashto"),
        ("Persian", "Persian"),
        ("Polish", "Polish"),
        ("Portuguese", "Portuguese"),
        ("Punjabi", "Punjabi"),
        ("Romanian", "Romanian"),
        ("Russian", "Russian"),
        ("Samoan", "Samoan"),
        ("Scots Gaelic", "Scots Gaelic"),
        ("Serbian", "Serbian"),
        ("Sesotho", "Sesotho"),
        ("Shona", "Shona"),
        ("Sindhi", "Sindhi"),
        ("Sinhala", "Sinhala"),
        ("Slovak", "Slovak"),
        ("Slovenian", "Slovenian"),
        ("Somali", "Somali"),
        ("Spanish", "Spanish"),
        ("Sundanese", "Sundanese"),
        ("Swahili", "Swahili"),
        ("Swedish", "Swedish"),
        ("Tagalog", "Tagalog"),
        ("Tajik", "Tajik"),
        ("Tamil", "Tamil"),
        ("Tatar", "Tatar"),
        ("Telugu", "Telugu"),
        ("Thai", "Thai"),
        ("Turkish", "Turkish"),
        ("Turkmen", "Turkmen"),
        ("Ukrainian", "Ukrainian"),
        ("Urdu", "Urdu"),
        ("Uyghur", "Uyghur"),
        ("Uzbek", "Uzbek"),
        ("Vietnamese", "Vietnamese"),
        ("Welsh", "Welsh"),
        ("Xhosa", "Xhosa"),
        ("Yiddish", "Yiddish"),
        ("Yoruba", "Yoruba"),
        ("Zulu", "Zulu"),)

    book_type_choices = (
        ("IELTS", "IELTS"),
        ("Inside Reading", "Inside Reading"),
        ("Inside Writing", "Inside Writing"),
        ("Teen2Teen", "Teen2Teen"),
        ("Four Corners", "Four Corners"),
        ("Four Corners Video Activity", "Four Corners Video Activity"),
        ("Cambridge", "Cambridge"),
        ("Academic Cambridge", "Academic Cambridge"),
        ("General Cambridge", "General Cambridge"),
        ("Evolve", "Evolve"),
        ("Evolve Video", "Evolve Video"),
        ("Top Notch Fundamentals", "Top Notch Fundamentals"),
        ("Top Notch", "Top Notch"),
        ("Interchange", "Interchange"),
        ("Interchange Video", "Interchange Video"),
        ("Market Leader", "Market Leader"),
        ("Passages", "Passages"),
        ("Touchstone", "Touchstone"),
        ("Viewpoint", "Viewpoint"),
        ("American English File", "American English File"),
        ("American English File Video", "American English File Video"),
        ("Cutting Edge", "Cutting Edge"),
        ("Tactics for Listening", "Tactics for Listening"),
        ("Active Listening", "Active Listening"),
        ("Magazine", "Magazine"),
        ("Other", "Other"),)

    skill_type_choices = (
        ("Writing", "Writing"),
        ("WritingWithMedia", "WritingWithMedia"),
        ("Reading", "Reading"),
        ("Listening", "Listening"),
        ("Video", "Video"),
        ("Podcast", "Podcast"),
        ("Song", "Song"),
        ("News", "News"),
        ("Periodicals", "Periodicals"),
        ("Story Book", "Story Book"),)

    cefr_choices = (
        ("Beginner (Easy Start/Starter)", "Beginner (Easy Start/Starter)"),
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),)

    spelling_choices = (("UK", "UK"),("US", "US"),)

    default_book_cover_photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4pNg-HwTm_WImVeVUgDnRSXU8awW_xMoN85BhqrsRpzMlywHe31eyadJ-zbs7PFFtidE&usqp=CAU"

    CEFR =  models.CharField(max_length=80,choices=cefr_choices)
    #is_video = models.BooleanField(default=False)
    language = models.CharField(max_length=50,default="English" , choices=language_type_choices)
    skill_type = models.CharField(max_length=50,choices=skill_type_choices)
    book_type = models.CharField(max_length=50,choices=book_type_choices)
    material_type = models.CharField(max_length=30, default="UK", choices=spelling_choices)
    book = models.CharField(max_length=100,blank=True,null=True)
    unit = models.CharField(max_length=100,blank=True, null=True)
    page = models.CharField(max_length=100, blank=True, null=True)
    cd = models.CharField(max_length=100,blank=True, null=True)
    track = models.CharField(max_length=100,blank=True, null=True)
    lyrics = models.CharField(max_length=100, blank=True, null=True)
    test = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    passage = models.CharField(max_length=100, blank=True, null=True)
    episode = models.CharField(max_length=100, blank=True, null=True)
    unit_opener = models.CharField(max_length=100, blank=True, null=True)
    article_title = models.CharField(max_length=100, blank=True, null=True)
    unit_title = models.CharField(max_length=100, blank=True, null=True)
    file = models.URLField(blank=True,null=True)
    script = models.TextField(max_length=10000,blank=True, null=True)
    book_cover_photo_url = models.CharField(max_length=300,blank=True,null=True,default=default_book_cover_photo_url)

    def __str__(self):
        return str(self.book) +"|"+ str(self.unit) +"|" +str(self.page) +"|"+ str(self.cd) +"|"+ str(self.track)
