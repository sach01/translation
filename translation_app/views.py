from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    UserProfile, Progress, Vocabulary, Feedback, Synonym, Antonym, Phrase,
    NamedEntity, SentenceAlignment, GrammarStructure, LanguageStructure, 
    TranslationMemory, TranslationError, Morphology
)
from .forms import (
    VocabularyForm, FeedbackForm, SynonymForm, AntonymForm, PhraseForm,
    NamedEntityForm, SentenceAlignmentForm, GrammarStructureForm,
    LanguageStructureForm, TranslationMemoryForm, TranslationErrorForm, 
    MorphologyForm
)

def test_template(request):
    return render(request, 'translation/test_template.html')

# Vocabulary Contribution View
#@login_required
def contribute_vocabulary(request):
    if request.method == 'POST':
        form = VocabularyForm(request.POST, request.FILES)
        if form.is_valid():
            vocabulary = form.save(commit=False)
            vocabulary.user = request.user
            vocabulary.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('vocabulary', points=10)
            user_profile.add_points(10)

            return redirect('leaderboard')
    else:
        form = VocabularyForm()
    return render(request, 'translation/contribute_vocabulary.html', {'form': form})

# Feedback Submission View
#@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('feedback', points=5)
            user_profile.add_points(5)

            return redirect('leaderboard')
    else:
        form = FeedbackForm()
    return render(request, 'translation/submit_feedback.html', {'form': form})

# Synonym Contribution View
#@login_required
def contribute_synonym(request):
    if request.method == 'POST':
        form = SynonymForm(request.POST)
        if form.is_valid():
            synonym = form.save(commit=False)
            synonym.user = request.user
            synonym.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('synonym', points=4)
            user_profile.add_points(4)

            return redirect('leaderboard')
    else:
        form = SynonymForm()
    return render(request, 'translation/contribute_synonym.html', {'form': form})

# Antonym Contribution View
#@login_required
def contribute_antonym(request):
    if request.method == 'POST':
        form = AntonymForm(request.POST)
        if form.is_valid():
            antonym = form.save(commit=False)
            antonym.user = request.user
            antonym.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('antonym', points=4)
            user_profile.add_points(4)

            return redirect('leaderboard')
    else:
        form = AntonymForm()
    return render(request, 'translation/contribute_antonym.html', {'form': form})

# Phrase Contribution View
#@login_required
def contribute_phrase(request):
    if request.method == 'POST':
        form = PhraseForm(request.POST)
        if form.is_valid():
            phrase = form.save(commit=False)
            phrase.user = request.user
            phrase.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('phrase', points=6)
            user_profile.add_points(6)

            return redirect('leaderboard')
    else:
        form = PhraseForm()
    return render(request, 'translation/contribute_phrase.html', {'form': form})

# Named Entity Contribution View
#@login_required
def contribute_named_entity(request):
    if request.method == 'POST':
        form = NamedEntityForm(request.POST)
        if form.is_valid():
            named_entity = form.save(commit=False)
            named_entity.user = request.user
            named_entity.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('named_entity', points=8)
            user_profile.add_points(8)

            return redirect('leaderboard')
    else:
        form = NamedEntityForm()
    return render(request, 'translation/contribute_named_entity.html', {'form': form})

# Sentence Alignment View
#@login_required
def align_sentence(request):
    if request.method == 'POST':
        form = SentenceAlignmentForm(request.POST)
        if form.is_valid():
            alignment = form.save(commit=False)
            alignment.user = request.user
            alignment.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('sentence_alignment', points=8)
            user_profile.add_points(8)

            return redirect('leaderboard')
    else:
        form = SentenceAlignmentForm()
    return render(request, 'translation/align_sentence.html', {'form': form})

# Grammar Structure Contribution View
#@login_required
def contribute_grammar_structure(request):
    if request.method == 'POST':
        form = GrammarStructureForm(request.POST)
        if form.is_valid():
            grammar_structure = form.save(commit=False)
            grammar_structure.user = request.user
            grammar_structure.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('grammar_structure', points=7)
            user_profile.add_points(7)

            return redirect('leaderboard')
    else:
        form = GrammarStructureForm()
    return render(request, 'translation/contribute_grammar_structure.html', {'form': form})

# Language Structure Contribution View
#@login_required
def contribute_language_structure(request):
    if request.method == 'POST':
        form = LanguageStructureForm(request.POST)
        if form.is_valid():
            language_structure = form.save(commit=False)
            language_structure.user = request.user
            language_structure.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('language_structure', points=7)
            user_profile.add_points(7)

            return redirect('leaderboard')
    else:
        form = LanguageStructureForm()
    return render(request, 'translation/contribute_language_structure.html', {'form': form})

# Translation Memory Contribution View
#@login_required
def contribute_translation_memory(request):
    if request.method == 'POST':
        form = TranslationMemoryForm(request.POST)
        if form.is_valid():
            translation_memory = form.save(commit=False)
            translation_memory.user = request.user
            translation_memory.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('translation_memory', points=5)
            user_profile.add_points(5)

            return redirect('leaderboard')
    else:
        form = TranslationMemoryForm()
    return render(request, 'translation/contribute_translation_memory.html', {'form': form})

# Translation Error Logging View
#@login_required
def log_translation_error(request):
    if request.method == 'POST':
        form = TranslationErrorForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.user = request.user
            error.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('translation_error', points=6)
            user_profile.add_points(6)

            return redirect('leaderboard')
    else:
        form = TranslationErrorForm()
    return render(request, 'translation/log_translation_error.html', {'form': form})

# Morphology Contribution View
#@login_required
def contribute_morphology(request):
    if request.method == 'POST':
        form = MorphologyForm(request.POST)
        if form.is_valid():
            morphology = form.save(commit=False)
            morphology.user = request.user
            morphology.save()

            # Update Progress and UserProfile points
            user_profile = request.user.profile
            progress = user_profile.progress
            progress.add_contribution('morphology', points=7)
            user_profile.add_points(7)

            return redirect('leaderboard')
    else:
        form = MorphologyForm()
    return render(request, 'translation/contribute_morphology.html', {'form': form})

# Leaderboard View
#@login_required
def leaderboard(request):
    user_profiles = UserProfile.objects.order_by('-points')[:10]  # Top 10 users by points
    return render(request, 'translation/leaderboard.html', {'user_profiles': user_profiles})
