from django.db import models

# Create your models here.

class TelegramUser(models.Model):
    full_name = models.CharField(max_length=60)
    username = models.CharField(max_length=60, null=True ,unique=True)
    telegram_id = models.PositiveBigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.full_name