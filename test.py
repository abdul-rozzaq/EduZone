import django

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from payment.payment_utils import payment_with_token, create_card_token, verify_token


# print(
#     payment_with_token(
#         card_token="0345E4CA-6186-498D-8E2E-3541D37F1A24",
#         amount=10000,
#         payment_id="asdad",
#     ),
# )

# card = "4073420084009582"
# exp = "07/28"

# print(
#     create_card_token(
#         card_number=card,
#         expire_date=exp,
#     )
# )


TOKEN = '119F32AB-C1CA-4067-BF2D-64044AAF2A22'

print(
    verify_token(
        card_token=TOKEN,
        sms_code=390752,
    ),
)