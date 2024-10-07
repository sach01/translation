from django.urls import path
from .views import (
    contribute_vocabulary,
    contribute_grammar_structure,
    contribute_sentence_alignment,
    contribute_related_word,
    contribute_phrase,
    contribute_named_entity,
    contribute_feedback,
    contribute_morphology,
    contribute_translation_memory,
    contribute_training_data,
    contribute_translation_error,
    contribute_number,
    contribute_moderation,
    user_progress_view,
    leaderboard_view
)

urlpatterns = [
    # Vocabulary
    path('vocabulary/', contribute_vocabulary, name='contribute_vocabulary'),

    # Grammar Structure
    path('grammar_structure/', contribute_grammar_structure, name='contribute_grammar_structure'),

    # Sentence Alignment
    path('sentence_alignment/', contribute_sentence_alignment, name='contribute_sentence_alignment'),

    # Related Word
    path('related_word/', contribute_related_word, name='contribute_related_word'),

    # Phrase
    path('phrase/', contribute_phrase, name='contribute_phrase'),

    # Named Entity
    path('named_entity/', contribute_named_entity, name='contribute_named_entity'),

    # Feedback
    path('feedback/', contribute_feedback, name='contribute_feedback'),

    # Morphology
    path('morphology/', contribute_morphology, name='contribute_morphology'),

    # Translation Memory
    path('translation_memory/', contribute_translation_memory, name='contribute_translation_memory'),

    # Training Data
    path('training_data/', contribute_training_data, name='contribute_training_data'),

    # Translation Error
    path('translation_error/', contribute_translation_error, name='contribute_translation_error'),

    # Numbers
    path('numbers/', contribute_number, name='contribute_number'),

    # Moderation
    path('moderate/', contribute_moderation, name='contribute_moderation'),

    # User Progress
    path('progress/', user_progress_view, name='user_progress'),

    # Leaderboard
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]
