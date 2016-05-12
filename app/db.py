# -*- coding: utf-8 -*-
import pymysql.cursors
import logging
import logging.config

logging.config.fileConfig('./conf/logging.conf')
db_logger = logging.getLogger()


config = {
	'host':'172.17.0.2',
	'port':3306,
	'user':'root',
	'password':'123456',
	'db':'test',
	'charset':'utf8',
}

connection = pymysql.connect(**config)

def get_token(appid, card, isTrade):
	try:
		connection.ping()
	except Exception as e:	
		connection = pymysql.connect(**config)
	finally:
		pass

	if isTrade is True:
		token_type = 'tradetoken'
	else:
		token_type = 'accesstoken'
	try:
		with connection.cursor() as cursor:
			sql = 'select %s from account_token ' % token_type 
			sql += 'where card = %s and appid = %s'
			cursor.execute(sql, (card, appid))
			result = cursor.fetchone()
		connection.commit()
		if result is not None and result[0] is not None:
				db_logger.info('%s SUCCESS' % token_type)
				return result[0]
		else:
			db_logger.info('%s FAIL' % token_type)
			return None	
	except Exception as e:
		connection.rollback()
		db_logger.error('get FAIL ,following as:%s' % str(e), exc_info = True)
	finally:
		connection.close()


def save_update_token(account, appid, market, token, card, isTrade, card_desc = None):
	try:
		connection.ping()
	except Exception as e:	
		connection = pymysql.connect(**config)
	finally:
		pass

	if isTrade is True:
		token_type = 'tradetoken'
	else:
		token_type = 'accesstoken'
	try:
		with connection.cursor() as cursor:
			operate = ''
			sql = 'select id from account_token where card = %s and appid = %s'
			cursor.execute(sql, (card, appid))
			result = cursor.fetchone()
			if result is None:
				operate = 'insert'
				sql1 = 'insert into account_token(account, %s, card, appid, market, card_infor)' % token_type
				sql1 += ' values(%s, %s, %s, %s, %s, %s)'  
				cursor.execute(sql1, (account, token, card, appid, market, card_desc))
			else:
				operate = 'update'
				sql = 'update account_token set %s =' % token_type
				sql += '%s where card = %s and appid = %s'
				cursor.execute(sql, (token, card, appid))
		db_logger.info('%s SUCCESS' % operate)
		connection.commit()
		return 'success'
	except Exception as e:
		connection.rollback()
		db_logger.error('%s FAIL，following as:%s' % (operate, str(e)), exc_info = True)
		return 'failure'
	finally:
		connection.close()

def delete_tokens(account, appid):
	global operate
	try:
		connection.ping()
	except Exception as e:	
		connection = pymysql.connect(**config)
	finally:
		pass

	try:
		with connection.cursor() as cursor:
			operate = 'delete'
			sql = 'delete from account_token where account = %s and appid = %s'
			cursor.execute(sql, (account, appid))
		db_logger.info('%s SUCCESS' % operate)
		connection.commit()
		return 'success'
	except Exception as e:
		connection.rollback()
		db_logger.error('%s FAIL，following as:%s' % (operate, str(e)), exc_info = True)
		return 'failure'
	finally:
		connection.close()
	
	
