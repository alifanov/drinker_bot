from django.urls import path
from .views import UpdateBotView

urlpatterns = [
    path('<str:token>', UpdateBotView.as_view(), name='update'),
]