from django.urls import path
from .api import TrainingListUpdate


urlpatterns = [
    path('', TrainingListUpdate.as_view(), name='training-list-update'),
] 