from django.urls import path
import signup.views as views

urlpatterns = [
    path("v1/new", views.signup),
]
