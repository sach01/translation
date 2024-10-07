from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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


# Language Model for numbers
class Numbers(models.Model):
    number = models.IntegerField()
    in_borana = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

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
        return f"{self.language.name} - {self.name} - {self.region}"


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

    part_of_speech = models.ForeignKey(PartOfSpeech, on_delete=models.CASCADE, related_name='vocabularies')
    phonetic_translation = models.CharField(max_length=100)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

    def __str__(self):
        return self.source_word


class GrammarStructure(models.Model):
    source_language = models.ForeignKey(Language, related_name="source_grammar", on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language, related_name="target_grammar", on_delete=models.CASCADE)
    
    # Ensure these fields are correctly defined
    rule_name = models.CharField(max_length=255)  # Add this line if not present
    source_sentence = models.TextField()
    target_sentence = models.TextField()
    
    grammatical_structure = models.CharField(max_length=100)
    grammar_type = models.CharField(max_length=50, choices=[
        ('Simple', 'Simple'), 
        ('Conditional', 'Conditional'), 
        ('Passive', 'Passive'), 
        ('Complex', 'Complex')
    ])
    level = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'), 
        ('Intermediate', 'Intermediate'), 
        ('Advanced', 'Advanced')
    ])
    tense = models.CharField(max_length=50, null=True, blank=True)
    pronouns_used = models.CharField(max_length=100, null=True, blank=True)
    negation = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the grammar structure

    def __str__(self):
        return f"{self.source_sentence[:50]} -> {self.target_sentence[:50]}"



# Sentence Alignment Model (Parallel Corpus)
class SentenceAlignment(models.Model):
    source_language = models.ForeignKey(Language, related_name="source_sentences", on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language, related_name="target_sentences", on_delete=models.CASCADE)
    source_corpus = models.CharField(max_length=100, null=True, blank=True)
    source_sentence = models.TextField()
    target_sentence = models.TextField()
    target_corpus = models.CharField(max_length=100, null=True, blank=True)
    alignment_score = models.FloatField(default=1.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

    def __str__(self):
        return f"{self.source_sentence[:50]} -> {self.target_sentence[:50]}"


# Related Word Model (Antonyms and Synonyms)
class RelatedWord(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='related_words')
    synonym_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    relationship_type = models.CharField(max_length=10, choices=[('synonym', 'Synonym'), ('antonym', 'Antonym')])
    meaning = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

    def __str__(self):
        return f"Related word for {self.vocabulary.source_word}"


# Phrase Model (Idioms and Cultural Context)
class Phrase(models.Model):
    phrase = models.CharField(max_length=255)
    source_language = models.ForeignKey(Language, related_name="phrases", on_delete=models.CASCADE)
    target_translation = models.TextField()
    literal_translation = models.TextField()
    cultural_meaning = models.TextField()
    phrase_type = models.CharField(max_length=50, choices=[('Common Phrase', 'Common Phrase'), ('Idiom', 'Idiom'), ('Proverb', 'Proverb')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

    def __str__(self):
        return f"Phrase: {self.phrase} ({self.source_language.name})"


# Named Entity Model (Proper Nouns)
class NamedEntity(models.Model):
    source_language = models.ForeignKey(Language, related_name="named_entities", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50)
    target_translation = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

    def __str__(self):
        return f"Named Entity: {self.name} ({self.entity_type})"


# User Feedback Model
class Feedback(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='feedback')
    user_feedback = models.TextField()
    accuracy_rating = models.IntegerField()  # Scale of 1-5
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    needs_correction = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.vocabulary.source_word} by {self.user.username}"


# Morphology Model
class Morphology(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='morphology')
    base_form = models.CharField(max_length=100)
    past_form = models.CharField(max_length=100, blank=True)
    future_form = models.CharField(max_length=100, blank=True)
    plural_form = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user

    def __str__(self):
        return f"Morphology for {self.vocabulary.source_word}"


# Translation Memory Model
class TranslationMemory(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='translation_memory')
    translation = models.CharField(max_length=255)
    source_meaning = models.TextField(blank=True)
    target_meaning = models.TextField(blank=True)
    usage_frequency = models.IntegerField(default=1)
    confidence_score = models.FloatField(default=1.0)
    last_used = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user

    def __str__(self):
        return f"Translation Memory: {self.vocabulary.source_word} -> {self.translation}"

# Machine Learning Training Data Model
class TrainingData(models.Model):
    sentence = models.TextField()
    translation = models.TextField()
    feedback_score = models.FloatField()
    date_used = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"Training Data: {self.sentence[:50]} -> {self.translation[:50]}"


# Translation Error Logging Model
class TranslationError(models.Model):
    original_sentence = models.TextField()
    error_description = models.TextField()
    correction = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='reported')
    priority_level = models.IntegerField(default=1)

    def __str__(self):
        return f"Error in: {self.original_sentence[:50]}"


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
    
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track the user who added the named entity

    def __str__(self):
        return f"Moderation: {self.content_object}"


# UserProfile Model for Gamification and Profile Data
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Gamification-related fields
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.ManyToManyField('Badge', blank=True, related_name='profiles')
    progress = models.OneToOneField('Progress', on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    
    def __str__(self):
        return f"Profile of {self.user.username}"


# Badge Model for User Achievements
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)

    def __str__(self):
        return self.name


# Reward Model for Tracking Points and Levels
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badge = models.CharField(max_length=100, blank=True)
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.level}, Points: {self.points}, Badge: {self.badge}"


# Progress Model for Gamification
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')

    # Tracking contributions for different models
    vocabulary_contributions = models.IntegerField(default=0)
    feedback_provided = models.IntegerField(default=0)
    synonyms_added = models.IntegerField(default=0)
    antonyms_added = models.IntegerField(default=0)
    phrases_contributed = models.IntegerField(default=0)
    named_entities_contributed = models.IntegerField(default=0)
    sentences_aligned = models.IntegerField(default=0)
    grammar_structures_contributed = models.IntegerField(default=0)
    language_structures_contributed = models.IntegerField(default=0)
    translation_memory_contributions = models.IntegerField(default=0)
    translation_errors_logged = models.IntegerField(default=0)
    morphology_contributed = models.IntegerField(default=0)

    # General metrics
    training_data_submitted = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)

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

        self.points_earned += points
        self.save()


# Achievement Model
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement_name = models.CharField(max_length=100)
    description = models.TextField()
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Achievement: {self.achievement_name} for {self.user.username}"


# Leaderboard Model
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.IntegerField()
    rank = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}, Points: {self.points}"
