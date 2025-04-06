from django.urls import path
from .views import chat_with_gemini, questionnaire,submit_profile, risk_score

urlpatterns = [
    path('', questionnaire, name='questionnaire'),
    path("chat/", chat_with_gemini),
    path('submit-profile/', submit_profile, name='submit_profile'),
    path('risk-score/', risk_score, name='risk_score'),
]
