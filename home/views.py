from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_exempt
import logging
import requests
import base64
import imghdr
import json
from dac.settings import config

SITE_DATA = {
    'google_api_js': config.get('Google', 'api_js_uri'),
    'google_site_key': config.get('Google', 'site_key'),
    'disable_header': config.getboolean(
        'Settings', 'disable_header', fallback=False
    ),
    'disable_footer': config.getboolean(
        'Settings', 'disable_footer', fallback=False
    ),
}

logger = logging.getLogger('dac')
stats = logging.getLogger('stats')


@xframe_options_exempt
def home(request):
    """
    View: /
    """
    return render(request, 'home.html', {'site_data': SITE_DATA})


@xframe_options_exempt
@require_http_methods(["POST"])
def avatar(request):
    """
    View: /avatar/
    """
    try:
        if not captcha_verify(request):
            return HttpResponse('Google Captcha Verify Failed.', status=400)

        if 'inputName' not in request.POST:
            error = "Please enter the bot <strong>Username</strong>."
            return HttpResponse(error, status=400)

        if 'inputToken' not in request.POST:
            error = "Please enter the bot <strong>OAuth Token</strong>."
            return HttpResponse(error, status=400)

        if 'inputAvatarFile' not in request.FILES:
            error = "Please select the bot's <strong>Avatar File</strong>."
            return HttpResponse(error, status=400)

        _name = request.POST['inputName']
        _token = request.POST['inputToken']
        _file = request.FILES['inputAvatarFile']

        img_type = imghdr.what(_file)
        with _file as image_file:
            testing = image_file.read()
            encoded_string = base64.b64encode(testing)
        image_data = 'data:image/%s;base64,%s' % (
            img_type, encoded_string.decode('ascii')
        )

        if config.get('Logging', 'ip_header') in request.META:
            ipaddr = request.META[config.get('Logging', 'ip_header')]
        else:
            ipaddr = 'unknown'
        try:
            discord = change_avatar(_token, _name, image_data)
            stats.info('SUCCESS - %s' % ipaddr)
        except Exception as error:
            stats.info('FAILURE - %s - %s' % (ipaddr, error))
            err_msg = 'Discord API Error: %s' % error
            return HttpResponse(err_msg, status=400)

        d_dict = json.loads(discord)
        d_json = json.dumps(d_dict, sort_keys=True, indent=2)

        winning = '-- What You Sent --\n\nname:   %s\ntoken:  %s\nimage:  %s\n\n-- What Discord Returned --\n\n%s' % (
            _name, _token, image_data, d_json
        )
        return HttpResponse(winning, status=200)

    except Exception as error:
        logger.error(error)
        return HttpResponse(error, status=400)


def captcha_verify(request):
    try:
        if request.session['recaptchaverified']:
            return True
    except:
        pass

    try:
        uri = config.get('Google', 'siteverify_uri')
        data = {
            'secret': config.get('Google', 'google_secret'),
            'response': request.POST['g-recaptcha-response']
        }
        r = requests.post(uri, data=data, timeout=6)
        j = json.loads(r.text)
        logger.debug(j)
        if j['success']:
            request.session['recaptchaverified'] = True
            return True
        else:
            return False
    except Exception as error:
        logger.exception(error)
        return False


def change_avatar(oauth, username, image):
    headers = {'Authorization': 'Bot ' + oauth, 'Content-Type': 'application/json'}
    data = {'username': username, 'avatar': image}
    uri = 'https://discordapp.com/api/users/@me'
    r = requests.patch(uri, data=json.dumps(data), headers=headers, timeout=10)
    results = json.loads(r.text)
    logger.debug(results)
    if r.status_code != 200:
        raise ValueError(r.text)
    else:
        return r.text
