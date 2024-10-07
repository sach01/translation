from django import forms
from .models import (
    User, Numbers, Language, Dialect, PartOfSpeech, Vocabulary,
    GrammarStructure, SentenceAlignment, RelatedWord, Phrase, NamedEntity,
    Feedback, Morphology, TranslationMemory, TrainingData, TranslationError,
    Moderation, UserProfile, Badge, Reward, Progress, Achievement, Leaderboard
)


# User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'user_permissions']


# Numbers Form
class NumbersForm(forms.ModelForm):
    class Meta:
        model = Numbers
        fields = ['number', 'in_borana', 'user']


# Language Form
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'code']


# Dialect Form
class DialectForm(forms.ModelForm):
    class Meta:
        model = Dialect
        fields = ['language', 'name', 'region']


# Part of Speech Form
class PartOfSpeechForm(forms.ModelForm):
    class Meta:
        model = PartOfSpeech
        fields = ['name']


# Vocabulary Form
class VocabularyForm(forms.ModelForm):
    class Meta:
        model = Vocabulary
        fields = [
            'user', 'dialect', 'source_language', 'source_word', 'source_meaning',
            'target_language', 'target_word', 'target_meaning', 'part_of_speech',
            'phonetic_translation', 'example_sentence_source_present', 'example_sentence_source_past',
            'example_sentence_source_future', 'example_sentence_target_present', 'example_sentence_target_past',
            'example_sentence_target_future', 'definition', 'usage_notes', 'cultural_context', 'audio_pronunciation'
        ]


# Grammar Structure Form
class GrammarStructureForm(forms.ModelForm):
    class Meta:
        model = GrammarStructure
        fields = [
            'source_language', 'target_language', 'rule_name', 'source_sentence',
            'target_sentence', 'grammatical_structure', 'grammar_type', 'level', 'tense', 'pronouns_used', 'negation'
        ]


# Sentence Alignment Form
class SentenceAlignmentForm(forms.ModelForm):
    class Meta:
        model = SentenceAlignment
        fields = ['source_language', 'target_language', 'source_corpus', 'source_sentence', 'target_sentence', 'target_corpus', 'alignment_score']


# Related Word Form
class RelatedWordForm(forms.ModelForm):
    class Meta:
        model = RelatedWord
        fields = ['vocabulary', 'synonym_language', 'word', 'relationship_type', 'meaning']


# Phrase Form
class PhraseForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = ['phrase', 'source_language', 'target_translation', 'literal_translation', 'cultural_meaning', 'phrase_type']


# Named Entity Form
class NamedEntityForm(forms.ModelForm):
    class Meta:
        model = NamedEntity
        fields = ['source_language', 'name', 'entity_type', 'target_translation']


# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['vocabulary', 'user_feedback', 'accuracy_rating', 'needs_correction']


# Morphology Form
class MorphologyForm(forms.ModelForm):
    class Meta:
        model = Morphology
        fields = ['vocabulary', 'base_form', 'past_form', 'future_form', 'plural_form']


# Translation Memory Form
class TranslationMemoryForm(forms.ModelForm):
    class Meta:
        model = TranslationMemory
        fields = ['vocabulary', 'translation', 'source_meaning', 'target_meaning', 'usage_frequency', 'confidence_score']


# Training Data Form
class TrainingDataForm(forms.ModelForm):
    class Meta:
        model = TrainingData
        fields = ['sentence', 'translation', 'feedback_score', 'language']


# Translation Error Form
class TranslationErrorForm(forms.ModelForm):
    class Meta:
        model = TranslationError
        fields = ['original_sentence', 'error_description', 'correction', 'reported_by', 'status', 'priority_level']


# Moderation Form
class ModerationForm(forms.ModelForm):
    class Meta:
        model = Moderation
        fields = ['content_type', 'object_id', 'contributor', 'status', 'moderator', 'review_notes']


# UserProfile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'avatar', 'points', 'level', 'badges', 'progress']


# Badge Form
class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'icon']


# Reward Form
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['user', 'points', 'level', 'badge']


# Progress Form
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = [
            'user', 'vocabulary_contributions', 'feedback_provided', 'synonyms_added', 'antonyms_added',
            'phrases_contributed', 'named_entities_contributed', 'sentences_aligned', 'grammar_structures_contributed',
            'language_structures_contributed', 'translation_memory_contributions', 'translation_errors_logged',
            'morphology_contributed', 'training_data_submitted', 'points_earned'
        ]


# Achievement Form
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['user', 'achievement_name', 'description']


# Leaderboard Form
class LeaderboardForm(forms.ModelForm):
    class Meta:
        model = Leaderboard
        fields = ['user', 'points', 'rank']
