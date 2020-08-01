from django.db import models

# Create your models here.

class FlashCard(models.Model):
    front_card_text = models.CharField(max_length=200, help_text="content of the front of the card")
    back_card_text = models.CharField(max_length=200, help_text="content of the back of the card")

    def __str__(self):
        return f"{self.front_card_text}, {self.back_card_text}"

class Attempt(models.Model):
    flash_card = models.ForeignKey('FlashCard', on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False,help_text="Whether the answer is correct or not")

    def __str__(self):
        return f"attempt={self.flash_card} is published_at={self.published_at}"