from django.shortcuts import render, redirect
from django.http import HttpResponse


from django.shortcuts import render, redirect
from .models import Book, Chapter, Verse, ParallelVerse, Language
import re

def extract_chapter_and_verse(line):
    """
    Tries to extract chapter and verse information from the line using different patterns.
    If it finds a chapter header, it returns the chapter number and resets the verse number.
    """
    # Try matching a format like 'Chapter 1'
    chapter_match = re.match(r'Chapter\s+(\d+)', line, re.IGNORECASE)
    if chapter_match:
        chapter_number = int(chapter_match.group(1))
        return chapter_number, None
    
    # Otherwise, return None for chapter and expect a verse
    return None, line

def upload_parallel_text(request):
    if request.method == 'POST':
        borana_title = request.POST.get('borana_title')
        english_title = request.POST.get('english_title')
        borana_text = request.POST.get('borana_text')
        english_text = request.POST.get('english_text')

        if not (borana_title and english_title and borana_text and english_text):
            return render(request, 'upload.html', {'error': 'All fields are required.'})

        # Get or create the languages
        borana_language, _ = Language.objects.get_or_create(name="Borana", code="bor")
        english_language, _ = Language.objects.get_or_create(name="English", code="eng")

        # Get or create the books
        borana_book, _ = Book.objects.get_or_create(title=borana_title, language=borana_language)
        english_book, _ = Book.objects.get_or_create(title=english_title, language=english_language)

        # Split the texts by line
        borana_lines = borana_text.strip().split('\n')
        english_lines = english_text.strip().split('\n')

        current_borana_chapter = None
        current_english_chapter = None

        # Initialize verse number
        verse_number = 1

        # Iterate through the lines
        for borana_line, english_line in zip(borana_lines, english_lines):
            # Extract chapters and verses for both languages
            borana_chapter, borana_content = extract_chapter_and_verse(borana_line)
            english_chapter, english_content = extract_chapter_and_verse(english_line)

            if borana_chapter is not None and english_chapter is not None:
                # If chapter headers are found, reset the verse number and create new chapters
                current_borana_chapter, _ = Chapter.objects.get_or_create(book=borana_book, chapter_number=borana_chapter)
                current_english_chapter, _ = Chapter.objects.get_or_create(book=english_book, chapter_number=english_chapter)
                verse_number = 1
            else:
                # If no chapter header, it's a verse
                if current_borana_chapter is None or current_english_chapter is None:
                    return render(request, 'upload.html', {'error': 'Chapter headers missing or incorrect.'})

                # Create the verses and link them
                borana_verse = Verse.objects.create(
                    chapter=current_borana_chapter,
                    verse_number=verse_number,
                    content=borana_content.strip()
                )
                english_verse = Verse.objects.create(
                    chapter=current_english_chapter,
                    verse_number=verse_number,
                    content=english_content.strip()
                )

                # Create ParallelVerse to link the Borana and English verses
                ParallelVerse.objects.create(
                    borana_verse=borana_verse,
                    english_verse=english_verse
                )

                # Increment verse number for the next line
                verse_number += 1

        return redirect('view_parallel_text')

    return render(request, 'upload.html')

def view_parallel_text(request):
    parallel_verses = ParallelVerse.objects.all().select_related(
        'borana_verse__chapter__book', 'english_verse__chapter__book'
    ).order_by(
        'borana_verse__chapter__chapter_number', 'borana_verse__verse_number'
    )

    context = {
        'parallel_verses': parallel_verses,
    }
    return render(request, 'view.html', context)

'''
def upload_parallel_text(request):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        borana_text = request.POST.get('borana_text')
        english_text = request.POST.get('english_text')

        if not (book_title and borana_text and english_text):
            return render(request, 'upload.html', {'error': 'All fields are required.'})

        # Get or create the languages
        borana_language, _ = Language.objects.get_or_create(name="Borana", code="bor")
        english_language, _ = Language.objects.get_or_create(name="English", code="eng")

        # Get or create the books
        borana_book, _ = Book.objects.get_or_create(title=book_title, language=borana_language)
        english_book, _ = Book.objects.get_or_create(title=book_title, language=english_language)

        # Split the texts by line
        borana_lines = borana_text.strip().split('\n')
        english_lines = english_text.strip().split('\n')

        current_borana_chapter = None
        current_english_chapter = None

        # Iterate through the lines
        for borana_line, english_line in zip(borana_lines, english_lines):
            # Check for chapter headers
            if borana_line.startswith("Chapter") and english_line.startswith("Chapter"):
                try:
                    chapter_number = int(borana_line.split()[1])
                except ValueError:
                    return render(request, 'upload.html', {'error': 'Invalid chapter number.'})

                # Get or create chapters
                current_borana_chapter, _ = Chapter.objects.get_or_create(book=borana_book, chapter_number=chapter_number)
                current_english_chapter, _ = Chapter.objects.get_or_create(book=english_book, chapter_number=chapter_number)
            else:
                # Assume lines are verses
                if current_borana_chapter is None or current_english_chapter is None:
                    return render(request, 'upload.html', {'error': 'Chapter headers missing or incorrect.'})

                verse_number = len(Verse.objects.filter(chapter=current_borana_chapter)) + 1

                # Create verses
                borana_verse = Verse.objects.create(
                    chapter=current_borana_chapter,
                    verse_number=verse_number,
                    content=borana_line.strip()
                )
                english_verse = Verse.objects.create(
                    chapter=current_english_chapter,
                    verse_number=verse_number,
                    content=english_line.strip()
                )

                # Create ParallelVerse
                ParallelVerse.objects.create(
                    borana_verse=borana_verse,
                    english_verse=english_verse
                )

        return redirect('view_parallel_text')

    return render(request, 'upload.html')

def view_parallel_text(request):
    parallel_verses = ParallelVerse.objects.all().select_related(
        'borana_verse__chapter__book', 'english_verse__chapter__book'
    ).order_by(
        'borana_verse__chapter__chapter_number', 'borana_verse__verse_number'
    )

    context = {
        'parallel_verses': parallel_verses,
    }
    return render(request, 'view.html', context)
'''