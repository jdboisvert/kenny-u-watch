from django.urls import path
import alerts.views as views

urlpatterns = [
    path("v1/get-alerts", views.get_alerts),
    path("v1/get-alert/<int:alert_id>", views.get_alert),
    path("v1/create-alert", views.create_alert),
    path("v1/update-alert/<int:alert_id>", views.update_alert),
    path("v1/delete-alert/<int:alert_id>", views.delete_alert),
]
