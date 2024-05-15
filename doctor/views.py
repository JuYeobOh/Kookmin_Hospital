import jwt
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Doctor
from django.conf import settings

# JWT 토큰 생성 함수
def create_jwt_token(doctor):
    payload = {
        'id': doctor.id,
        'email': doctor.email,
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

@require_http_methods(["POST"])
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        doctor = Doctor.objects.get(email=email)
        if doctor.check_password(password):
            token = create_jwt_token(doctor)
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=401)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)

@require_http_methods(["POST"])
def logout(request):
    # 로그아웃 뷰는 세션 기반 로그인 시 사용
    request.session.flush()
    return JsonResponse({'message': 'Logged out'}, status=200)
