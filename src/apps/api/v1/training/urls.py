from django.urls import path
from .api import TrainingListUpdate, TrainingInfo


urlpatterns = [
    path('', TrainingListUpdate.as_view(), name='training-list-update'),
    path('info/', TrainingInfo.as_view()),
] 