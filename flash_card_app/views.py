import random

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views import View

from flash_card_app.models import FlashCard, Attempt


def random_card(request):
    card = get_random()
    attempt_count = Attempt.objects.filter(flash_card=card).count()
    correct_count = Attempt.objects.filter(flash_card=card,is_correct=True).count()
    last_four = Attempt.objects.filter(flash_card=card).order_by('published_at')[::-1][:4]
    context = {
        'card': card,
        'attempt_count': attempt_count,
        'correct_count': correct_count,
        'last_four': last_four
    }
    return render(request, 'random_card.html', context)


class CreateAttempt(View):

    def post(self, request):
        is_correct = True if request.POST.get("is_correct") == "true" else False
        flash_card_id = request.POST.get("flash_card_id")
        flash_card = FlashCard.objects.get(pk=flash_card_id)
        Attempt.objects.create(is_correct=is_correct, flash_card=flash_card)
        return HttpResponse('OK')


# utilities
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
