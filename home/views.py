from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
import configparser
import logging
import requests
import base64
import imghdr
import json
from dac.settings import CONFIG_FILE

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

log_file = config.get('Logging', 'file')
log_level = config.get('Logging', 'level')

logging_level = logging.getLevelName(log_level)
logging.basicConfig(filename=log_file, level=logging_level)


def home(request):
	return render(request, 'home.html')


@require_http_methods(["POST"])
def avatar(request):
	log_req(request)
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

		#return HttpResponse('you win avatar', status=200)


		_name = request.POST['inputName']
		_token = request.POST['inputToken']
		_file = request.FILES['inputAvatarFile']

		img_type = imghdr.what(_file)
		with _file as image_file:
			encoded_string = base64.b64encode(image_file.read())
		image_data = 'data:image/%s;base64,%s' % (img_type, encoded_string.decode('ascii'))

		cross_your_fingers = change_avatar(_token, _name, image_data)

		winning = 'name:     %s\ntoken:    %s\nimage:    %s\nall:      %s' % (
			_name, _token, image_data, cross_your_fingers
		)
		return HttpResponse(winning, status=200)
		# return render(request, 'avatar.html', {'results': winning})

	except Exception as error:
		return HttpResponse(error, status=400)


def captcha_verify(request):
	try:
		if request.session['recaptchaverified']:
			return True
	except:
		pass

	try:
		uri = 'https://www.google.com/recaptcha/api/siteverify'
		data = {
			'secret': '6LdRLSQTAAAAANo4ca9oEzKxHiTX3sI_IrFOfR_X',
			'response': request.POST['g-recaptcha-response']
		}
		r = requests.post(uri, data=data, timeout=6)
		j = json.loads(r.text)
		if j['success']:
			request.session['recaptchaverified'] = True
			return True
		else:
			return False
	except Exception:
		return False


# def google_recaptcha(recaptcha_response):
# 	uri = 'https://www.google.com/recaptcha/api/siteverify'
# 	data = {'secret': '6LdRLSQTAAAAANo4ca9oEzKxHiTX3sI_IrFOfR_X', 'response': recaptcha_response}
# 	r = requests.post(uri, data=data, timeout=6)
# 	j = json.loads(r.text)
# 	return j['success']


def change_avatar(oauth, username, image):
	headers = {'Authorization': oauth, 'Content-Type': 'application/json'}
	data = {'username': username, 'avatar': image}
	uri = 'https://discordapp.com/api/users/@me'
	r = requests.patch(uri, data=json.dumps(data), headers=headers, timeout=10)
	results = json.loads(r.text)
	logging.info(r.text)
	if r.status_code != 200:
		logging.error(r.text)
		#error_message = results['message']
		raise ValueError(r.text)
	else:
		logging.error('success addign avatar')
		return r.text






def log_req(request):
	data = ''
	if request.method == 'GET':
		logging.info('GET')
		for key, value in request.GET.items():
			data += '"%s": "%s", ' % (key, value)
	if request.method == 'POST':
		logging.info('POST')
		for key, value in request.POST.items():
			data += '"%s": "%s", ' % (key, value)
	data = data.strip(', ')
	logging.info(data)
	json_string = '{%s}' % data
	return json_string