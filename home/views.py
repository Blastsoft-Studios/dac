from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
import logging
import requests
import base64
import imghdr
import json
from dac.settings import config

logger = logging.getLogger(__name__)


def home(request):
    google_stuff = {
        'js_uri': config.get('Google', 'api_js_uri'),
        'site_key': config.get('Google', 'site_key'),
    }
    return render(request, 'home.html', {'google': google_stuff})


@require_http_methods(["POST"])
def avatar(request):
    try:
        if not captcha_verify(request):
            return HttpResponse('Google Captcha Verify Failed.', status=400)

        _name = request.POST['inputName']
        _token = request.POST['inputToken']
        _file = request.FILES['inputAvatarFile']

        if not _name:
            error = "Please enter the bot <strong>Username</strong>."
            return HttpResponse(error, status=400)

        if not _token:
            error = "Please enter the bot <strong>OAuth Token</strong>."
            return HttpResponse(error, status=400)

        if not _file:
            error = "Please select the bot's <strong>Avatar File</strong>."
            return HttpResponse(error, status=400)

        _name = request.POST['inputName']
        _token = request.POST['inputToken']
        _file = request.FILES['inputAvatarFile']

        img_type = imghdr.what(_file)
        with _file as image_file:
            encoded_string = base64.b64encode(image_file.read())
        image_data = 'data:image/%s;base64,%s' % (
            img_type, encoded_string.decode('ascii')
        )

        discord = change_avatar(_token, _name, image_data)
        d_dict = json.loads(discord)
        d_json = json.dumps(d_dict, sort_keys=True, indent=2)

        winning = '-- What You Sent --\n\nname:   %s\ntoken:  %s\nimage:  %s\n\n-- What Discord Returned --\n\n%s' % (
            _name, _token, image_data, d_json
        )
        return HttpResponse(winning, status=200)

    except Exception as error:
        logger.debug(error)
        return HttpResponse(error, status=400)


def captcha_verify(request):
    try:
        if request.session['recaptchaverified']:
            logger.debug('request.session: recaptchaverified')
            return True
    except:
        logger.debug('not recaptcha verified')
        pass

    try:
        uri = config.get('Google', 'siteverify_uri')
        data = {
            'secret': config.get('Google', 'google_secret'),
            'response': request.POST['g-recaptcha-response']
        }
        logger.debug(data)
        r = requests.post(uri, data=data, timeout=6)
        logger.debug(r.text)
        j = json.loads(r.text)
        if j['success']:
            request.session['recaptchaverified'] = True
            return True
        else:
            return False
    except Exception as error:
        logger.debug(error)
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
