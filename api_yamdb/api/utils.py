from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


def confirm_email_sendler(email: str, user: CustomUser) -> None:
    """
    Функция генерирует 39-значный код и отправляет его на почту указанную
     пользователем.
    """
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=(
            f'Ваш код регистрации учетной записи: {confirmation_code}.'
        ),
        from_email=settings.YAMDB_EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )


def get_auth_jwt_token(user: CustomUser) -> dict[str, str]:
    """Генератор jwt-токена."""
    token = RefreshToken.for_user(user)
    return {
        'refresh': str(token),
        'access': str(token.access_token),
    }
