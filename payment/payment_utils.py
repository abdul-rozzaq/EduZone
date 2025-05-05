import requests
import time
import hashlib
import logging
import time

from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)


def get_digest():
    timestamp = str(int(time.time()))
    digest = hashlib.sha1(f"{timestamp}{settings.CLICK_SECRET_KEY}".encode()).hexdigest()
    return digest, timestamp


def make_request(url, headers, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.RequestException as e:
        logger.error(f"Request to {url} failed: {e}")
        return None, {"error": str(e)}


def create_card_token(card_number, expire_date):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "service_id": settings.CLICK_SERVICE_ID,
        "card_number": card_number,
        "expire_date": expire_date.replace("/", ""),
        "temporary": 1,
    }
    status_code, response_body = make_request(settings.CREATE_TOKEN_URL, headers, payload)

    logger.warning(f"Card token creation response: {response_body}")

    return status_code, response_body


def verify_token(card_token, sms_code):
    digest, timestamp = get_digest()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Auth": f"{settings.CLICK_MERCHANT_USER_ID}:{digest}:{timestamp}",
    }
    payload = {
        "service_id": settings.CLICK_SERVICE_ID,
        "card_token": card_token,
        "sms_code": sms_code,
    }

    return make_request(settings.VERIFY_TOKEN_URL, headers, payload)


def payment_with_token(card_token, amount, payment_id):
    digest, timestamp = get_digest()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Auth": f"{settings.CLICK_MERCHANT_USER_ID}:{digest}:{timestamp}",
    }

    payload = {
        "service_id": settings.CLICK_SERVICE_ID,
        "card_token": card_token,
        "amount": amount,
        "transaction_parameter": payment_id,
    }

    return make_request(settings.PAYMENT_TOKEN_URL, headers, payload)


def generate_payment_check_resource(payment_id):
    digest, timestamp = get_digest()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Auth": f"{settings.CLICK_MERCHANT_USER_ID}:{digest}:{timestamp}",
    }

    response = requests.get(f"https://api.click.uz/v2/merchant/payment/ofd_data/{settings.CLICK_SERVICE_ID}/{payment_id}/", headers=headers)

    return response.status_code, response.json()


def mask_card(card_number: str) -> str:
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Karta raqami 16 xonali bo'lishi kerak")
    return card_number[:4] + "*" * 8 + card_number[-4:]

