from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def confirm_email_sendler(email, confirm_code):
    """Функция для отправки сообщения пользователю с кодом подтверждения."""
    send_mail(
        subject='Код подтверждения',
        message=(
            f'Ваш код регистрации учетной записи: {confirm_code}.\n'
        ),
        from_email=settings.YAMDB_EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )


def get_auth_jwt_token(user):
    """Генератор jwt-токена."""
    token = RefreshToken.for_user(user)
    message = {
        'refresh': str(token),
        'access': str(token.access_token),
    }
    return message
