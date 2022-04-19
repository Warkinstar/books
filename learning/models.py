import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='images/', blank=True)
    document = models.FileField('Документ', upload_to='documents/', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review


@receiver(models.signals.post_delete, sender=Book)
def auto_delete_document(sender, instance, **kargs):
    file = instance.document
    try:
        file.storage.delete(name=file.name)
    except:
        print('nothing')


@receiver(models.signals.post_delete, sender=Book)
def auto_delete_document(sender, instance, **kargs):
    file = instance.image
    try:
        file.storage.delete(name=file.name)
    except:
        print('nothing')