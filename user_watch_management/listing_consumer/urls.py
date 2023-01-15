from django.urls import path
import listing_consumer.views as views

urlpatterns = [
    path("v1/new-listing", views.consume_listing),
]
