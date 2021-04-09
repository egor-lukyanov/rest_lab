from django.urls import path
from rest_framework import routers
from main import views

router = routers.SimpleRouter()
router.register(r'jobs', views.JobViewSet)
router.register(r'results', views.JobResultViewSet)

urlpatterns = [
    path(r'api/simple/', views.SimpleView.as_view()),
    path(r'api/cpu/', views.CPUView.as_view()),
    path(r'api/big/', views.BigView.as_view()),
    path(r'api/ping/', views.PingView.as_view())
]