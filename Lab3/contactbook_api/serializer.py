from rest_framework import serializers
from django.forms import ValidationError

from .models import Contact, User


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField("username", read_only=True)
    contact_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(max_length=50, required=False)
    phone_number = serializers.IntegerField(required=True)

    class Meta:
        model = Contact
        fields = ['id', 'user', 'contact_name', 'email', 'phone_number']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        contact = Contact.objects.create(**validated_data)
        return contact

    def validate(self, data):
        if len(data['contact_name']) < 5:
            raise ValidationError("Thats a bad contact name. Ensure contact name has a minimum of 5 characters")
        return data

    def update(self, instance, validated_data):
        instance.contact_name = validated_data.get('contact_name', instance.contact_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
