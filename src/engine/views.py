from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Word
from .serializers import WordSerializer
from .utility import process_word, process_sentence, process_assessment, process_chatbot, webscrapeHowManySyllables, webscrapeYouGlish, webscrapeMerriam

load_dotenv()

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def process(request):
    process_type = request.GET.get('type')
    if (process_type == 'word'):
        print("processing word")
        return process_word(request)
    elif (process_type == 'sentence'):
        print("processing sentence")
        return process_sentence(request)
    elif (process_type == 'assessment'):
        print("processing assessment")
        return process_assessment(request)
    elif (process_type == 'chatbot'):
        print("processing chatbot")
        return process_chatbot(request)
    else:
        return Response(data="Invalid process type", status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def search(request):
    existing = Word.objects.filter(word=request.data.get('search'))
    if existing:
        print("existing word found in db. returning...")
        serializer = WordSerializer(existing, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    print("word not found in db. scraping...")

    word = request.data.get('search')
    word = word.lower()

    print("web scraping howmanysyllables...")

    scrapedHowManySyllables = webscrapeHowManySyllables(word)
    
    if scrapedHowManySyllables:
        print("web scraped from howmanysyllables")
        new_word = Word(word=word, laymans=scrapedHowManySyllables)
        
    else:
        print("web scraping youglish...")
        scrapedYouGlish = webscrapeYouGlish(word)

        if scrapedYouGlish:
            print("web scraped from youglish")
            new_word = Word(word=word, laymans=scrapedYouGlish)

        else:
            print("web scraped from Merriam")
            generated = webscrapeMerriam(word)
            new_word = Word(word=word, laymans=generated)

    new_word.save()
    serializer = WordSerializer(new_word)

    return Response(data=[serializer.data], status=status.HTTP_200_OK)
