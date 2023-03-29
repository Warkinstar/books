import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from tinymce.models import HTMLField


ACCESS_PUBLIC = 0
ACCESS_TEACHER = 1
ACCESS_PRIVATE = 2
ACCESS_LEVEL_CHOICES = [
    (ACCESS_PUBLIC, "Все"),
    (ACCESS_TEACHER, "Преподаватели"),
    (ACCESS_PRIVATE, "Только я"),
]


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Название", max_length=200)
    preview = HTMLField("Превью", blank=True)
    text = HTMLField()
    image = models.ImageField("Изображение", upload_to="images/", blank=True)
    document = models.FileField("Документ", upload_to="documents/", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Название темы", max_length=200)
    access_level = models.IntegerField(
        "Доступ",
        help_text="Кто видит эту тему и имеет к ней доступ",
        choices=ACCESS_LEVEL_CHOICES,
        default=ACCESS_PUBLIC,
    )
    image = models.ImageField("Изображение", upload_to="images/topics", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_indexT"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("topic", args=[str(self.id)])


class SubTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField("Название подтемы", max_length=200)
    access_level = models.IntegerField(
        "Имеют доступ",
        help_text="Кто видит эту тему и имеет к ней доступ",
        choices=ACCESS_LEVEL_CHOICES,
        default=ACCESS_PUBLIC,
    )
    image = models.ImageField("Изображение", upload_to="images/subtopics", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("subtopic", args=[str(self.id)])


class Record(models.Model):
    """Информация, изученная пользователем по теме."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField("Название темы записи", max_length=200)
    preview = HTMLField("Превью", blank=True)
    text = HTMLField("Описание")
    access_level = models.IntegerField(
        "Имеют доступ",
        help_text="Кто видит эту запись и имеет к ней доступ",
        choices=ACCESS_LEVEL_CHOICES,
        default=ACCESS_PUBLIC,
    )
    image = models.ImageField("Изображение", upload_to="images/records", blank=True)
    document = models.FileField("Документ", upload_to="documents/records", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Возвращает строковое представление модели. До 50 символов"""
        return self.title

    def get_absolute_url(self):
        return reverse("record", args=[str(self.id)])


class ItemBase(models.Model):
    """Абстрактная модель файлов для записей"""
    title = models.CharField(max_length=250, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f"learning/items/{self._meta.model_name}.html", {"item": self}
        )


class RecordFile(ItemBase):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="Файл", related_name="files")
    file = models.FileField(
        verbose_name="Доп. документ",
        upload_to="documents/records/",
    )


class SubRecord(models.Model):
    """Информация, изученная пользователем по теме."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)  # subtopic
    title = models.CharField("Название темы записи", max_length=200)
    preview = HTMLField("Превью", blank=True)
    text = HTMLField("Описание")
    access_level = models.IntegerField(
        "Имеют доступ",
        help_text="Кто видит эту запись и имеет к ней доступ",
        choices=ACCESS_LEVEL_CHOICES,
        default=ACCESS_PUBLIC,
    )
    image = models.ImageField("Изображение", upload_to="images/subrecords", blank=True)
    document = models.FileField(
        "Документ", upload_to="documents/subrecords", blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Возвращает строковое представление модели. До 50 символов"""
        return self.title

    def get_absolute_url(self):
        return reverse("subrecord", args=[str(self.id)])


class SubRecordFile(ItemBase):
    subrecord = models.ForeignKey(
        SubRecord, on_delete=models.CASCADE, verbose_name="Файл", related_name="files"
    )
    file = models.FileField(
        verbose_name="Доп. документ",
        upload_to="documents/subrecords",
    )
