from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField("username", read_only=True)
    contact_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(max_length=50, required=False)
    phone_number = serializers.IntegerField(required=True)
