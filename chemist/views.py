import jwt
from datetime import datetime, timedelta, timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from .models import Chemist
from .serializers import ChemistSerializer
from django.contrib.auth.hashers import check_password

class ChemistViewSet(viewsets.ModelViewSet):
    queryset = Chemist.objects.all()
    serializer_class = ChemistSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            chemist = Chemist.objects.get(email=email)
            if check_password(password, chemist.password):
                token = self.create_jwt_token(chemist)
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Chemist.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.session.flush()
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)

    def create_jwt_token(self, chemist):
        payload = {
            'id': chemist.id,
            'email': chemist.email,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
