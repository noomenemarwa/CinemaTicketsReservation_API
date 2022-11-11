from rest_framework import serializers
from tickets.models import Guest, Movie, Resevation, Post

# Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# Reservation Serializer 
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model =Resevation
        fields = '__all__'

# Guest Serializer
class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model= Guest
        fields= ['pk', 'reservation', 'name', 'mobile']

# uuid and slug

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields = '__all__'
