from rest_framework import serializers
from .models import (
    Vocabulary, GrammarStructure, SentenceAlignment, RelatedWord,
    Phrase, NamedEntity, Feedback, Morphology, TranslationMemory,
    TrainingData, TranslationError, Moderation, Numbers
)

class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'

class GrammarStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarStructure
        fields = '__all__'

class SentenceAlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentenceAlignment
        fields = '__all__'

class RelatedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedWord
        fields = '__all__'

class PhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrase
        fields = '__all__'

class NamedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NamedEntity
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class MorphologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Morphology
        fields = '__all__'

class TranslationMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationMemory
        fields = '__all__'

class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = '__all__'

class TranslationErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationError
        fields = '__all__'

class ModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderation
        fields = '__all__'

class NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numbers
        fields = '__all__'
