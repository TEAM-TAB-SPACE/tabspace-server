from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os
import json
import sys
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRET_BASE_FILE = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']
CLOUDFRONT = secrets['cloudfront']
KOREAN_API_KEY = secrets["serviceKey"]
KAKAO_REST_API_KEY = secrets["kakao_rest_api_key"]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #유저 인증
    "rest_framework",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    #보안
    "corsheaders",
    #기타
    'django_crontab',
    #앱
    "users.apps.UsersConfig",
    'common.apps.CommonConfig',
    'secretkeys.apps.SecretkeysConfig',
    'lectures.apps.LecturesConfig',
    'lecture_rooms.apps.LectureRoomsConfig',
    'dashboards.apps.DashboardsConfig',
    'homeworks.apps.HomeworksConfig',
    'course_reviews.apps.CourseReviewsConfig',
    'lecture_comments.apps.LectureCommentsConfig',
    'weekdays.apps.WeekdaysConfig',
    'appliers.apps.AppliersConfig',
    #저장소
    'storages',
    
]

CRONJOBS = [
    ('0 0 1 * *', 'lectures.cron.update_monthly_lectures', '>> /home/ubuntu/tabspace-server/cron_logs/update_monthly_lectures.log'),
    ('0 0 * * 1-5', 'lectures.cron.update_today_lectures', '>> /home/ubuntu/tabspace-server/cron_logs/update_today_lectures.log'),   
    ('59 23 * * 1-5', 'dashboards.cron.update_user_attendance', '>> /home/ubuntu/tabspace-server/cron_logs/update_user_attendance.log'),   
    ('0 0 * * 6', 'lectures.cron.update_no_today_lectures', '>> /home/ubuntu/tabspace-server/cron_logs/update_no_today_lectures.log'),   
    ('3 0 * * *', 'dashboards.cron.update_user_notifications', '>> /home/ubuntu/tabspace-server/cron_logs/update_user_notifications.log'),   
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

MIDDLEWARE = [
     #corsheaders
    "corsheaders.middleware.CorsMiddleware",
    #
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
   
    
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default":{
        "ENGINE":"django.db.backends.mysql",
        "NAME":secrets["DBNAME"],
        "USER":secrets["USER"],
        "PASSWORD":secrets["PASSWORD"],
        "HOST":secrets["HOST"],
        "PORT":"3306"
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True
USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",

    # custom
    'AUTH_COOKIE': 'access',
    # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh',
    # A string like "example.com", or None for standard domain cookie. 나중에 client domain 주소로 수정
    'AUTH_COOKIE_DOMAIN': None,
    # # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_SECURE': False, 
    # # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_HTTP_ONLY': False,
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    # # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
    'AUTH_COOKIE_SAMESITE': 'Lax', # TODO: Modify to Lax
}

# CORS 관련 추가
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000','http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True #쿠키가 cross-site HTTP 요청에 포함될 수 있다

# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

#CSRF token을 session으로 관리함, 토큰 저장 안됨
# CSRF_USE_SESSIONS = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = "None"
# SESSION_COOKIE_SAMESITE = "None"

#커스텀유저
AUTH_USER_MODEL = "users.User"

#s3 저장소
###########################AWS
AWS_ACCESS_KEY_ID = secrets["AWS_ACCESS_KEY_ID"] # .csv 파일에 있는 내용을 입력 Access key ID
AWS_SECRET_ACCESS_KEY = secrets["AWS_SECRET_ACCESS_KEY"] # .csv 파일에 있는 내용을 입력 Secret access key
AWS_REGION = secrets["AWS_REGION"]

###S3 Storages
AWS_STORAGE_BUCKET_NAME = secrets["AWS_STORAGE_BUCKET_NAME"] # 설정한 버킷 이름
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'config.utils.CustomS3Boto3Storage'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'path/to/store/my/files/')
