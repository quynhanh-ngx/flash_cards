import random

from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from flash_card_app.models import FlashCard


def random_card(request):
    card = get_random()
    context = {
        'front': card.front_card_text,
        'back': card.back_card_text
    }
    return render(request, 'random_card.html', context)


def get_random() -> 'FlashCard':
    max_id = FlashCard.objects.all().aggregate(max_id=Max("id"))['max_id']
    tried = set()
    while True:
        pk = None
        while pk in tried or pk is None:
            pk = random.randint(1, max_id)
        card = FlashCard.objects.filter(pk=pk).first()
        if card:
            return card
        tried.add(pk)
