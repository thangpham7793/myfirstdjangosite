from django.contrib import admin

# Register your models here.
from .models import Question, Choice

# Basically like a phpmyadmin site
class ChoiceInLine(
    admin.TabularInline
):  # make choice fields show up as cols of a table
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Question Content", {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]

    inlines = [ChoiceInLine]  # enable choices to be edited from Question
    list_display = (
        "question_text",
        "pub_date",
        "published_recently",  # method name can be added as well
    )  # fields to display for each Question object

    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
