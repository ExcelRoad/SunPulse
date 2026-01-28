from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^05\d{8}$',
    message='מספר טלפון לא תקין. פורמט: 05XXXXXXXX'
)


israeli_id_validator = RegexValidator(
    regex=r'^\d{9}$',
    message='תעודת זהות חייבת להכיל 9 ספרות'
)