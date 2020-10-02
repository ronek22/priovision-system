from django.shortcuts import render
from .models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView


# Create your views here.
class CreateClientView(CreateAPIView):
    model = Client
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer