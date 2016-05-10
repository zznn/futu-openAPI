import requests

# ipport = '127.0.0.1:5000'
ipport = '192.168.111.128:8080'

#美股现金
app_account = 'aa@bb.com'
card = '1001100200100059'
appid = '10000001'

# #港股保证金账户
# app_account = 'aa@bb.com'
# card = '1001100100100059'
# appid = '10000001'

# #港股现金账户
# app_account = 'aa@bb.com'
# card = '1001100120012143'
# appid = '10000001'

# #保存accesstoken
# r = requests.post(
# 	"http://%s/ap1/v1/save_token" % ipport, 
# 	json={'app_account':app_account,
# 		'appid':appid,
# 		'market':'us',
# 		'token':'rxu6CEYMSBrB6zSyOKjjk8j-17wRYw0qANky1xHuXPMpqUSVQaUotoBK1LV7OhMR',
# 		'card':card,
# 		'text':'美股现金账户'
# 		}
# 	)
# print(r.text)

# #获取交易密码
# r = requests.post(
# 	"http://%s/api/v1/tradetoken" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'trade_pswd':'asdasd'
# 		}
# 	)
# print(r.text)

# #删除token
# r = requests.post(
# 	"http://%s/api/v1/delete_token" % ipport, 
# 	json={'app_account':app_account,
# 		'appid':appid,
# 		}
# 	)
# print(r.text)


# #获取账户信息
# r = requests.post(
# 	"http://%s/api/v1/account" % ipport, 
# 	json={'app_account':app_account,
# 		'card':card,
# 		'appid':appid
# 		}
# 	)
# print(r.text)

# #获取账户现金
# r = requests.post(
# 	"http://%s/api/v1/account/cash" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid
# 		}
# 	)
# print(r.text)

# #获取账户持仓
# r = requests.post(
# 	"http://%s/api/v1/account/portfolio" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid
# 		}
# 	)
# print(r.text)


# #获取订单列表
# r = requests.post(
# 	"http://%s/api/v1/get_list_orders" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'date_begin':'',
# 		'date_end':''
# 		}
# 	)
# print(r.text)

# #获取交易列表
# r = requests.post(
# 	"http://%s/api/v1/get_list_trades" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid
# 		}
# 	)
# print(r.text)

# #美股限价下单
# r = requests.post(
# 	"http://%s/api/v1/place_order" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'code':'BABA',
# 		'quantity':1000,
# 		'price':90,
# 		'side':'BUY',
# 		'type':'LIMIT'
# 		}
# 	)
# print(r.text)

# #美股市价下单
# r = requests.post(
# 	"http://%s/api/v1/place_order" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'code':'BABA',
# 		'quantity':500,
# 		'price':0,
# 		'side':'BUY',
# 		'type':'MARKET'
# 		}
# 	)
# print(r.text)

# #港股下单
# r = requests.post(
# 	"http://%s/api/v1/place_order" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'code':'90008',
# 		'quantity':100,
# 		'price':1.5,
# 		'side':'BUY',
# 		'type':'E'
# 		}
# 	)
# print(r.text)

# #改单
# r = requests.post(
# 	"http://%s/api/v1/change_order" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'order_id':'odr_us_sht_trd_svc_51_20160510_100059_1',
# 		'quantity':1000,
# 		'price':80
# 		}
# 	)
# print(r.text)

# #撤单
# r = requests.post(
# 	"http://%s/api/v1/cancle_order" % ipport, 
# 	json={
# 		'app_account':app_account,
# 		'card':card,
# 		'appid':appid,
# 		'order_id':'odr_us_sht_trd_svc_51_20160510_100059_1'
# 		}
# 	)
# print(r.text)







# import time
# def test(second):
# 	for x in range(1,5):
# 		time.sleep(second)
# 		r = requests.post(
# 			"http://127.0.0.1:5000/api/v1/account/cash", 
# 			json={
# 				'app_account':app_account,
# 				'card':card,
# 				'appid':appid
# 				}
# 			)
# 		print(r.text)

# test(3)
