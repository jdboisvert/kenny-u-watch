from rest_framework import serializers


class KennyUPullListingSerializer(serializers.Serializer):
    year = serializers.CharField()
    make = serializers.CharField()
    model = serializers.CharField()
    date_listed = serializers.CharField()
    row_id = serializers.CharField()
    branch = serializers.CharField()
    listing_url = serializers.CharField()
    client_id = serializers.UUIDField()
