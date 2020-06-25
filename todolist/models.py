from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class todoItem(models.Model):
    choices = (
        (0, 'Low'),
        (1, 'Medium'),
        (2, 'High'),
    )
    item_text = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(null=True,
                                   choices=choices,
                                   default=choices[0][0],)

    def __str__(self):
        return self.item_text
