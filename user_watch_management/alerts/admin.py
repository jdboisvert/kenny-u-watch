from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from alerts.models import Vehicle, Alert


class AlertAdmin(SimpleHistoryAdmin):
    """
    A class handling the admin view of the User's alerts in the alerts Django app.
    """

    model = Alert


admin.site.register(Alert, AlertAdmin)
admin.site.register(Vehicle)
