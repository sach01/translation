from django import forms
from .models import (
    Vocabulary, Feedback, Synonym, Antonym, Phrase, NamedEntity,
    SentenceAlignment, GrammarStructure, LanguageStructure, TranslationMemory,
    TranslationError, Morphology
)

# Vocabulary Form
class VocabularyForm(forms.ModelForm):
    class Meta:
        model = Vocabulary
        fields = [
            'source_language', 'source_word', 'target_language', 'target_word', 
            'definition', 'usage_notes', 'phonetic_translation', 
            'audio_pronunciation', 'base_form', 'past_form', 'future_form', 
            'plural_form', 'example_sentence_source_present',
            'example_sentence_source_past', 'example_sentence_source_future',
            'example_sentence_target_present', 'example_sentence_target_past',
            'example_sentence_target_future', 'cultural_context'
        ]

# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['vocabulary', 'user_feedback', 'accuracy_rating', 'needs_correction']

# Synonym Form
class SynonymForm(forms.ModelForm):
    class Meta:
        model = Synonym
        fields = ['vocabulary', 'synonym_word', 'synonym_meaning', 'synonym_language']

# Antonym Form
class AntonymForm(forms.ModelForm):
    class Meta:
        model = Antonym
        fields = ['vocabulary', 'antonym_word', 'antonym_meaning', 'antonym_language']

# Phrase Form
class PhraseForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = [
            'phrase', 'source_language', 'target_translation', 'literal_translation',
            'cultural_meaning', 'is_idiomatic'
        ]

# Named Entity Form
class NamedEntityForm(forms.ModelForm):
    class Meta:
        model = NamedEntity
        fields = ['source_language', 'name', 'entity_type', 'target_translation']

# Sentence Alignment Form
class SentenceAlignmentForm(forms.ModelForm):
    class Meta:
        model = SentenceAlignment
        fields = [
            'source_language', 'target_language', 'source_sentence', 
            'target_sentence', 'source_corpus', 'target_corpus', 'alignment_score'
        ]

# Grammar Structure Form
class GrammarStructureForm(forms.ModelForm):
    class Meta:
        model = GrammarStructure
        fields = [
            'source_sentence', 'target_sentence', 'source_language', 
            'target_language', 'grammatical_structure', 'tense', 'pronouns_used', 'negation'
        ]

# Language Structure Form
class LanguageStructureForm(forms.ModelForm):
    class Meta:
        model = LanguageStructure
        fields = [
            'language', 'word_order', 'phonology', 'morphology', 'syntax', 
            'semantics', 'writing_system'
        ]

# Translation Memory Form
class TranslationMemoryForm(forms.ModelForm):
    class Meta:
        model = TranslationMemory
        fields = [
            'vocabulary', 'translation', 'source_meaning', 'target_meaning',
            'usage_frequency', 'confidence_score'
        ]

# Translation Error Form
class TranslationErrorForm(forms.ModelForm):
    class Meta:
        model = TranslationError
        fields = [
            'original_sentence', 'error_description', 'correction', 
            'reported_by', 'status', 'priority_level'
        ]

# Morphology Form
class MorphologyForm(forms.ModelForm):
    class Meta:
        model = Morphology
        fields = [
            'vocabulary', 'plural_form', 'conjugated_forms'
        ]
