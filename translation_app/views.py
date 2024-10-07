from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .forms import (
    VocabularyForm, GrammarStructureForm, SentenceAlignmentForm, 
    RelatedWordForm, PhraseForm, NamedEntityForm, FeedbackForm, 
    MorphologyForm, TranslationMemoryForm, TrainingDataForm, 
    TranslationErrorForm, ModerationForm, NumbersForm
)
from .models import (
    Vocabulary, GrammarStructure, SentenceAlignment, RelatedWord, 
    Phrase, NamedEntity, Feedback, Morphology, TranslationMemory, 
    TrainingData, TranslationError, Moderation, Numbers, Progress, 
    UserProfile, Badge
)
from .serializers import (
    VocabularySerializer, GrammarStructureSerializer, SentenceAlignmentSerializer, 
    RelatedWordSerializer, PhraseSerializer, NamedEntitySerializer, FeedbackSerializer, 
    MorphologySerializer, TranslationMemorySerializer, TrainingDataSerializer, 
    TranslationErrorSerializer, ModerationSerializer, NumbersSerializer
)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserForm

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Automatically log in the user
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to home or another page
        else:
            messages.error(request, 'There was an error in the registration form.')

    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .forms import (
    VocabularyForm, GrammarStructureForm, SentenceAlignmentForm,
    RelatedWordForm, PhraseForm, NamedEntityForm, FeedbackForm,
    MorphologyForm, TranslationMemoryForm, TrainingDataForm,
    TranslationErrorForm, ModerationForm, NumbersForm
)
from .models import (
    Vocabulary, GrammarStructure, SentenceAlignment, RelatedWord,
    Phrase, NamedEntity, Feedback, Morphology, TranslationMemory,
    TrainingData, TranslationError, Moderation, Numbers
)
from .serializers import (
    VocabularySerializer, GrammarStructureSerializer, SentenceAlignmentSerializer,
    RelatedWordSerializer, PhraseSerializer, NamedEntitySerializer, FeedbackSerializer,
    MorphologySerializer, TranslationMemorySerializer, TrainingDataSerializer,
    TranslationErrorSerializer, ModerationSerializer, NumbersSerializer
)

def reward_user(user, contribution_type, points=10):
    """Reward user with points for their contribution."""
    try:
        user_profile = user.profile
        progress = user_profile.progress
        progress.add_contribution(contribution_type, points)
        user_profile.points += points
        user_profile.save()
        progress.save()
    except Exception as e:
        print(f"Error rewarding user: {e}")
        raise

def handle_form_error(form, template, request):
    """Handle form errors for web rendering."""
    for field, errors in form.errors.items():
        messages.error(request, f"{field}: {errors[0]}")
    return render(request, template, {'form': form})

def handle_serializer_error(serializer):
    """Handle serializer errors for API responses."""
    error_messages = {field: ', '.join(errors) for field, errors in serializer.errors.items()}
    return Response({"errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)

# Vocabulary View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_vocabulary(request):
    if request.method == 'GET':
        form = VocabularyForm()
        return render(request, 'translation/contribute_vocabulary.html', {'form': form})

    elif request.method == 'POST':
        form = VocabularyForm(request.POST, request.FILES)
        if form.is_valid():
            vocabulary = form.save(commit=False)
            vocabulary.user = request.user
            vocabulary.save()
            reward_user(request.user, 'vocabulary', points=10)
            messages.success(request, 'Vocabulary added successfully!')
            return redirect('contribute_vocabulary')
        else:
            return handle_form_error(form, 'translation/contribute_vocabulary.html', request)

    serializer = VocabularySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'vocabulary', points=10)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Grammar Structure View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_grammar_structure(request):
    if request.method == 'GET':
        form = GrammarStructureForm()
        return render(request, 'translation/contribute_grammar_structure.html', {'form': form})

    elif request.method == 'POST':
        form = GrammarStructureForm(request.POST)
        if form.is_valid():
            grammar_structure = form.save(commit=False)
            grammar_structure.user = request.user
            grammar_structure.save()
            reward_user(request.user, 'grammar_structure', points=15)
            messages.success(request, 'Grammar structure added successfully!')
            return redirect('contribute_grammar_structure')
        else:
            return handle_form_error(form, 'translation/contribute_grammar_structure.html', request)

    serializer = GrammarStructureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'grammar_structure', points=15)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Sentence Alignment View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_sentence_alignment(request):
    if request.method == 'GET':
        form = SentenceAlignmentForm()
        return render(request, 'translation/contribute_sentence_alignment.html', {'form': form})

    elif request.method == 'POST':
        form = SentenceAlignmentForm(request.POST)
        if form.is_valid():
            alignment = form.save(commit=False)
            alignment.user = request.user
            alignment.save()
            reward_user(request.user, 'sentence_alignment', points=20)
            messages.success(request, 'Sentence alignment added successfully!')
            return redirect('contribute_sentence_alignment')
        else:
            return handle_form_error(form, 'translation/contribute_sentence_alignment.html', request)

    serializer = SentenceAlignmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'sentence_alignment', points=20)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Related Word View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_related_word(request):
    if request.method == 'GET':
        form = RelatedWordForm()
        return render(request, 'translation/contribute_related_word.html', {'form': form})

    elif request.method == 'POST':
        form = RelatedWordForm(request.POST)
        if form.is_valid():
            related_word = form.save(commit=False)
            related_word.user = request.user
            related_word.save()
            reward_user(request.user, 'related_word', points=5)
            messages.success(request, 'Related word added successfully!')
            return redirect('contribute_related_word')
        else:
            return handle_form_error(form, 'translation/contribute_related_word.html', request)

    serializer = RelatedWordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'related_word', points=5)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Phrase View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_phrase(request):
    if request.method == 'GET':
        form = PhraseForm()
        return render(request, 'translation/contribute_phrase.html', {'form': form})

    elif request.method == 'POST':
        form = PhraseForm(request.POST)
        if form.is_valid():
            phrase = form.save(commit=False)
            phrase.user = request.user
            phrase.save()
            reward_user(request.user, 'phrase', points=10)
            messages.success(request, 'Phrase added successfully!')
            return redirect('contribute_phrase')
        else:
            return handle_form_error(form, 'translation/contribute_phrase.html', request)

    serializer = PhraseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'phrase', points=10)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Named Entity View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_named_entity(request):
    if request.method == 'GET':
        form = NamedEntityForm()
        return render(request, 'translation/contribute_named_entity.html', {'form': form})

    elif request.method == 'POST':
        form = NamedEntityForm(request.POST)
        if form.is_valid():
            named_entity = form.save(commit=False)
            named_entity.user = request.user
            named_entity.save()
            reward_user(request.user, 'named_entity', points=8)
            messages.success(request, 'Named entity added successfully!')
            return redirect('contribute_named_entity')
        else:
            return handle_form_error(form, 'translation/contribute_named_entity.html', request)

    serializer = NamedEntitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'named_entity', points=8)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Feedback View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_feedback(request):
    if request.method == 'GET':
        form = FeedbackForm()
        return render(request, 'translation/contribute_feedback.html', {'form': form})

    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            reward_user(request.user, 'feedback', points=5)
            messages.success(request, 'Feedback added successfully!')
            return redirect('contribute_feedback')
        else:
            return handle_form_error(form, 'translation/contribute_feedback.html', request)

    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'feedback', points=5)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Morphology View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_morphology(request):
    if request.method == 'GET':
        form = MorphologyForm()
        return render(request, 'translation/contribute_morphology.html', {'form': form})

    elif request.method == 'POST':
        form = MorphologyForm(request.POST)
        if form.is_valid():
            morphology = form.save(commit=False)
            morphology.user = request.user
            morphology.save()
            reward_user(request.user, 'morphology', points=6)
            messages.success(request, 'Morphology added successfully!')
            return redirect('contribute_morphology')
        else:
            return handle_form_error(form, 'translation/contribute_morphology.html', request)

    serializer = MorphologySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'morphology', points=6)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Translation Memory View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_translation_memory(request):
    if request.method == 'GET':
        form = TranslationMemoryForm()
        return render(request, 'translation/contribute_translation_memory.html', {'form': form})

    elif request.method == 'POST':
        form = TranslationMemoryForm(request.POST)
        if form.is_valid():
            translation_memory = form.save(commit=False)
            translation_memory.user = request.user
            translation_memory.save()
            reward_user(request.user, 'translation_memory', points=12)
            messages.success(request, 'Translation memory added successfully!')
            return redirect('contribute_translation_memory')
        else:
            return handle_form_error(form, 'translation/contribute_translation_memory.html', request)

    serializer = TranslationMemorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'translation_memory', points=12)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Training Data View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_training_data(request):
    if request.method == 'GET':
        form = TrainingDataForm()
        return render(request, 'translation/contribute_training_data.html', {'form': form})

    elif request.method == 'POST':
        form = TrainingDataForm(request.POST)
        if form.is_valid():
            training_data = form.save(commit=False)
            training_data.user = request.user
            training_data.save()
            reward_user(request.user, 'training_data', points=10)
            messages.success(request, 'Training data added successfully!')
            return redirect('contribute_training_data')
        else:
            return handle_form_error(form, 'translation/contribute_training_data.html', request)

    serializer = TrainingDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'training_data', points=10)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Translation Error View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_translation_error(request):
    if request.method == 'GET':
        form = TranslationErrorForm()
        return render(request, 'translation/contribute_translation_error.html', {'form': form})

    elif request.method == 'POST':
        form = TranslationErrorForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.reported_by = request.user
            error.save()
            reward_user(request.user, 'translation_error', points=7)
            messages.success(request, 'Translation error reported successfully!')
            return redirect('contribute_translation_error')
        else:
            return handle_form_error(form, 'translation/contribute_translation_error.html', request)

    serializer = TranslationErrorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(reported_by=request.user)
        reward_user(request.user, 'translation_error', points=7)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Numbers View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_number(request):
    if request.method == 'GET':
        form = NumbersForm()
        return render(request, 'translation/contribute_number.html', {'form': form})

    elif request.method == 'POST':
        form = NumbersForm(request.POST)
        if form.is_valid():
            number = form.save(commit=False)
            number.user = request.user
            number.save()
            reward_user(request.user, 'number', points=5)
            messages.success(request, 'Number added successfully!')
            return redirect('contribute_number')
        else:
            return handle_form_error(form, 'translation/contribute_number.html', request)

    serializer = NumbersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        reward_user(request.user, 'number', points=5)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)

# Moderation View
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def contribute_moderation(request):
    if request.method == 'GET':
        form = ModerationForm()
        return render(request, 'translation/moderate_content.html', {'form': form})

    elif request.method == 'POST':
        form = ModerationForm(request.POST)
        if form.is_valid():
            moderation = form.save(commit=False)
            moderation.moderator = request.user
            moderation.save()
            messages.success(request, 'Content moderated successfully!')
            return redirect('contribute_moderation')
        else:
            return handle_form_error(form, 'translation/contribute_moderation.html', request)

    serializer = ModerationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(moderator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return handle_serializer_error(serializer)


def user_progress_view(request):
    try:
        progress = Progress.objects.get(user=request.user)
        return render(request, 'translation/user_progress.html', {'progress': progress})
    except Progress.DoesNotExist:
        messages.error(request, "Progress not found.")
        return redirect('some_default_view')

# Leaderboard View
def leaderboard_view(request):
    users = UserProfile.objects.order_by('-points')[:10]
    return render(request, 'translation/leaderboard.html', {'users': users})