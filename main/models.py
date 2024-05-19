from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Assignment(models.Model):
    subject = models.CharField(max_length=100)
    due_date = models.DateField()
    description = models.TextField()
    students = models.ManyToManyField(User, related_name='assignments')

    def __str__(self):
        return self.subject