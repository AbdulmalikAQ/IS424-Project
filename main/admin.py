from django.contrib import admin
from .models import User, Assignment

class Admin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_superuser')
    list_filter = ('user_type', 'is_superuser')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'due_date')
    filter_horizontal = ('students',)

admin.site.register(User, Admin)
admin.site.register(Assignment, AssignmentAdmin)