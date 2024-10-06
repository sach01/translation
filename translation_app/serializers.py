from rest_framework import serializers
from .models import Language, Book, Chapter, Verse, ParallelVerse

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = '__all__'

class ParallelVerseSerializer(serializers.ModelSerializer):
    borana_content = serializers.CharField(write_only=True)
    english_content = serializers.CharField(write_only=True)

    class Meta:
        model = ParallelVerse
        fields = ['borana_content', 'english_content']

    def create(self, validated_data):
        # Fetch the respective languages
        borana_language = Language.objects.get(name="Borana")
        english_language = Language.objects.get(name="English")

        # Get or create books and chapters for both languages
        borana_book, _ = Book.objects.get_or_create(title="Yohana", language=borana_language)
        english_book, _ = Book.objects.get_or_create(title="John", language=english_language)

        # Get or create chapter (assuming chapter 1 for simplicity)
        chapter_number = 1
        borana_chapter, _ = Chapter.objects.get_or_create(book=borana_book, chapter_number=chapter_number)
        english_chapter, _ = Chapter.objects.get_or_create(book=english_book, chapter_number=chapter_number)

        # Create verses for both Borana and English
        borana_verse = Verse.objects.create(
            chapter=borana_chapter,
            verse_number=self.context['verse_number'],
            content=validated_data['borana_content']
        )
        english_verse = Verse.objects.create(
            chapter=english_chapter,
            verse_number=self.context['verse_number'],
            content=validated_data['english_content']
        )

        # Create and return the parallel verse linking Borana and English
        parallel_verse = ParallelVerse.objects.create(
            borana_verse=borana_verse,
            english_verse=english_verse
        )
        return parallel_verse
