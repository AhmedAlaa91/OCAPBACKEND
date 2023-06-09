from __future__ import annotations

import base64
import json
import logging

import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect


class OrangeAuthBackend(BaseBackend):
    logger = logging.getLogger(__name__)

    def authenticate(self, request):
        """Override authenticate method in base auth backend

        Parameters
        ----------
        request : HttpRequest
            The request object
        """
        try:
            self.logger.debug('orange_auth_backend: start authenticate method')
            user = request.user
            if 'cuid' in request.session:
                if user.is_anonymous == False and user.username == request.session['cuid']:
                    return redirect(request.META.get('HTTP_REFERER', 'pages.home'))
                else:
                    return self.check_user_authentication(request, request.session['cuid'])
            elif 'cuid' not in request.session:
                # Check if URL query string contains "code" which means the user authenticated by Orange API
                return self.handle_auth_code_authorization(request=request)
            else:
                return self.do_authenticate()
        except Exception as ex:
            self.logger.error(ex)
        finally:
            self.logger.debug('orange_auth_backend: end authenticate method')

    def get_user(self, user_id):
        """Override get_user method in base auth backend

        Parameters
        ----------
        user_id : Integer
            The user ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @classmethod
    def do_authenticate(cls):
        """Redirect user to orange windows session identifier for authentication
        """

        try:
            cls.logger.debug(
                'orange_auth_backend: start do_authenticate method',
            )
            response = redirect(
                'https://inside01.api.intraorange/openidconnect/internal/v1/authorize?response_type=code&client_id=' +
                settings.ORANGE_AUTH_CLIENT_ID + '&redirect_uri=' +
                settings.ORANGE_AUTH_REDIRECT_URI + '&scope=openid&state=test',
            )
            return response
            # return (response.headers['Location'] if hasattr(response, 'headers') else response) if response.status_code == 302 else response.text
        except Exception as ex:
            cls.logger.error(ex)
        finally:
            cls.logger.debug('orange_auth_backend: end do_authenticate method')

    @classmethod
    def handle_auth_code_authorization(cls, request: HttpRequest):
        """Handle request either with code authorization from authentication callback or do orange authentication

        Parameters
        ----------
        request : HttpRequest
            The request object
        """

        def get_request_headers(headers={}):
            return headers | {
                'Authorization': settings.ORANGE_AUTH_HEADER,
                'Content-Type': 'application/x-www-form-urlencoded',
            }

        def get_request_params(params={}):
            return params | {
                'grant_type': 'authorization_code',
                'code': request.GET.get('code') if request.GET.get('code') is not None else None,
                'redirect_uri': settings.ORANGE_AUTH_REDIRECT_URI,
            }

        if request.GET.get('code') is not None:
            headers = get_request_headers()
            parameters = get_request_params()
            response = requests.post(
                settings.ORANGE_AUTH_URL, headers=headers, data=parameters, verify=False,
            )
            return cls.handle_auth_response(request=request, response=response)
        else:
            return cls.do_authenticate()

    @classmethod
    def handle_auth_response(cls, request: HttpRequest, response: HttpResponse):
        """Handle orange auth response to get response data

        Parameters
        ----------
        request : HttpRequest
            The request object
        response : HttpResponse
            The response object
        """
        if response.status_code == 200:
            json_response = json.loads(response.text)
            request.session['access_token'] = json_response.get('access_token')
            request.session['expires_in'] = json_response.get('expires_in')
            request.session['id_token'] = json_response.get('id_token')
            request.session['token_type'] = json_response.get('token_type')
            decoded_string = base64.b64decode(
                request.session['id_token'].split(
                    '.',
                )[1] + '==',
            )      # "==" added to fix error "Incorrect padding" in decoding
            logged_user_cuid = json.loads(decoded_string).get('sub')
            request.session['cuid'] = logged_user_cuid
            # Compare sub element with CUID in DB
            return cls.check_user_authentication(request, logged_user_cuid)
        else:
            return redirect('pages.home')

    @classmethod
    def check_user_authentication(cls, request: HttpRequest, cuid: str):
        """Check user authentication to log in django application

        Parameters
        ----------
        request : HttpRequest
            The request object
        cuid : String
            Orange cuid
        """
        try:
            cls.logger.debug(
                'orange_auth_backend: start check_user_authentication method',
            )
            try:
                user = User.objects.get(username=cuid)
                login(request, user, backend='website.backends.OrangeAuthBackend')
                return redirect(request.META.get('HTTP_REFERER', 'pages.home'))
            except User.DoesNotExist:
                return redirect('pages.home')
        except Exception as ex:
            cls.logger.error(ex)
        finally:
            cls.logger.debug(
                'orange_auth_backend: end check_user_authentication method',
            )
