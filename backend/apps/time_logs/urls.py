from django.urls import path
from apps.time_logs.views import WorkSessionStartView

urlpatterns = [
    path('work-session/start/', WorkSessionStartView.as_view(), name='work-session-start'),
]