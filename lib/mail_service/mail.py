from __future__ import annotations

import base64
import json
import logging
from typing import Dict
from typing import List

import requests
from django.conf import settings
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)

# get temp access token for send an email


def get_mail_access_token():
    try:
        auth_headers = base64.b64encode(
            f'{settings.ORANGE_SEND_EMAIL_CLIENT_ID}:{settings.ORANGE_SEND_EMAILS_CLIENT_SECRET}'.encode(
                'utf-8',
            ),
        ).decode()

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json;charset=utf-8',
            'Authorization': f'Basic {auth_headers}',

        }
        payload = {
            'grant_type': 'client_credentials',
        }
        response = requests.post(
            url=settings.SEND_MAILS_ACCESS_TOKENS_URL, data=payload,
            headers=headers,
            verify=settings.ORANGE_MAIL_API_CERT, timeout=10,
        )
        data = json.dumps(response.json())
        content = json.loads(data)
        logger.info(f"token is generated {content['access_token']}")
        return content['access_token']
    except Exception as ex:
        logger.error(f'error  :{str(ex)} ')
        return None


# Send Alertig Email
def send_alerting_message(email_list: List[Dict[str, str]], content_message: str):
    """
   send alerting message to  list of employee
    """
    try:
        token = get_mail_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        context = {
            'content': content_message,
        }
        logger.info(f'trying to send alert to {len(email_list)} users')
        msg_template = render_to_string(
            'partials/_email-template.html', context=context,
        )
        payload = {
            'messages': [
                {
                    'html': msg_template,
                    'from': {
                        'email': f'{settings.SENDER_EMAIL}',
                        'name': 'OCAP',
                    },
                    'replyTo': {
                        'email': f'{settings.SENDER_EMAIL}',
                        'name': 'OCAP',
                    },
                    'subject': '[Car-Pooling] Alerting Message ',
                    'to': email_list,
                },
            ],
        }
        response = requests.post(
            url=settings.SEND_MAIL_SERVICE_URL, data=json.dumps(payload),
            headers=headers,
            verify=settings.ORANGE_MAIL_API_CERT, timeout=10,
        )
        logger.info(f'Email send status code : {response.status_code}')
        return response.status_code
    except Exception as ex:
        logger.error(f'error {str(ex)}')
        return None
