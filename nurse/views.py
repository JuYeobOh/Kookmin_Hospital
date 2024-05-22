# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .models import Nurse, Record
from .serializers import NurseSerializer, RecordSerializer
from django.contrib.auth.hashers import check_password

class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            nurse = Nurse.objects.get(email=email)
            if check_password(password, nurse.password):
                token = self.create_jwt_token(nurse)
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Nurse.DoesNotExist:
            return Response({'error': 'Nurse not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.session.flush()
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)

    def create_jwt_token(self, nurse):
        payload = {
            'id': nurse.id,
            'email': nurse.email,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        nurse_id = self.request.query_params.get('nurse_id', None)
        if nurse_id is not None:
            queryset = queryset.filter(nurse_id=nurse_id)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.refresh_from_db()  # DB에서 최신 데이터 불러오기
        return instance