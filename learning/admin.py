from django.contrib import admin
from .models import Book, Review, Topic, Record, SubTopic, SubRecord


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ("title",)


admin.site.register(Book, BookAdmin)
admin.site.register(Topic)
admin.site.register(Record)
admin.site.register(SubTopic)
admin.site.register(SubRecord)

