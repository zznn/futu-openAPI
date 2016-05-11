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
config.read('./conf/default.conf')

# class clientException(Exception):
# 	"""docstring for clientException"""
# 	def __init__(self, arg):
# 		super(clientException, self).__init__()
# 		print("错误原因 => {}".format(arg))
# 		self.arg = arg
		

# def check_error(myjson):
# 	'''
# 	检测富途API接口返回值中是否包含错误的返回码
# 	成功返回0，失败返回1
# 	'''
# 	if myjson:
# 		print('返回的jsom数据:')
# 		print(myjson)
# 	else:
# 		print('未获得数据')

# 	if 'result_code' in myjson and myjson['result_code'] != 0:
# 		raise clientException('{}:{}'.format(myjson['result_code'],myjson['error_msg']))
# 	return myjson

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

		# self.appid = 10000001 #申请的第三方id
		# self.appsecret = '!UMC+RztTD5De9ZV4sg6H6eUURJdyzlL' #申请的第三方secret
		#港股保证金授权令牌
		# self._token = 'YHTNALMOm6IqkKsoOmxwLBMEySRhl6TrPnMLx18aySHOMoAPdTsfk82HauR1Rl5s'
		#港股现金授权令牌
		# self._token = 'nsTYReqbLXI52yV56lpKIgGaFjWboSDfmq4xHlH1J0z_NMgggni8skwu0oGELKgJ'
		# 美股现金授权令牌
		# self._token = 'rxu6CEYMSBrB6zSyOKjjk-Ja1d_TibK7lO-6pMZMPlgpqUSVQaUotoBK1LV7OhMR' 

		# self._tradetoken = 'zFHNNNQNbav_hWatroPbEW47gYk7lIdMO0yUmHWwGzD-D6qYT1Vu1VQZU5BqtK0Q4wuUyXOyRvc24HLSX_iOkg=='
		#self._tradetoken_expires_at = None #交易授权令牌
		# self._cert = ('d:/Program Files/Sublime Text 3/openAPIdemo/july_client.pem', 'd:/Program Files/Sublime Text 3/openAPIdemo/client.key')


	def gen_headers(self, isTrade, data, url, method, lang = 'sc'):
		'''
		isTrade字段用于判断是否携带交易授权令牌
		'''
		if not self._token:
			return {'ClientWarning':'didn\'t get accesstoken'}

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
				return {'ClientWarning':'didn\'t get tradetoken'}
			
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
		# print('发送的完整的http头部信息:')
		# print(myheaders)
		# print('发送的完整的http数据:')
		# print(data)
		return myheaders

	def get(self, url, data = None, lang = 'sc'):
		'''
		GET请求，获取数据
		'''
		headers = self.gen_headers(False, data, url, 'GET', lang)
		if 'ClientWarning' in headers:
			return headers
		else:
			return requests.get(url, params = data, headers = headers, cert = self._cert)

	def post(self, url, data = None):
		'''
		POST请求，修改数据
		'''
		headers = self.gen_headers(True, data, url, 'POST')
		if 'ClientWarning' in headers:
			return headers
		else:
			return requests.post(url, data = json.dumps(data), headers = headers, cert = self._cert)


	def put(self, url, data = None):
		'''
		PUT请求是幂等的，重复执行多次，效果一样
		'''
		headers = self.gen_headers(True, data, url, 'PUT')
		if 'ClientWarning' in headers:
			return headers
		else:
			return requests.put(url, data = json.dumps(data), headers = headers, cert = self._cert)
		# print(req.url)
		

	# def grant_token(self):
	# 	'''
	# 	获得Access Token
	# 	例如：https://open.futu5.com/oauth/show?app_id=10000001&app_account=aa@bb.com&market=hk
	# 	'''
	# 	req = requests.get(
	# 		'https://open.futu5.com/oauth/show',
	# 		{
	# 			'app_id':self.appid, 
	# 			'app_account':self.app_account, 
	# 			'market':self.market
	# 		}
	# 	)
	# 	print(req.content)


	# @property
	# def token(self):
	# 	'''
	# 	验证Access Token是否有效，并设置Token过期时间
	# 	'''
	# 	if self._token:
	# 		# now = datetime.now()
	# 		# if self._token_expires_at > now :
	# 		return self._token
	# 	myjson = self.grant_token()
	# 	# self._token_expires_at = datetime.now() + timedelta(days = 90)
	# 	self._token = myjson['accesstoken']
	# 	self.text = myjson['text']
	# 	self.card = myjson['card']
	# 	return self._token

	def get_trade_token(self, trade_pswd):
		'''
		验证交易密码，获取tradetoken
		'''
		data = {
				'trade_pswd':trade_pswd #'asdasd'
			}
		url = 'https://sandbox-openapi.futu5.com/auth_trade_pswd'
		headers = self.gen_headers(False, data, url, 'POST')
		if 'ClientWarning' in headers:
			return headers
		req = requests.post(url,
				 data = json.dumps(data),
				 headers = headers,
				 cert = self._cert)
		return check_type(req)
		# print(req.text)
		#myjson = req.json()
		# if check_error(myjson):
			# self._tradetoken = myjson['data']['trade_token']
		#return myjson

	# @property
	# def trade_token(self):
	# 	if self._tradetoken:
	# 		# now = datetime.now()
	# 		# if self._token_expires_at > now :
	# 		return self._tradetoken
	# 	myjson = self.get_trade_token()
	# 	# self._tradetoken_expires_at = datetime.now() + timedelta(hours = 8)
	# 	self._tradetoken = myjson['trade_token']
	# 	return self._tradetoken

	def get_account_detail(self):
		'''
		获取账户详情
		'''
		req = self.get('https://sandbox-tradeopen.futu5.com/account')
		# print(req.text)
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson  

	def get_account_cash(self):
		'''
		获取现金数据
		'''
		req = self.get('https://sandbox-tradeopen.futu5.com/account/cash')
		# print(req.text)
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

	def get_account_portfolio(self):
		'''
		获取当前账户股票持仓数据
		'''
		req = self.get('https://sandbox-tradeopen.futu5.com/account/portfolio')
		# print(req.text)
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

	def get_list_orders(self, date_begin = '', date_end = ''):
		'''
		获取订单数据
		datetime.now().date().strftime('%Y%m%d')
		'''
		url = 'https://sandbox-tradeopen.futu5.com/orders?date_begin={0}&date_end={1}'.format(date_begin, date_end)

		req = self.get(
			url,
			lang = 'tc'
		)
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

	def get_list_trades(self):
		'''
		获取账户今日成交列表
		'''
		req =  self.get('https://sandbox-tradeopen.futu5.com/trades')
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

	def place_order(self, code, quantity, price, side, ltype):
		'''
		下订单
		'''
		req = self.post(
			'https://sandbox-tradeopen.futu5.com/orders',
		 	{
				'code':code, 
				'quantity':quantity, 
				'price':price, 
				'side':side, 
				'type':ltype 
			}
		)
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

	def change_order(self, order_id, quantity, price):
		'''
		修改订单
		'''
		url = 'https://sandbox-tradeopen.futu5.com/orders/' + str(order_id)
		req = self.put(
			url,
			{
				'action':1,
				'quantity':quantity, 
				'price':price 
			})
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

	def cancel_order(self, order_id):
		'''
		取消订单，对还没有成交的订单撤单
		'''
		url = 'https://sandbox-tradeopen.futu5.com/orders/' + str(order_id)
		req = self.put(
			url,
			{
				'action':0
			}
		)
		return check_type(req)
		# myjson = req.json()
		# if check_error(myjson):
		# return myjson

# cc = client('aa@bb.com', '1001100200100059', '10000001') #us hk
# cc = client('aa@bb.com', 'hk', 'app1')

# cc.grant_token()

# cc.get_account_detail()
# cc.get_account_cash() 
# cc.get_account_portfolio() 

# cc.get_list_orders() 
# cc.get_list_trades() #内部错误bug

# cc.get_trade_token('asdasd') #内部错误
# print('TRADETOKEN is {0}'.format(cc._tradetoken))

# cc.place_order('BABA', 100, 0, 'BUY', 'MARKET') #美股
# cc.place_order('BABA', 2000, 90, 'BUY', 'LIMIT')
# cc.change_order('odr_us_sht_trd_svc_51_20160415_100059_124', 200, 100)
# cc.cancel_order('odr_us_sht_trd_svc_51_20160415_100059_63')



# cc.place_order('90008', 100, 1.5, 'BUY', 'E') #港股
# cc.change_order(12, 200, 2.5)
# cc.cancel_order(12)
