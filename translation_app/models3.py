from django.db import models

# Language Model
class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

# Sentence Alignment Model for Parallel Corpus
class SentenceAlignment(models.Model):
    source_sentence = models.TextField()
    target_sentence = models.TextField()
    source_language = models.ForeignKey(Language, related_name="source_sentences", on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language, related_name="target_sentences", on_delete=models.CASCADE)
    source_corpus = models.CharField(max_length=100, null=True, blank=True)  # E.g., Bible, Legal, Folklore
    target_corpus = models.CharField(max_length=100, null=True, blank=True)
    alignment_score = models.FloatField(default=1.0)  # Optional: rating of alignment

    def __str__(self):
        return f"{self.source_sentence[:50]} -> {self.target_sentence[:50]}"

# Dialect Model
class Dialect(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='dialects')

    def __str__(self):
        return f"{self.name} - {self.region}"

# Vocabulary Model for Word-Level Translations
class Vocabulary(models.Model):
    source_word = models.CharField(max_length=100)
    target_word = models.CharField(max_length=100)
    source_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='source_vocabularies')
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_vocabularies')
    dialect = models.ForeignKey(Dialect, on_delete=models.SET_NULL, null=True, blank=True)
    part_of_speech = models.CharField(max_length=50)  # E.g., Noun, Verb, Adjective
    phonetic_transcription = models.CharField(max_length=255, null=True, blank=True)
    plural_form = models.CharField(max_length=255, null=True, blank=True)
    conjugated_forms = models.JSONField(null=True, blank=True)  # JSON for verb forms

    def __str__(self):
        return f"{self.source_word} ({self.source_language.name}) -> {self.target_word} ({self.target_language.name})"

# Grammar Structure Model
class GrammarStructure(models.Model):
    source_sentence = models.TextField()
    target_sentence = models.TextField()
    source_language = models.ForeignKey(Language, related_name="source_grammar", on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language, related_name="target_grammar", on_delete=models.CASCADE)
    grammatical_structure = models.CharField(max_length=100)  # E.g., SVO, Negation
    tense = models.CharField(max_length=50, null=True, blank=True)  # Present, Past, Future
    pronouns_used = models.CharField(max_length=100, null=True, blank=True)
    negation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.source_sentence[:50]} -> {self.target_sentence[:50]} ({self.grammatical_structure})"

# Phrase Model for Idioms and Phrases
class Phrase(models.Model):
    phrase = models.CharField(max_length=255)
    source_language = models.ForeignKey(Language, related_name="phrases", on_delete=models.CASCADE)
    target_translation = models.TextField()
    literal_translation = models.TextField()
    cultural_meaning = models.TextField()  # Actual meaning in context
    is_idiomatic = models.BooleanField(default=False)

    def __str__(self):
        return f"Phrase: {self.phrase} ({self.source_language.name})"

# Dialectal Variation Model
class DialectVariation(models.Model):
    dialect = models.ForeignKey(Dialect, on_delete=models.CASCADE, related_name="variations")
    standard_word = models.CharField(max_length=100)
    dialect_word = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dialect_word} ({self.dialect.name} - {self.region})"

# Named Entity Model
class NamedEntity(models.Model):
    name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50)  # E.g., Person, Place, Organization
    source_language = models.ForeignKey(Language, related_name="named_entities", on_delete=models.CASCADE)
    target_translation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Named Entity: {self.name} ({self.entity_type})"

# Audio Pronunciation Model
class AudioPronunciation(models.Model):
    word = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name="audio_pronunciations")
    audio_file = models.FileField(upload_to='audio_files/')
    phonetic_transcription = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Audio Pronunciation of {self.word.source_word}"

# Translation Feedback Model
class TranslationFeedback(models.Model):
    sentence_alignment = models.ForeignKey(SentenceAlignment, on_delete=models.CASCADE, related_name="feedback")
    user_feedback = models.TextField()
    accuracy_rating = models.IntegerField()  # Rating from 1 to 5
    reported_by = models.CharField(max_length=100)  # User providing feedback
    correction_suggestion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Feedback for: {self.sentence_alignment.source_sentence[:50]}"
