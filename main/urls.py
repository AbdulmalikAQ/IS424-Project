from django.urls import path
from .views import *

urlpatterns = [
    path('', default, name='default'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('assignments/', assignments_list, name='assignments'),
    path('assignments/<int:pk>/', assignment_detail, name='assignment_detail'),
    path('assignments/create/', assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/edit/', assignment_update, name='assignment_update'),
    path('assignments/<int:pk>/delete/', assignment_delete, name='assignment_delete')
]