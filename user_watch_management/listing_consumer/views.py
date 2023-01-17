from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from listing_consumer.data_models import KennyUPullListing
from listing_consumer.serializers import KennyUPullListingSerializer
from listing_consumer.tasks import ingest_listening


@api_view(["POST"])
@csrf_exempt
def consume_listing(request):
    """
    Consume a listing for a Kenny U Pull listing from the producer.
    """
    data = request.data
    listing_serializer = KennyUPullListingSerializer(data=data)

    if not listing_serializer.is_valid():
        return JsonResponse(listing_serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

    valid_data = listing_serializer.validated_data
    ingest_listening.delay(kenny_u_pull_listing_data=valid_data)

    # Successfully consumed listing.
    return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
