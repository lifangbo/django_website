from django.contrib import admin
from .models import user_ext

# Register your models here.
class ChoiceInline(admin.StackedInline):
    model = user_ext
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Information', {'fields': ['birthday'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(user_ext, QuestionAdmin)
