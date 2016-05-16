# 富途开放-交易接口

for 第三方开发者

author: july

<!-- MarkdownTOC -->
- [Token API 令牌接口](#token)
    - [save_token 保存令牌](#save_token)
    - [delete_token 删除令牌](#delete_token)
    - [trade_token 交易令牌](#trade_token)
- [Accounts API 账户接口](#accounts_api)
    - [get_account_detail 获取账户详情](#get_account_detail)
    - [get_account_cash 获取账户现金数据](#get_account_cash)
    - [get_account_portfolio 获取账户持仓](#get_account_portfolio)
    - [get_list_orders 获取订单列表](#get_list_orders)
    - [get_list_trades 获取成交列表](#get_list_trades)
- [Order API 交易接口](#order_api)
    - [place_order 下单](#place_order)
    - [change_order 修改订单](#change_order)
    - [cancle_order 撤单](#cancel_order)

- [附录](#附录)
    - [接口中涉及的数据结构](#接口中涉及的数据结构)

<!-- /MarkdownTOC -->

## <a name='token'></a>Token API 令牌接口
###<a name='save_token'></a>save_token 
####功能说明
将accesstoken保存到数据库，并与账户及卡号绑定
####URL
http://127.0.0.1:8888/ap1/v1/save_token
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| app_account    | string |   第三方帐号     |
| token      | string |   获取的accesstoken  |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| text       | string |     牛牛账户中卡号的描述 |
| appid     | string |  富途分配的第三方应用ID  |
| market    | string |      股票市场         |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001",		
	"market":"us",
 	"token":"rxu6CEYMSBrB6zSyOKjjk8j-17wRYw0qANky1xHuXPMpqUSVQaUotoBK1LV7OhMR",
 	"text":"美股现金账户"
}
```

####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| DB_result   | string |   保存是否成功     |
####返回数据示例
成功：
```python
{
    "DB_result":"token删除成功" 
}
```
失败：
```python
{
    "DB_result":"token保存失败"
}
```
**备注：若未save_token而直接调用其他接口(除了delete_token)，将返回如下信息**
```python
{
    "ClientWarning":"didn't get accesstoken" 
}
```

###<a name='delete_token'></a>delete_token 
####功能说明
从数据库中删除账户及关联的令牌
####URL
http://127.0.0.1:8888/ap1/v1/delete_token
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| app_account    | string |   第三方帐号     |
| appid     | string |  富途分配的第三方应用ID  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "appid":"10000001"
}
```

####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| DB_result   | string |   删除是否成功     |
####返回数据示例
成功：
```python
{
    "DB_result":"token删除成功" 
}
```
失败：
```python
{
    "DB_result":"token删除失败" 
}
```

###<a name='trade_token'></a>trade_token
####功能说明
验证交易密码，获取tradetoken
####URL
http://127.0.0.1:8888/ap1/v1/tradetoken
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
| trade_pswd | string |  交易密码  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001",
    "trade_pswd": "asdasd"
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| trade_token | string|  tradetoken   |
####返回数据示例
成功：
```python
{
    "result_code": 0,
    "error_msg": "",
    "data": {
        "trade_token": "Ij0UYMooWbBqvyNllTXAysfA1KOutFbzQLwCmUK2GiAaOUmlFWEH_Cg_uf7pHwhgOcf0-MLSurDZ                         goL4F73gxg=="
    }
}
```
失败：
```python
{
    "result_code": 1102,
    "error_msg": "交易密码错误"
}
```
**备注：若未获得tradetoken而直接调用3种交易接口，将返回如下信息**
```python
{
    "ClientWarning":"didn't get tradetoken" 
}
```

## <a name='accounts_api'></a>Accounts API 账户接口

###<a name='get_account_detail'></a>get_account_detail 
####功能说明
获取当前账户详情，如账户类型、状态、所属市场
####URL
http://127.0.0.1:8888/ap1/v1/account
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001"
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| type   | string |   账户类型。可能值: CASH(现金账户), MARGIN(保证金账户)     |
| state      | string |  账户状态。可能值: OPENING(正在开户), OPENED(已开户), CLOSED(已销户) |
| market    | string |  所属市场。可能值：HK(港股市场)，US(美股市场) |
####返回数据示例
```python
{
    'result_code': 0,
    'error_msg': "",
    'data': {
        'account': {
            'type': 'CASH',
            'state': 'OPENED',
            'market': 'HK'
        }
    }
}
```

###<a name='get_account_cash'></a>get_account_cash
####功能说明
获取当前账户现金数据
####URL
http://127.0.0.1:8888/ap1/v1/account/cash
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001"
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| cash    | CashPosition |   现金数据，CashPosition数据类型见后面说明    |
####返回数据示例
```python
{
    'result_code': 0,
    'error_msg': '',
    'data': {
        'cash': {
            'balance': '10030',
            'debit_recover': '0',
            'drawable': '0',
            'frozen_power': '0',
            'loan_max': '100000',
            'power': '100000',
            'prev_asset_value': '10030',
            'prev_balance': '10030',
            'prev_stock_value': '0',
            'stock_margin_value': '153000',
            'stock_value': '310200',
            'today_profit': '0',
            'today_profit_ratio': 0,
            'today_settled': 0,
            'today_turnover': '0',
            'total_asset_value': '320230',
            'trade_count': 0,
            'type': 'MARGIN',
        }
    }
}
```

###<a name='get_account_portfolio'></a>get_account_portfolio
####功能说明
获取当前账户股票持仓数据
####URL
http://127.0.0.1:8888/ap1/v1/account/portfolio
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001"
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| portfolio   | StockPosition |   股票持仓数据，StockPosition数据类型见后面说明   |
####返回数据示例
```python
{
    "result_code": 0,
    "error_msg": "",
    "data": {
        "portfolio": [
            {
                "code": 90008,
                "name": "Futu&stock 8",
                "cost_price": "23",
                "cost_price_invalid": "",
                "power": 8000,
                "profit": "7600",
                "profit_ratio": 0.041304347826087,
                "profit_ratio_invalid": "",
                "quantity": 8000,
                "today_long_avg_price": "0",
                "today_long_shares": 0,
                "today_long_turnover": "0",
                "today_profit": "0",
                "today_short_avg_price": "0",
                "today_short_shares": 0,
                "today_short_turnover": "0",
                "today_turnover": "0",
                "value": "191600",
                "value_price": "23.95"
            },
            {
                "code": 90009,
                "name": "Futu&stock 9",
                "cost_price": "23",
                "cost_price_invalid": "",
                "power": 8000,
                "profit": "7600",
                "profit_ratio": 0.041304347826087,
                "profit_ratio_invalid": "",
                "quantity": 1000,
                "today_long_avg_price": "0",
                "today_long_shares": 0,
                "today_long_turnover": "0",
                "today_profit": "0",
                "today_short_avg_price": "0",
                "today_short_shares": 0,
                "today_short_turnover": "0",
                "today_turnover": "0",
                "value": "41234",
                "value_price": "132.95"
            }
        ]
    }
}
```

###<a name='get_list_orders'></a>get_list_orders
####功能说明
获取当前用户当前账户订单数据
####URL
http://127.0.0.1:8888/ap1/v1/get_list_orders
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |   必填 | 
| --------   | :-----: | :----:  |:----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
|date_begin  | string |  起始日期，如20151101，默认为当天日期;  | 否 |
|date_end   | string |  结束日期，如20151105，默认为当天日期  | 否  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001",
    "date_begin":"",
    "date_end":""
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| order   | Order |   订单列表，Order数据类型见后面说明   |
####返回数据示例
```python
{
    "result_code": 0,
    "error_msg": "",
    "data": {
        "order": [
            {
                "order_id": "1234561",
                "avg_price": "142.5",
                "code": "00700",
                "name": "腾讯",
                "created": 1446618508,
                "enable": 1,
                "last_err": 0,
                "matched_quantity": 0,
                "modified": 1446618536,
                "price": "142",
                "quantity": 1000,
                "side": "SELL",
                "state": 1,
                "type": "E",
                "last_err_text": "",
                "side_text": "卖",
                "type_text": "普通",
                "state_text": "等待成交"
            },
            {
                "order_id": "1234562",
                "avg_price": "12.5",
                "code": "02208",
                "name": "金风科技",
                "created": 1446618608,
                "enable": 1,
                "last_err": 0,
                "matched_quantity": 0,
                "modified": 1446618636,
                "price": "13",
                "quantity": 1000,
                "side": "SELL",
                "state": 1,
                "type": "E",
                "last_err_text": "",
                "side_text": "买",
                "type_text": "普通",
                "state_text": "已成交"
            }
        ]
    }
}
```

###<a name='get_list_trades'></a>get_list_trades
####功能说明
获取账户今日成交列表，一个订单可能会对应多个成交。成交可能没有对应的订单，比如线下的成交
####URL
http://127.0.0.1:8888/ap1/v1/get_list_trades
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |  
| --------   | :-----: | :----:  |:----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001",
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| trade  | Trade |  成交列表，Trade数据类型见后面说明   |
####返回数据示例
```python
{
    "result_code": 0,
    "error_msg": "",
    "data": {
        "trade": [
            {
                "code": 90008,
                "name": "Futu&stock 8",
                "counter_broker_id": 5001,
                "created": 1446620585,
                "order_created": 1446620585,
                "order_id": "23452345",
                "order_modified": 1446620585,
                "price": "30.5",
                "quantity": 200,
                "side": "SELL",
                "id": 16,
                "side_text": "卖"
            }
        ]
    }
}
```
