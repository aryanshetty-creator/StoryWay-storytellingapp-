from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.story_gui, name='story_gui'), 
    path('api/generate-story/', views.generate_story, name='generate_story'),
]