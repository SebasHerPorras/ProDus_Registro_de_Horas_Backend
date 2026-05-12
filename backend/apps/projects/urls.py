from django.urls import path

from apps.projects.views import ActiveProjectListView, ActiveCoordinatorListView


urlpatterns = [
    path('active/', ActiveProjectListView.as_view(), name='projects-active-list'),
    path('coordinators/active/', ActiveCoordinatorListView.as_view(), name='coordinators-active-list'),
]