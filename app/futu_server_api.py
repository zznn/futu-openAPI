# -*- coding: utf-8 -*-
try:
	from urllib import urlencode
except ImportError:
	from urllib.parse import urlencode
from datetime import datetime, timedelta
from myutility import gen_signature
from urllib.parse import quote,quote_plus
from db import get_token
import urllib
import json
import random
import time
import requests
import configparser

config = configparser.ConfigParser()
config.read('./conf/appinfo.ini')

def check_type(request):
	if isinstance(request, dict):
		return request
	elif isinstance(request.json(), dict):
		return request.json()
	else:
		return request.text

class client(object):
	"""docstring for client"""
	def __init__(self, app_account, card, appid):
		super(client, self).__init__()
		for item in config.sections():
			if item == appid:
				self.appid = item
				self.appsecret = config[item]['app_secret']
				self._cert = (config[item]['client_cer'], config[item]['client_key'])
			else:
				pass
		self.app_account = app_account
		self.card = card
		self._token = get_token(appid, card, False)
		self._tradetoken = get_token(appid, card, True)

	def gen_headers(self, isTrade, data, url, method, lang = 'sc'):
		'''
		isTrade字段用于判断是否携带交易授权令牌
		'''
		if not self._token:
			return {'result_code':2, 'error_msg':'didn\'t get accesstoken'}

		myheaders = {
			'Accept':'application/vnd.futu5.openapi-v1+json',
			'Content-Type':'application/vnd.futu5.openapi-v1+json',
			'X-Futu-Oauth-Appid':self.appid,
			'X-Futu-Oauth-App-Account':self.app_account,
			'X-Futu-Oauth-Nonce':random.randint(1, 100000),
			'X-Futu-Oauth-Accesstoken':self._token,
			'X-Futu-Oauth-Signature-Method':'HMAC-SHA1',
			'X-Futu-Oauth-Timestamp':int(time.time()),
			'X-Futu-Oauth-Version':'1.0',
			'X-Futu-Oauth-Lang':lang #可预留接口扩展
		}

		if isTrade:
			if self._tradetoken:
				myheaders['X-Futu-Oauth-Tradetoken'] = self._tradetoken
			else:
				return {'result_code':2, 'error_msg':'didn\'t get tradetoken'}
			
		sigheaders = {
			'X-Futu-Oauth-Appid':myheaders['X-Futu-Oauth-Appid'],
			'X-Futu-Oauth-App-Account':myheaders['X-Futu-Oauth-App-Account'],
			'X-Futu-Oauth-Nonce':myheaders['X-Futu-Oauth-Nonce'],
			'X-Futu-Oauth-Accesstoken':myheaders['X-Futu-Oauth-Accesstoken'],
			'X-Futu-Oauth-Signature-Method':myheaders['X-Futu-Oauth-Signature-Method'],
			'X-Futu-Oauth-Timestamp':myheaders['X-Futu-Oauth-Timestamp'],
			'X-Futu-Oauth-Version':'1.0',
			'X-Futu-Oauth-Lang':myheaders['X-Futu-Oauth-Lang']
		}

		if isTrade:
				sigheaders['X-Futu-Oauth-Tradetoken'] = self._tradetoken

		sig = gen_signature(sigheaders, data, url, method, self.appsecret, self._token)
		myheaders['X-Futu-Oauth-Signature'] = sig
		return myheaders

	def get(self, url, data = None, lang = 'sc'):
		'''
		GET请求，获取数据
		'''
		headers = self.gen_headers(False, data, url, 'GET', lang)
		if 'error_msg' in headers:
			return headers
		else:
			return requests.get(url, params = data, headers = headers, cert = self._cert)

	def post(self, url, data = None):
		'''
		POST请求，修改数据
		'''
		headers = self.gen_headers(True, data, url, 'POST')
		if 'error_msg' in headers:
			return headers
		else:
			return requests.post(url, data = json.dumps(data), headers = headers, cert = self._cert)


	def put(self, url, data = None):
		'''
		PUT请求是幂等的，重复执行多次，效果一样
		'''
		headers = self.gen_headers(True, data, url, 'PUT')
		if 'error_msg' in headers:
			return headers
		else:
			return requests.put(url, data = json.dumps(data), headers = headers, cert = self._cert)


	def get_trade_token(self, trade_pswd):
		'''
		验证交易密码，获取tradetoken
		'''
		data = {
				'trade_pswd':trade_pswd
			}
		url = 'https://openapi.futu5.com/auth_trade_pswd'
		headers = self.gen_headers(False, data, url, 'POST')
		if 'error_msg' in headers:
			return headers
		req = requests.post(url,
				 data = json.dumps(data),
				 headers = headers,
				 cert = self._cert)
		return check_type(req)
		
		
	def get_account_detail(self):
		'''
		获取账户详情
		'''
		req = self.get('https://tradeopen.futu5.com/account')
		return check_type(req)


	def get_account_cash(self):
		'''
		获取现金数据
		'''
		req = self.get('https://tradeopen.futu5.com/account/cash')
		return check_type(req)


	def get_account_portfolio(self):
		'''
		获取当前账户股票持仓数据
		'''
		req = self.get('https://tradeopen.futu5.com/account/portfolio')
		return check_type(req)


	def get_list_orders(self, date_begin = '', date_end = ''):
		'''
		获取订单数据
		datetime.now().date().strftime('%Y%m%d')
		'''
		url = 'https://tradeopen.futu5.com/orders?date_begin={0}&date_end={1}'.format(date_begin, date_end)

		req = self.get(
			url,
			lang = 'tc'
		)
		return check_type(req)


	def get_list_trades(self):
		'''
		获取账户今日成交列表
		'''
		req =  self.get('https://tradeopen.futu5.com/trades')
		return check_type(req)


	def place_order(self, code, quantity, price, side, ltype):
		'''
		下订单
		'''
		req = self.post(
			'https://tradeopen.futu5.com/orders',
		 	{
				'code':code, 
				'quantity':quantity, 
				'price':price, 
				'side':side, 
				'type':ltype 
			}
		)
		return check_type(req)


	def change_order(self, order_id, quantity, price):
		'''
		修改订单
		'''
		url = 'https://tradeopen.futu5.com/orders/' + str(order_id)
		req = self.put(
			url,
			{
				'action':1,
				'quantity':quantity, 
				'price':price 
			})
		return check_type(req)


	def cancel_order(self, order_id):
		'''
		取消订单，对还没有成交的订单撤单
		'''
		url = 'https://tradeopen.futu5.com/orders/' + str(order_id)
		req = self.put(
			url,
			{
				'action':0
			}
		)
		return check_type(req)

