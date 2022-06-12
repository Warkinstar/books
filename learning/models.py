import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from tinymce.models import HTMLField


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField('Название', max_length=200)
    preview = HTMLField('Превью', blank=True)
    text = HTMLField()
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


class Topic(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField('Название темы', max_length=200)
    image = models.ImageField('Изображение', upload_to='images/topics', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_indexT'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topic', args=[str(self.id)])


class SubTopic(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField('Название подтемы', max_length=200)
    image = models.ImageField('Изображение', upload_to='images/subtopics', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subtopic', args=[str(self.id)])


class Record(models.Model):
    """Информация, изученная пользователем по теме."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField('Название темы записи', max_length=200)
    preview = HTMLField('Превью', blank=True)
    text = HTMLField('Описание')
    image = models.ImageField('Изображение', upload_to='images/records', blank=True)
    document = models.FileField('Документ', upload_to='documents/records', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Возвращает строковое представление модели. До 50 символов"""
        return self.title

    def get_absolute_url(self):
        return reverse('record', args=[str(self.id)])


class SubRecord(models.Model):
    """Информация, изученная пользователем по теме."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE) # subtopic
    title = models.CharField('Название темы записи', max_length=200)
    preview = HTMLField('Превью', blank=True)
    text = HTMLField('Описание')
    image = models.ImageField('Изображение', upload_to='images/subrecords', blank=True)
    document = models.FileField('Документ', upload_to='documents/subrecords', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Возвращает строковое представление модели. До 50 символов"""
        return self.title

    def get_absolute_url(self):
        return reverse('subrecord', args=[str(self.id)])


@receiver(models.signals.post_delete, sender=Book)
@receiver(models.signals.post_delete, sender=Record)
@receiver(models.signals.post_delete, sender=SubRecord)
def auto_delete_document(sender, instance, **kargs):
    file = instance.document
    try:
        file.storage.delete(name=file.name)
    except:
        print('nothing')


@receiver(models.signals.post_delete, sender=Book)
@receiver(models.signals.post_delete, sender=Topic)
@receiver(models.signals.post_delete, sender=SubTopic)
@receiver(models.signals.post_delete, sender=Record)
@receiver(models.signals.post_delete, sender=SubRecord)
def auto_delete_image(sender, instance, **kargs):
    file = instance.image
    try:
        file.storage.delete(name=file.name)
    except:
        print('nothing')