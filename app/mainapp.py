# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, abort, make_response
from futu import *
from db import save_update_token
from db import delete_tokens
import logging
import logging.config
import json

app = Flask(__name__)

logging.config.fileConfig('./conf/logging.conf')
no_db_logger = logging.getLogger()

def check_parameters(pjson):
	if not pjson or not 'app_account' in pjson or not 'card' in pjson or not 'appid' in pjson:
		no_db_logger.info('No Parameter')
		abort(400)
	cli = {'account':pjson['app_account'], 'card':pjson['card'], 'appid':pjson['appid']}
	return client(cli['account'], cli['card'], cli['appid'])

def log_handler(myjson, mytitle):
	if 'ClientWarning' in myjson:
		return '%s' % myjson['ClientWarning']
	elif myjson['result_code'] == 0:
		return 'SUCCESS' 
	else:
		return 'FAIL ,REASON OF FAILURE:%s ,PARAMETER:%s' % (myjson['error_msg'], request.json)


@app.route('/')
def hello_world():
	no_db_logger.info('server start#####')
	return 'hello 22222222 world!'


@app.route('/api/v1/tradetoken', methods=['POST'])
def trade_token():
	trade_pswd = request.json['trade_pswd']
	account = request.json['app_account']
	card = request.json['card']
	appid = request.json['appid']
	cc = check_parameters(request.json)
	message = cc.get_trade_token(trade_pswd)
	if 'ClientWarning' in message:
		no_db_logger.info('didn\'t get accesstoken')
		return json.dumps(message)
	if message['result_code'] == 0:
		token = message['data']['trade_token']
		save_update_token(account, appid, None, token, card, True)
	return jsonify(**message)



@app.route('/api/v1/account', methods=['POST'])
def get_account_detail():
	cc = check_parameters(request.json)
	message = cc.get_account_detail()
	logtext = log_handler(message, '获取账户信息')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)
	


@app.route('/api/v1/account/cash', methods=['POST'])
def get_account_cash():
	cc = check_parameters(request.json)
	message = cc.get_account_cash()
	logtext = log_handler(message, '获取账户现金')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/api/v1/account/portfolio', methods=['POST'])
def get_account_portfolio():
	cc = check_parameters(request.json)
	message = cc.get_account_portfolio()
	logtext = log_handler(message, '获取账户持仓')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/api/v1/get_list_orders', methods=['POST'])
def get_list_orders():
	date_begin = request.json['date_begin']
	date_end = request.json['date_end']
	cc = check_parameters(request.json)
	message = cc.get_list_orders()
	logtext = log_handler(message, '获取订单列表')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/api/v1/get_list_trades', methods=['POST'])
def get_list_trades():
	cc = check_parameters(request.json)
	message = cc.get_list_trades()
	logtext = log_handler(message, '获取交易列表')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/api/v1/place_order', methods=['POST'])
def place_order():
	code = request.json['code']
	quantity = request.json['quantity']
	price = request.json['price']
	side = request.json['side']
	ltype = request.json['type']
	cc = check_parameters(request.json)
	message = cc.place_order(code, quantity, price, side, ltype)
	logtext = log_handler(message, '下单')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/api/v1/change_order', methods=['POST'])
def change_order():
	order_id = request.json['order_id']
	quantity = request.json['quantity']
	price = request.json['price']
	cc = check_parameters(request.json)
	message = cc.change_order(order_id, quantity, price)
	logtext = log_handler(message, '改单')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/api/v1/cancle_order', methods=['POST'])
def cancle_order():
	order_id = request.json['order_id']
	cc = check_parameters(request.json)
	message = cc.cancel_order(order_id)
	logtext = log_handler(message, '撤单')
	no_db_logger.info(logtext)
	return json.dumps(message, ensure_ascii=False)


@app.route('/ap1/v1/save_token', methods=['POST'])
def save_token():
	account = request.json['app_account']
	appid = request.json['appid']
	market = request.json['market']
	token = request.json['token']
	card = request.json['card']
	card_desc = request.json['text']
	DB_result = save_update_token(account, appid, market, token, card, False, card_desc)
	if DB_result == 'success':
		no_db_logger.info('token save success')
		return json.dumps({'DB_result':'token保存成功'}, ensure_ascii=False)
	else:
		no_db_logger.info('token save fail')
		return json.dumps({'DB_result':'token保存失败'}, ensure_ascii=False)
	


@app.route('/api/v1/delete_token', methods=['POST'])
def delete_token():
	appid = request.json['appid']
	account = request.json['app_account']
	DB_result = delete_tokens(account, appid)
	if DB_result == 'success':
		no_db_logger.info('token delete success')
		return json.dumps({'DB_result':'token删除成功'}, ensure_ascii=False)
	else:
		no_db_logger.info('token delete fail')
		return json.dumps({'DB_result':'token删除失败'}, ensure_ascii=False)
	
	
if __name__ == '__main__':
	app.run()
