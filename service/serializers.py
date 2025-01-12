from rest_framework import serializers
from service.models import Service, MultipleSpellings, HyphenatedAdjectives, FeedbackSystem, DraftService
from file.serializers import FileSerializer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        #fields = "__all__"
        exclude = ['full_result']
        

class DraftServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DraftService
        #fields = "__all__"
        exclude = ['full_result']
        

class DraftItemServiceSerializer(serializers.ModelSerializer):
    file_details = FileSerializer(source='file', read_only=True)
    
    class Meta:
        model = DraftService
        #fields = "__all__"
        exclude = ['full_result']
        
        
class ServiceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        # fields = "__all__"
        exclude = ['playback', 'full_result', 'share_with']
        
        
class MultipleSpellingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleSpellings
        fields = "__all__"


class HyphenatedAdjectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HyphenatedAdjectives
        fields = ['word']



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackSystem
        fields = "__all__"