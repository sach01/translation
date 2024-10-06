from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User Model
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name='translation_app_users', blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='translation_app_users', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# Language Model
class Numbers(models.Model):
    number = models.IntegerField()
    in_borana = models.CharField(max_length=1000)

    def __str__(self):
        return self.in_borana

# Language Model
class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

# Dialect Model
class Dialect(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='dialects')
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language} - {self.name} - {self.region}"

# Part of Speech Model
class PartOfSpeech(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Vocabulary Model for Morphology, Conjugation, and Pluralization
class Vocabulary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vocabularies')
    dialect = models.ForeignKey(Dialect, on_delete=models.SET_NULL, null=True, blank=True, related_name='vocabularies')
    source_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='source_vocabularies')
    source_word = models.CharField(max_length=100)  # Base form in Borana or English
    source_meaning = models.TextField(blank=True)  # Meaning of the source word
    
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_vocabularies')
    target_word = models.CharField(max_length=100)  # Translation in the target language
    target_meaning = models.TextField(blank=True)  # Meaning of the target word

    part_of_speech = models.ForeignKey(PartOfSpeech, on_delete=models.CASCADE, related_name='vocabularies')  # ForeignKey to PartOfSpeech model
    phonetic_translation = models.CharField(max_length=100) 
    
    # Morphological details
    base_form = models.CharField(max_length=100)  # Present Simple or singular form
    past_form = models.CharField(max_length=100, blank=True)  # Past tense (if applicable)
    future_form = models.CharField(max_length=100, blank=True)  # Future tense (if applicable)
    plural_form = models.CharField(max_length=100, blank=True)  # Pluralization (if applicable)
    
    # Example sentences source
    example_sentence_source_present = models.TextField(blank=True)
    example_sentence_source_past = models.TextField(blank=True)
    example_sentence_source_future = models.TextField(blank=True)
    
    # Example sentences target
    example_sentence_target_present = models.TextField(blank=True)
    example_sentence_target_past = models.TextField(blank=True)
    example_sentence_target_future = models.TextField(blank=True)

    # Additional data
    definition = models.TextField()
    usage_notes = models.TextField(blank=True)
    cultural_context = models.TextField(blank=True)
    audio_pronunciation = models.FileField(upload_to='pronunciations/', blank=True)

    def __str__(self):
        return self.source_word

# Grammar Structure Model
class GrammarStructure(models.Model):
    source_sentence = models.TextField(help_text="Enter the sentence in Borana (e.g., 'Ani si argaa' for 'I see you').")
    target_sentence = models.TextField(help_text="Enter the translated sentence in English (e.g., 'I see you' for 'Ani si argaa').")
    source_language = models.ForeignKey(Language, related_name="source_grammar", on_delete=models.CASCADE, help_text="Select the source language (e.g., Borana)")
    target_language = models.ForeignKey(Language, related_name="target_grammar", on_delete=models.CASCADE, help_text="Select the target language (e.g., English)")
    grammatical_structure = models.CharField(max_length=100, help_text="Describe the grammatical structure (e.g., 'SVO' for Subject-Verb-Object).")
    tense = models.CharField(max_length=50, null=True, blank=True, help_text="Specify the tense (e.g., 'Present', 'Past', 'Future').")
    pronouns_used = models.CharField(max_length=100, null=True, blank=True, help_text="List the pronouns used in the sentence (e.g., 'Ani' for 'I').")
    negation = models.BooleanField(default=False, help_text="Check this box if the sentence includes negation (e.g., 'Ani hin dhufne' for 'I did not come').")

    def __str__(self):
        return f"{self.source_sentence[:50]} -> {self.target_sentence[:50]} ({self.grammatical_structure})"

class LanguageStructure(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='language_structures')
    word_order = models.CharField(max_length=100, help_text="Describe the word order (e.g., 'SVO', 'VSO', 'SOV')")
    phonology = models.TextField(help_text="Describe the sound rules and pronunciation guidelines.")
    morphology = models.TextField(help_text="Describe the rules for word formation, including inflections, prefixes, and suffixes.")
    syntax = models.TextField(help_text="Describe how words and phrases are arranged to create sentences.")
    semantics = models.TextField(help_text="Describe the overarching structure of meaning in the language.")
    writing_system = models.TextField(help_text="Describe the punctuation and writing system rules.")
    
    def __str__(self):
        return f"Language Structure for {self.language.name}"

# Sentence Alignment Model (Parallel Corpus)
class SentenceAlignment(models.Model):
    source_language = models.ForeignKey(Language, related_name="source_sentences", on_delete=models.CASCADE, help_text="Select the source language (e.g., Borana)")
    target_language = models.ForeignKey(Language, related_name="target_sentences", on_delete=models.CASCADE, help_text="Select the target language (e.g., English)")
    source_corpus = models.CharField(max_length=100, null=True, blank=True, help_text="Specify the type of corpus (e.g., 'Conversation', 'Bible', 'Folklore').")
    source_sentence = models.TextField(help_text="Enter the sentence in the source language (e.g., 'Wo'ee haa' for 'How are you?').")
    target_sentence = models.TextField(help_text="Enter the corresponding sentence in the target language (e.g., 'How are you?' for 'Wo'ee haa').")
    target_corpus = models.CharField(max_length=100, null=True, blank=True, help_text="Specify the type of corpus for the target sentence (e.g., 'Conversation', 'Bible').")
    alignment_score = models.FloatField(default=1.0, help_text="Optional: Rate the quality of alignment between the sentences (1.0 means perfect alignment).")

    def __str__(self):
        return f"{self.source_sentence[:50]} -> {self.target_sentence[:50]}"
    
# Synonym Model
class Synonym(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='synonyms')  # Links to the main vocabulary
    synonym_word = models.CharField(max_length=100)  # The synonym itself
    synonym_meaning = models.TextField(blank=True)  # Meaning of the synonym word
    synonym_language = models.ForeignKey(Language, on_delete=models.CASCADE)  # Language of the synonym

    def __str__(self):
        return f"Synonym of {self.vocabulary.source_word}: {self.synonym_word}"

# Antonym Model
class Antonym(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='antonyms')  # Links to the main vocabulary
    antonym_word = models.CharField(max_length=100)  # The antonym itselfantonym_word = models.CharField(max_length=100)  # The antonym itself
    antonym_meaning = models.TextField(blank=True)  # Meaning of the antonym word
    antonym_language = models.ForeignKey(Language, on_delete=models.CASCADE)  # Language of the antonym

    def __str__(self):
        return f"Antonym of {self.vocabulary.source_word}: {self.antonym_word}"

# Phrase Model (Idioms and Cultural Context)
class Phrase(models.Model):
    phrase = models.CharField(
        max_length=255, help_text="Enter the idiom or phrase in Borana (e.g., 'Biyyee nyaadhu' for 'Eat dirt')."
    )
    source_language = models.ForeignKey(Language, related_name="phrases", on_delete=models.CASCADE, help_text="Select the source language (e.g., Borana)")
    target_translation = models.TextField(
        help_text="Enter the translated idiom or phrase in English (e.g., 'Swallow your pride' for 'Biyyee nyaadhu')."
    )
    literal_translation = models.TextField(
        help_text="Provide the literal translation (e.g., 'Eat dirt' for 'Biyyee nyaadhu')."
    )
    cultural_meaning = models.TextField(
        help_text="Describe the cultural meaning of the idiom (e.g., 'Show humility' for 'Biyyee nyaadhu')."
    )
    is_idiomatic = models.BooleanField(default=False, help_text="Check this box if the phrase is an idiom.")

    def __str__(self):
        return f"Phrase: {self.phrase} ({self.source_language.name})"

 # Named Entity Model (Proper Nouns)
class NamedEntity(models.Model):
    source_language = models.ForeignKey(Language, related_name="named_entities", on_delete=models.CASCADE, help_text="Select the language of the entity name (e.g., Borana)")
    name = models.CharField(max_length=255, help_text="Enter the proper noun (e.g., 'Finfinnee' for 'Addis Ababa').")
    entity_type = models.CharField(max_length=50, help_text="Specify the type of entity (e.g., 'City', 'Organization', 'Person').")
    target_translation = models.CharField(max_length=255, null=True, blank=True, help_text="Enter the translation or equivalent name in the target language (e.g., 'Addis Ababa' for 'Finfinnee').")
    def __str__(self):
        return f"Named Entity: {self.name} ({self.entity_type})"
    
# User Feedback Model
class Feedback(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='feedback')
    user_feedback = models.TextField()
    accuracy_rating = models.IntegerField()  # Scale of 1-5
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    needs_correction = models.BooleanField(default=False)  # Flag for requiring correction
    #correct_answer
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.vocabulary.source_word} by {self.user.username}"

class SentenceAlignmentFeedback(models.Model):
    sentence_alignment = models.ForeignKey(SentenceAlignment, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField(blank=True, null=True)
    is_correct_alignment = models.BooleanField(default=True)  # Flag if alignment is incorrect
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on alignment by {self.user.username}"
'''
class Morphology(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='morphology')
    plural_form = models.CharField(max_length=100, help_text="Enter the plural form of the word, if applicable.")
    conjugated_forms = models.JSONField(help_text="Provide conjugated forms of the verb or other inflected forms (e.g., past, present, future).")
    derivational_forms = models.JSONField(null=True, blank=True, help_text="Provide derivational forms, if applicable.")
    verb_aspect = models.CharField(max_length=100, blank=True, help_text="Aspect of the verb, e.g., 'perfective', 'progressive'.")
    additional_inflections = models.JSONField(null=True, blank=True, help_text="Additional inflection rules for the word.")

    def __str__(self):
        return f"Morphology for {self.vocabulary.source_word}"

'''
# Morphology Model
class Morphology(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='morphology')
    plural_form = models.CharField(max_length=100, help_text="Enter the plural form of the word, if applicable.")
    conjugated_forms = models.JSONField(help_text="Provide conjugated forms of the verb or other inflected forms (e.g., past, present, future).")

    def __str__(self):
        return f"Morphology for {self.vocabulary.source_word}"

    
# Translation Feedback Model
class TranslationFeedback(models.Model):
    sentence_alignment = models.ForeignKey(SentenceAlignment, on_delete=models.CASCADE, related_name="feedback", help_text="Select the sentence alignment you are giving feedback on.")
    user_feedback = models.TextField(help_text="Provide feedback on the accuracy of the translation (e.g., 'The translation is correct' or 'The verb is incorrect').")
    accuracy_rating = models.IntegerField(help_text="Rate the accuracy from 1 (poor) to 5 (excellent).")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_feedback")
    correction_suggestion = models.TextField(null=True, blank=True, help_text="Provide any suggestions for correcting the translation (e.g., 'Change the verb to the past tense').")

    def __str__(self):
        return f"Feedback for: {self.sentence_alignment.source_sentence[:50]}"
    
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Moderation Model
class Moderation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moderated_contributions")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    moderator = models.ForeignKey(User, related_name="moderated_by", on_delete=models.SET_NULL, null=True)
    review_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Moderation: {self.content_object}"
      
# Translation Memory Model
class TranslationMemory(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='translation_memory')
    translation = models.CharField(max_length=255)
    source_meaning = models.TextField(blank=True)  # Meaning of the source word/phrase
    target_meaning = models.TextField(blank=True)  # Meaning of the translated word/phrase
    usage_frequency = models.IntegerField(default=1)
    confidence_score = models.FloatField(default=1.0)  # Confidence level of the translation
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Translation Memory: {self.vocabulary.source_word} -> {self.translation}"
    
# Machine Learning Training Data Model
class TrainingData(models.Model):
    sentence = models.TextField()
    translation = models.TextField()
    feedback_score = models.FloatField()
    date_used = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  # Added field for language

    def __str__(self):
        return f"Training Data: {self.sentence[:50]} -> {self.translation[:50]}"

# Translation Error Logging Model
class TranslationError(models.Model):
    original_sentence = models.TextField()
    error_description = models.TextField()
    correction = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='reported')  # Added status field
    priority_level = models.IntegerField(default=1)  # Added priority level field

    def __str__(self):
        return f"Error in: {self.original_sentence[:50]}"
    



# UserProfile Model for Gamification and Profile Data
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text="User's bio or description")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Profile picture")
    
    # Gamification-related fields
    points = models.IntegerField(default=0, help_text="Total points accumulated by the user")
    level = models.IntegerField(default=1, help_text="User's level based on activity")
    badges = models.ManyToManyField('Badge', blank=True, related_name='profiles', help_text="Special badges earned by the user")
    progress = models.OneToOneField('Progress', on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    
    def __str__(self):
        return f"Profile of {self.user.username}"

# Badge Model for User Achievements
class Badge(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the badge (e.g., 'Top Contributor')")
    description = models.TextField(help_text="Description of what the badge is awarded for")
    icon = models.ImageField(upload_to='badges/', blank=True, null=True, help_text="Icon representing the badge")

    def __str__(self):
        return self.name


# Reward Model for Tracking Points and Levels
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    points = models.IntegerField(default=0)  # Track points earned by the user
    level = models.IntegerField(default=1)  # User's level
    badge = models.CharField(max_length=100, blank=True)  # Special badges based on achievements
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.level}, Points: {self.points}, Badge: {self.badge}"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    
    # Track contributions for each model
    vocabulary_contributions = models.IntegerField(default=0, help_text="Track number of vocabulary words contributed")
    feedback_provided = models.IntegerField(default=0, help_text="Track number of feedback instances provided")
    synonyms_added = models.IntegerField(default=0, help_text="Track number of synonyms contributed")
    antonyms_added = models.IntegerField(default=0, help_text="Track number of antonyms contributed")
    phrases_contributed = models.IntegerField(default=0, help_text="Track number of phrases contributed")
    named_entities_contributed = models.IntegerField(default=0, help_text="Track number of named entities contributed")
    sentences_aligned = models.IntegerField(default=0, help_text="Track number of sentence alignments")
    grammar_structures_contributed = models.IntegerField(default=0, help_text="Track number of grammar structures contributed")
    language_structures_contributed = models.IntegerField(default=0, help_text="Track number of language structures contributed")
    translation_memory_contributions = models.IntegerField(default=0, help_text="Track number of translation memory entries")
    translation_errors_logged = models.IntegerField(default=0, help_text="Track number of translation errors logged")
    morphology_contributed = models.IntegerField(default=0, help_text="Track number of morphology contributions")
    
    # General metrics
    training_data_submitted = models.IntegerField(default=0, help_text="Track number of training data sentences submitted")
    points_earned = models.IntegerField(default=0, help_text="Track total points earned from all contributions")

    def __str__(self):
        return f"Progress for {self.user.username}"

    def add_contribution(self, contribution_type, points):
        """Update contribution count and points based on the contribution type."""
        if contribution_type == 'vocabulary':
            self.vocabulary_contributions += 1
        elif contribution_type == 'feedback':
            self.feedback_provided += 1
        elif contribution_type == 'synonym':
            self.synonyms_added += 1
        elif contribution_type == 'antonym':
            self.antonyms_added += 1
        elif contribution_type == 'phrase':
            self.phrases_contributed += 1
        elif contribution_type == 'named_entity':
            self.named_entities_contributed += 1
        elif contribution_type == 'sentence_alignment':
            self.sentences_aligned += 1
        elif contribution_type == 'grammar_structure':
            self.grammar_structures_contributed += 1
        elif contribution_type == 'language_structure':
            self.language_structures_contributed += 1
        elif contribution_type == 'translation_memory':
            self.translation_memory_contributions += 1
        elif contribution_type == 'translation_error':
            self.translation_errors_logged += 1
        elif contribution_type == 'morphology':
            self.morphology_contributed += 1
        elif contribution_type == 'training_data':
            self.training_data_submitted += 1

        self.points_earned += points  # Add points for the contribution
        self.save()



# Achievement Model for Special Milestones
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement_name = models.CharField(max_length=100, help_text="Name of the achievement (e.g., 'Top Contributor')")
    description = models.TextField(help_text="Description of the achievement (e.g., 'Contributed 100 vocabulary words')")
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Achievement: {self.achievement_name} for {self.user.username}"

# Leaderboard Model to Track Top Users
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.IntegerField()
    rank = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}, Points: {self.points}"
