from django.contrib import admin

from eventlog.mixins import LoggerAdminMixin

from school.models.base import Tag


@admin.register(Tag)
class TagAdmin(LoggerAdminMixin, admin.ModelAdmin):
    list_display = ["id", "text", "logger"]
