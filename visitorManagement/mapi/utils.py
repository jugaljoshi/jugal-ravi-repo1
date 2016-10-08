from django.http import HttpResponse, HttpResponseForbidden, HttpRequest, \
    HttpResponseNotAllowed
import simplejson
import json
import base64
import hmac
import functools
import logging
from django.conf import settings


class MapiErrorCodeDescriptor(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code


class MapiErrorCodes(object):
    LOGIN_REQUIRED = MapiErrorCodeDescriptor('login_required', 100) # goto login page, clear preference data
    GENERIC_ERROR = MapiErrorCodeDescriptor('error_occurred', 101) # same page

    NO_VISITOR_EXIT = MapiErrorCodeDescriptor('no_visitor', 102) # go to create visitor page



    INTERNAL_SERVER_ERROR = MapiErrorCodeDescriptor('internal_server_error', 101)
    INVALID_FIELD = MapiErrorCodeDescriptor('invalid_field', 102)
    INVALID_USER = MapiErrorCodeDescriptor('invalid_user', 103)
    INVALID_USER_PASSED = MapiErrorCodeDescriptor('invalid_user_pass', 105)

    MISSING_REQUIRED_FIELD = MapiErrorCodeDescriptor('missing_required_field', 107)
    INVALID_INPUT = MapiErrorCodeDescriptor('invalid_input', 108)



class JSONResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None,
                 content_type='application/json'):

        if not isinstance(content, str):

            content = simplejson.dumps(content)

        super(JSONResponse, self).__init__(
            content=content,
            #mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


def base64_safe_decode(data):
    """
    EBS sometimes sends BASE64 encoded responses with incorrect padding.
    base64.decode barfs if the data is incorrectly padded
    But we can safely calculate the required padding and pad it
    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)


def mapi_mandatory_parameters(*params):
    from visitorManagement.mapi.views import BaseMapiView
    def decorater_maker(fn):
        @functools.wraps(fn)
        def wrapper(request, *args, **kwargs):
            if isinstance(request, HttpRequest):
                request_dict = request.__getattribute__(request.method)
                for param in params:
                    if not request_dict.get(param, None):
                        return BaseMapiView.render_error_response(
                            MapiErrorCodes.INVALID_FIELD,
                            "Missing field '%s' in request" % param)
            return fn(request, *args, **kwargs)

        return wrapper

    return decorater_maker

'''
def render_response(response=None, status=0, message='success'):
    ret_dict = {'status': status,
                'message': message,
                'response': response if response is not None else {}
                }
    return JSONResponse(json.dumps(ret_dict))


def render_error_response(mapi_error_code, message=None, response=None):
    message = message if message else mapi_error_code.name. \
        replace('_', ' ').capitalize()
    return JSONResponse(json.dumps({'status': mapi_error_code.code,
                                    'message': message,
                                    'response': response if response else {}
                                    }))
'''


def get_visitor_all_fields():
    from visitorManagement.mapi.models import Visitor
    # visitor_fields = Visitor._meta.get_all_field_names() // below 1.8 django version
    visitor_fields = Visitor.object.get_all_field_names()

    # remove foreign key fields
    # visitor_fields.remove('workbook')
    # visitor_fields.remove('workbook_id')
    # visitor_fields.remove('id')
    return visitor_fields


def save_image_to_s3(key, file_name):
    key.key = 'media/%s' % file_name.name
    key.set_contents_from_file(file_name)
    logging.debug("Image from S3 : %s" % key.key)


def get_base_image_url(protocol='http'):
    is_using_s3 = getattr(settings, 'MEDIA_FROM_S3', None)
    if is_using_s3:
        base_url = settings.MEDIA_URL
    else:
        base_url = settings.UPLOAD_DIR
    if base_url.startswith('//'):
        base_url = "%s:%s" % (protocol, base_url)

    if not base_url.endswith("/"):
        base_url = "%s/" % base_url
    return base_url


def format_visitor_data(visitors, needed_fields):
    from copy import deepcopy
    import datetime
    rect_dict = []
    for visitor in visitors:
        d = dict()
        temp_needed_fields = deepcopy(needed_fields)
        while temp_needed_fields:
            field_name = temp_needed_fields.pop()
            field_value = visitor[field_name]
            if isinstance(field_value, datetime.datetime):
                #field_value = field_value.replace(tzinfo=timezone.get_default_timezone())
                field_value = field_value.strftime('%I.%M %p')#("%I.%M %p")

            if field_name in ['photo', 'signature'] and field_value:
                field_value = '%s%s' % (get_base_image_url(), field_value)

            d.update({str(field_name): field_value})
        if d:
            rect_dict.append(d)
    return rect_dict
