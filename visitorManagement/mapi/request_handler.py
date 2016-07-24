from django.http import HttpResponse, HttpResponseForbidden, HttpRequest, HttpResponseNotAllowed
from django.http import HttpResponse
from visitorManagement.mapi.utils import base64_safe_decode
from django.conf import settings
import hmac
import json
from visitorManagement.mapi.models import Member
import functools
from django.http import Http404
from visitorManagement.mapi.utils import MapiErrorCodes
import os, time


def validate_request(request, optional=False):
    """
    :type request: HttpRequest
    :type optional: bool
    """
    token = request.COOKIES.get('AUTH_TOKEN')
    if not optional and not token:
        return HttpResponse(
            'X-BB-Auth-Token is empty in cookies',
            content_type='text/plain',
            status=401
        )
    if token:
        member = verify_token(token)
        if member is None:
            if not optional:
                return HttpResponse('Invalid X-BB-Auth-Token value',
                                    content_type='text/plain',
                                    status=401)
            return None

        request.user = member
        return None

    return HttpResponse(
        'X-BB-Auth-Token is empty in cookies',
        content_type='text/plain',
        status=401
    )


def verify_token(token):
    """
    Takes a token and returns a Member object
    """
    member = None
    try:
        decoded_token = token.decode('base64')
    except:
        decoded_token = base64_safe_decode(token)

    ver = decoded_token[0]
    if ver == '0':
        signature = decoded_token[1:17]
        data = decoded_token[17:]
        h = hmac.new(settings.SECRET_KEY, data)
        computed_digest = h.digest()
        if len(signature) != len(computed_digest):
            return None
        else:
            success = True
            for a, b in zip(signature, computed_digest):
                if a != b:
                    success = False
            if not success:
                return None
        json_data = json.loads(data)
        # token_time = json_data['time']
        # expiry_time = token_time + (30 * 24 * 3600)  # One month
        # if expiry_time > time.time():
        #    return None

        try:
            member = Member.objects.get(pk=json_data['mid'])
        except Member.DoesNotExist:
            return member

        return member


def mapi_authenticate(optional=False):
    """
    :param optional: boolean, indicates if login is optional or not.
    compliant response for error is returned
    """

    def decorator_maker(fn):
        """
        :parameter fn: callable
        """

        @functools.wraps(fn)
        def decorator(request, *args, **kwargs):
            from visitorManagement.mapi.views import BaseMapiView
            if not settings.DEBUG and not request.is_secure():
                return HttpResponseForbidden()

            errors = validate_request(request, optional)
            if errors:
                return errors
            try:
                response = fn(request, *args, **kwargs)
            except Exception as e:
                if isinstance(e, Http404):
                    raise e
                if isinstance(e, HttpResponseForbidden):
                    raise e
                else:
                    return BaseMapiView.render_error_response(
                        MapiErrorCodes.INTERNAL_SERVER_ERROR,
                        "Internal Server Error %s" % e.message)
            return response

        return decorator

    return decorator_maker


def make_token(member):
    s = json.dumps({
        'chaff': os.urandom(10).encode('base64'),
        'time': time.time(),
        'mid': member.pk,
        'password': member.password,
        'email': member.email
    })
    h = hmac.new(settings.SECRET_KEY, s)
    token = ('0' + h.digest() + s).encode('base64')
    token = token.replace('\n', '')
    return token