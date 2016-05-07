# -*- coding: utf-8 -*-
import hashlib,hmac
import json
import random
import base64
import urllib
from urllib.parse import quote_plus

def gen_signature(header, body, url, method, app_secret, accesstoken):
	if body:
		sign = dict(header, **body)
	else:
		sign = header
	
	dic = sorted(sign.items(), key = lambda d:d[0]) 
	params = method + '&' + urllib.parse.quote_plus(url)

	for (key, value) in dic:
		params += '&' + key + '=' + urllib.parse.quote_plus(str(value))
	signkey = app_secret + '&' + accesstoken
	h = base64.b64encode(hmac.new(signkey.encode('utf-8'), params.encode('utf-8'), hashlib.sha1).digest())
	return h.decode('utf-8')

