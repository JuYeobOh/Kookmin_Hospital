import jwt
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Nurse, Record
from django.conf import settings

# JWT 토큰 생성 함수
def create_jwt_token(nurse):
    payload = {
        'id': nurse.id,
        'email': nurse.email,
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

@require_http_methods(["POST"])
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        nurse = Nurse.objects.get(email=email)
        if nurse.check_password(password):
            token = create_jwt_token(nurse)
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=401)
    except Nurse.DoesNotExist:
        return JsonResponse({'error': 'Nurse not found'}, status=404)

@require_http_methods(["POST"])
def logout(request):
    # 로그아웃 뷰는 세션 기반 로그인 시 사용
    request.session.flush()
    return JsonResponse({'message': 'Logged out'}, status=200)

@require_http_methods(["POST", "GET"])
def record(request, nurse_id):
    if request.method == 'POST':
        context = request.POST.get('context')
        try:
            nurse = Nurse.objects.get(id=nurse_id)
            Record.objects.create(nurse=nurse, context=context)
            return JsonResponse({'message': 'Record created'}, status=201)
        except Nurse.DoesNotExist:
            return JsonResponse({'error': 'Nurse not found'}, status=404)
    elif request.method == 'GET':
        try:
            nurse = Nurse.objects.get(id=nurse_id)
            records = Record.objects.filter(nurse=nurse).order_by('-date')
            records_data = [{'context': record.context, 'date': record.date.strftime('%Y-%m-%d')} for record in records]
            return JsonResponse({'records': records_data}, status=200)
        except Nurse.DoesNotExist:
            return JsonResponse({'error': 'No records'}, status=404)
