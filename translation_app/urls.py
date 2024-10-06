from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test_template, name='test_template'),
    path('contribute/vocabulary/', views.contribute_vocabulary, name='contribute_vocabulary'),
    path('submit/feedback/', views.submit_feedback, name='submit_feedback'),
    path('contribute/synonym/', views.contribute_synonym, name='contribute_synonym'),
    path('contribute/antonym/', views.contribute_antonym, name='contribute_antonym'),
    path('contribute/phrase/', views.contribute_phrase, name='contribute_phrase'),
    path('contribute/named-entity/', views.contribute_named_entity, name='contribute_named_entity'),
    path('align/sentence/', views.align_sentence, name='align_sentence'),
    path('contribute/grammar-structure/', views.contribute_grammar_structure, name='contribute_grammar_structure'),
    path('contribute/language-structure/', views.contribute_language_structure, name='contribute_language_structure'),
    path('contribute/translation-memory/', views.contribute_translation_memory, name='contribute_translation_memory'),
    path('log/translation-error/', views.log_translation_error, name='log_translation_error'),
    path('contribute/morphology/', views.contribute_morphology, name='contribute_morphology'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
