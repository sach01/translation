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
@permission_classes([IsAuthenticated])
def contribute_vocabulary(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = VocabularyForm()
                vocabularies = Vocabulary.objects.all()
                return render(request, 'translation/contribute_vocabulary.html', {'form': form, 'vocabularies': vocabularies})
            else:
                vocabularies = Vocabulary.objects.all()
                serializer = VocabularySerializer(vocabularies, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = VocabularySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'vocabulary', points=10)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_vocabulary: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Grammar Structure View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_grammar_structure(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = GrammarStructureForm()
                grammar_structures = GrammarStructure.objects.all()
                return render(request, 'translation/contribute_grammar_structure.html', {'form': form, 'grammar_structures': grammar_structures})
            else:
                grammar_structures = GrammarStructure.objects.all()
                serializer = GrammarStructureSerializer(grammar_structures, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = GrammarStructureSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'grammar_structure', points=15)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_grammar_structure: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Sentence Alignment View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_sentence_alignment(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = SentenceAlignmentForm()
                alignments = SentenceAlignment.objects.all()
                return render(request, 'translation/contribute_sentence_alignment.html', {'form': form, 'alignments': alignments})
            else:
                alignments = SentenceAlignment.objects.all()
                serializer = SentenceAlignmentSerializer(alignments, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = SentenceAlignmentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'sentence_alignment', points=20)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_sentence_alignment: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Related Word View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_related_word(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = RelatedWordForm()
                related_words = RelatedWord.objects.all()
                return render(request, 'translation/contribute_related_word.html', {'form': form, 'related_words': related_words})
            else:
                related_words = RelatedWord.objects.all()
                serializer = RelatedWordSerializer(related_words, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = RelatedWordSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'related_word', points=5)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_related_word: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Phrase View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_phrase(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = PhraseForm()
                phrases = Phrase.objects.all()
                return render(request, 'translation/contribute_phrase.html', {'form': form, 'phrases': phrases})
            else:
                phrases = Phrase.objects.all()
                serializer = PhraseSerializer(phrases, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = PhraseSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'phrase', points=10)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_phrase: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Named Entity View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_named_entity(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = NamedEntityForm()
                named_entities = NamedEntity.objects.all()
                return render(request, 'translation/contribute_named_entity.html', {'form': form, 'named_entities': named_entities})
            else:
                named_entities = NamedEntity.objects.all()
                serializer = NamedEntitySerializer(named_entities, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = NamedEntitySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'named_entity', points=8)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_named_entity: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Feedback View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_feedback(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = FeedbackForm()
                feedbacks = Feedback.objects.all()
                return render(request, 'translation/contribute_feedback.html', {'form': form, 'feedbacks': feedbacks})
            else:
                feedbacks = Feedback.objects.all()
                serializer = FeedbackSerializer(feedbacks, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = FeedbackSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'feedback', points=5)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_feedback: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Morphology View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_morphology(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = MorphologyForm()
                morphologies = Morphology.objects.all()
                return render(request, 'translation/contribute_morphology.html', {'form': form, 'morphologies': morphologies})
            else:
                morphologies = Morphology.objects.all()
                serializer = MorphologySerializer(morphologies, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = MorphologySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'morphology', points=6)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_morphology: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Translation Memory View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_translation_memory(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = TranslationMemoryForm()
                translation_memories = TranslationMemory.objects.all()
                return render(request, 'translation/contribute_translation_memory.html', {'form': form, 'translation_memories': translation_memories})
            else:
                translation_memories = TranslationMemory.objects.all()
                serializer = TranslationMemorySerializer(translation_memories, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = TranslationMemorySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'translation_memory', points=12)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_translation_memory: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Training Data View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_training_data(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = TrainingDataForm()
                training_data_list = TrainingData.objects.all()
                return render(request, 'translation/contribute_training_data.html', {'form': form, 'training_data_list': training_data_list})
            else:
                training_data_list = TrainingData.objects.all()
                serializer = TrainingDataSerializer(training_data_list, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = TrainingDataSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'training_data', points=10)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_training_data: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Translation Error View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_translation_error(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = TranslationErrorForm()
                errors = TranslationError.objects.all()
                return render(request, 'translation/contribute_translation_error.html', {'form': form, 'errors': errors})
            else:
                errors = TranslationError.objects.all()
                serializer = TranslationErrorSerializer(errors, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = TranslationErrorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(reported_by=request.user)
                    reward_user(request.user, 'translation_error', points=7)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_translation_error: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Numbers View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contribute_number(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = NumbersForm()
                numbers = Numbers.objects.all()
                return render(request, 'translation/contribute_number.html', {'form': form, 'numbers': numbers})
            else:
                numbers = Numbers.objects.all()
                serializer = NumbersSerializer(numbers, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
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

            else:
                serializer = NumbersSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    reward_user(request.user, 'number', points=5)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in contribute_number: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Moderation View (For Admins)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def moderate_content(request):
    try:
        if request.method == 'GET':
            if request.accepted_renderer.format == 'html':
                form = ModerationForm()
                moderations = Moderation.objects.all()
                return render(request, 'translation/moderate_content.html', {'form': form, 'moderations': moderations})
            else:
                moderations = Moderation.objects.all()
                serializer = ModerationSerializer(moderations, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            if request.accepted_renderer.format == 'html':
                form = ModerationForm(request.POST)
                if form.is_valid():
                    moderation = form.save(commit=False)
                    moderation.moderator = request.user
                    moderation.save()
                    messages.success(request, 'Content moderated successfully!')
                    return redirect('moderate_content')
                else:
                    return handle_form_error(form, 'translation/moderate_content.html', request)

            else:
                serializer = ModerationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(moderator=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return handle_serializer_error(serializer)

    except Exception as e:
        print(f"Error in moderate_content: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Progress View
@login_required
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
