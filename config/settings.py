from pathlib import Path
from environs import Env
from datetime import timedelta

env = Env()
env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env.str("SECRET_KEY")
BOT_TOKEN = env.str("BOT_TOKEN")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # External
    "rest_framework",
    "drf_yasg",
    "django_filters",
    "nested_admin",
    "rest_framework_simplejwt.token_blacklist",
    "click_up",
    # Internal
    "users",
    "core",
    "quiz",
    "payment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "basic",
        },
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
    },
    "LOGOUT_URL": "/api/v1/auth/logout/",
    "LOGIN_URL": "/api/v1/auth/login/",
    "DOC_EXPANSION": "none",
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = "users.User"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "/static/"

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]
else:
    STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Click API settings

BASE_URL = "https://api.click.uz/v2/merchant/card_token"
CREATE_TOKEN_URL = f"{BASE_URL}/request"
VERIFY_TOKEN_URL = f"{BASE_URL}/verify"
PAYMENT_TOKEN_URL = f"{BASE_URL}/payment"


CLICK_SERVICE_ID = env.int("CLICK_SERVICE_ID")
CLICK_MERCHANT_ID = env.int("CLICK_MERCHANT_ID")
CLICK_SECRET_KEY = env.str("CLICK_SECRET_KEY")
CLICK_MERCHANT_USER_ID = env.int("CLICK_MERCHANT_USER_ID")

CLICK_ACCOUNT_MODEL = "payment.models.Payment"
CLICK_AMOUNT_FIELD = "amount"


TEST_CARD_NUMBERS = env.list("TEST_CARD_NUMBERS", subcast=str)
TEST_CARD_EXPIRY = env.list("TEST_CARD_EXPIRY", subcast=str)


OTP_EMAIL = env.str("OTP_EMAIL", default="TEST")
OTP_PASSWORD = env.str("OTP_PASSWORD", default="TEST")


# Logger

INSTALLED_APPS += ["drf_api_logger"]
MIDDLEWARE += ["drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware"]
DRF_API_LOGGER_DATABASE = True
