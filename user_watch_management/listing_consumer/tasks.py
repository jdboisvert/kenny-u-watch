from celery import shared_task
from django.core.mail import send_mail


from listing_consumer.data_models import KennyUPullListing
from alerts.models import Alert, Vehicle

import logging

logger = logging.getLogger(__name__)


@shared_task
def ingest_listening(kenny_u_pull_listing_data: dict[str, str]):
    """
    Ingest a listing and alert all users who are watching for this listing.

    :param kenny_u_pull_listing: The listing to ingest.
    """
    kenny_u_pull_listing = KennyUPullListing(**kenny_u_pull_listing_data)
    logger.info(f"Got a new listing to ingest: {kenny_u_pull_listing}")

    try:
        alert = Alert.objects.get(external_id=kenny_u_pull_listing.client_id)
        if alert.branch and alert.branch != kenny_u_pull_listing.branch:
            # The branch doesn't match what the user wanted, skip this alert.
            logger.info(f"Skipping alert {kenny_u_pull_listing} because the branch doesn't match.")
            return

        if alert.vehicle.manufacturer_name.lower() != kenny_u_pull_listing.make.lower():
            # The manufacturer doesn't match what the user wanted, skip this alert.
            logger.info(f"Skipping alert {kenny_u_pull_listing} because the manufacturer doesn't match.")
            return

        if alert.vehicle.model_name.lower() != kenny_u_pull_listing.model.lower():
            # The model doesn't match what the user wanted, skip this alert.
            logger.info(f"Skipping alert {kenny_u_pull_listing} because the model doesn't match.")
            return

        try:
            logger.info(f"Sending email to {alert.user.email} for {alert.vehicle} for alert {alert.id}")
            # TODO apply i18n to this email's text.
            send_mail(
                f"Hey! You have a new listing for a {alert.vehicle}!",
                f"You can go visit the listing on their website at {kenny_u_pull_listing.listing_url}",
                "kennyu.watch@gmail.com",
                [
                    alert.user.email,
                ],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send email to {alert.user.email} for {alert.vehicle} with error {e}")

    except Alert.DoesNotExist:
        logger.warning(f"Got a listing for a vehicle we don't have an alert for: {kenny_u_pull_listing}")
