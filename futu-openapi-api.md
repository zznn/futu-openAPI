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

## <a name='order_api'></a>Order API 交易接口

###<a name='place_order'></a>place_order
####功能说明
在当前账户下订单
####URL
http://127.0.0.1:8888/ap1/v1/place_order
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  |  备注 |
| --------   | :-----: | :----:  |:----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
| stockcode       | string |  股票代码，如00700（港股账户），或BABA（美股账户）  |
| quantity     | int |  数量，如1000  |
| price   | 	double |  价格，如150.5  | 若为美股MARKET市价单，请填0 |
| side      | string | 方向。BUY买入，SELL卖出 |
|type    | string  |  	订单类型。港股和美股不同。港股：E普通订单（增强限价单），A竞价单，I竞价限价单；美股：LIMIT限价单，MARKET市价单  |
####请求参数示例
```python
{
    'app_account':'aa@bb.com',
    'card':'1001100200100059',
    "appid":"10000001",
    "code": "00700",
    "quantity": 1000,
    "price": 150.5,
    "side": "SELL",
    "type": "E"
}
```
####返回数据（JSON格式）
| 参数       | 类型   |  描述  |
| --------   | :-----: | :----:  |
| order_id | string|  订单ID   |
####返回数据示例
```python
{
    "result_code": 0,
    "error_msg": "",
    "data": {
        "order_id": "odr_us_sht_trd_svc_51_20160507_100059_6"
    }
}
```

###<a name='change_order'></a>change_order
####功能说明
对还没成交的订单做修改，仅可修改订单数量和价格
####URL
http://127.0.0.1:8888/ap1/v1/change_order
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  | 
| --------   | :-----: | :----:  |:----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
| order_id      | string |  订单ID  |
| quantity  | 	int |  数量 |
| price    | double | 价格 |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001",
    "order_id": "odr_us_sht_trd_svc_51_20160507_100059_6",
    "quantity": 1000,
    "price": 160.5
}
```
####返回数据（JSON格式）
空
####返回数据示例
成功：
```python
{
    "result_code": 0,
    "error_msg": ""
}
```
失败：
```python
{
    "result_code": 100,
    "error_msg": "资金不足"
}
```

###<a name='cancle_order'></a>cancle_order
####功能说明
对还没成交的订单撤单
####URL
http://127.0.0.1:8888/ap1/v1/cancle_order
####POST请求参数（JSON格式）
| 参数       | 类型   |  描述  | 
| --------   | :-----: | :----:  |:----:  |
| app_account    | string |   第三方帐号     |
| card       | string |  牛牛账户中相应的卡号，例如港股现金卡号，保证金卡号  |
| appid     | string |  富途分配的第三方应用ID  |
| order_id      | string |  订单ID  |
####请求参数示例
```python
{
    "app_account":"aa@bb.com",
    "card":"1001100200100059",
    "appid":"10000001",
    "order_id": 'odr_us_sht_trd_svc_51_20160507_100059_6'
}
```
####返回数据（JSON格式）
空
####返回数据示例
成功：
```python
{
    "result_code": 0,
    "error_msg": ""
}
```
失败：
```python
{
    "result_code": 111,
    "error_msg": "非交易时间"
}
```

## <a name='附录'></a>附录

### <a name='接口中涉及的数据结构'></a>接口中涉及的数据结构
##### <a name='CashPosition'></a>现金仓位 CashPosition

说明：表示客户资产的现金部分。以下金额单位都为0.001元，如10025000表示10025元

字段：

| 名称 | 说明 |
| ---- | ---- |
| balance | 现金结余 |
| debit_recover | 欠款 |
| drawable | 可提金额（暂时不要用这个金额） |
| loan_max | 可使用的最大信贷额度 |
| power | 当前最大购买力 |
| frozen_power | 已冻结购买力。由于下买单等暂时冻结的购买力 |
| prev_asset_value | 上个交易日结算后的资产市值 |
| prev_balance | 上个交易日结算后的现金结余 |
| prev_stock_value | 上个交易日结算后的股票市值 |
| stock_margin_value | 股票抵押额 |
| stock_value | 股票市值 |
| today_profit | 今日交易的盈亏额 |
| today_profit_ratio | 今日交易的盈亏比例。0.1表示10% |
| today_settled | 今天是否已经结算。0表示未结算，1表示已结算 |
| today_turnover | 今日成交额 |
| total_asset_value | 资产总额，含现金和股票市值 |
| trade_count | 今日成交笔数 |

例如:

    {
        "balance": "10030",
        "debit_recover": "0",
        "drawable": "0",
        "frozen_power": "0",
        "loan_max": "100000",
        "power": "100000",
        "prev_asset_value": "10030",
        "prev_balance": "10030",
        "prev_stock_value": "0",
        "stock_margin_value": "153000",
        "stock_value": "310200",
        "today_profit": "0",
        "today_profit_ratio": 0,
        "today_settled": 0,
        "today_turnover": "0",
        "total_asset_value": "320230",
        "trade_count": 0
    }


##### <a name='StockPosition'></a>股票仓位 StockPosition

说明：表示客户资产的股票部分

字段：

| 名称 | 说明 |
| ---- | ---- |
| code | 股票代码 |
| name | 股票名称。使用了请求中指定的语言 |
| cost_price | 成本价（以何种价格卖出才能使本次建仓不亏本） |
| cost_price_invalid | 成本价非法。该字段不为空时表示成本价不可用 |
| on_hold | 由于卖单而暂时冻结的可卖股数 |
| power | 可卖股数 |
| quantity | 持有股数 |
| profit | 自建仓以来的总盈亏额 |
| profit_ratio | 自建仓以来的总盈亏比例 |
| profit_ratio_invalid | 总盈亏比例非法。该字段不为空时表示总盈亏额不可用 |
| today_long_avg_price | 今日平均买入价 |
| today_long_shares | 今日买入股数 |
| today_long_turnover | 今日买入成交额 |
| today_profit | 今日盈亏额。今日不管建仓清仓多少次，所有在这只股票上操作的盈亏额。 |
| today_short_avg_price | 今日平均卖出价 |
| today_short_shares | 今日卖出股数 |
| today_short_turnover | 今日卖出成交额 |
| today_turnover | 今日成交额 |
| value | 当前市值 |
| value_price | 用于计算市值的价格 |

例如：

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
    }


##### <a name='Order'></a>订单 Order

说明：表示一个订单

字段：

| 名称 | 意义 |
| ---- | ---- |
| avg_price | 平均成交价 |
| code | 股票代码 |
| name | 股票名称。使用了请求中指定的语言 |
| create_time | 创建时间（时间戳） |
| update_time | 最近一次修改时间（时间戳） |
| enable | 生效自段（暂不用管） |
| last_err | 订单最近一次发生的错误码。0为没有错误。 具体的错误文本可以使用下面的last_err_text展示给客户 |
| matched_quantity | 已成交股数 |
| order_id | 订单号，可以唯一标记该用户的一个订单 |
| price | 订单价格 |
| quantity | 订单数量 |
| side | 方向。字符串。BUY：买入， SELL：卖出。可以使用下面的side_text字段展示给客户。 |
| state | 状态。整数。可能的取值有：<br />0正在提交，1正常，2已撤单，3已删除，4下单失败，5 等待开盘。<br />可以使用下面的state_text字段展示给客户。 |
| type | 订单类型。字符串，必须是一个字符。 可能的取值如下：<br /> E:增强限价单(Enhanced Limit)，A:竞价单(Auction)，I:竞价限价单(Auction Limit)，L:限价单(Limit)，S:特别限价单(Special Limit)。LIMIT:限价单，MARKET:市价单<br />对港股只有E\A\I三种订单允许客户输入，美股只有LIMIT和MARKET<br />可以使用下面的type_text字段展示给客户。|
| last_err_text | 对应上面last_err字段的展示文本，文本使用的语言由请求参数决定 |
| side_text | 对应上面side字段的展示文本，文本使用的语言由请求参数决定 |
| type_text | 对应上面type字段的展示文本，文本使用的语言由请求参数决定 |
| state_text | 对应上面state字段的展示文本，文本使用的语言由请求参数决定 |

例如：

    {
        "avg_price": "0",
        "code": 90003,
        "name": "Futu&stock 3",
        "create_time": 1446618508,
        "enable": 1,
        "last_err": 0,
        "matched_quantity": 0,
        "update_time": 1446618536,
        "order_id": "13253",
        "price": "10.5",
        "quantity": 1000,
        "side": "SELL",
        "state": 1,
        "type": "E",
        "last_err_text": "",
        "side_text": "卖",
        "type_text": "普通",
        "state_text": "等待成交"
    }

##### <a name='Trade'></a>成交 Trade

说明：表示一个成交。一个订单可能会对应多笔成交。

字段：

| 名称 | 意义 |
| ---- | ---- |
| code | 股票代码 |
| name | 股票名称。使用了请求中指定的语言 |
| counter_broker_id | 成交对手经纪号 |
| create_time | 创建时间（时间戳） |
| order_created | 所属订单的创建时间（时间戳） |
| order_id | 所属订单ID。有可能为0，表示该成交不属于任何一个订单。 |
| order_modified | 所属订单的修改时间（时间戳） |
| price | 成交价格 |
| quantity | 成交数量 |
| side | 方向。字符串。BUY：买入， SELL：卖出。可以使用下面的side_text字段展示给客户。 |
| id | 成交ID，唯一标志了一笔成交 |
| side_text | 对应上面side字段的展示文本，文本使用的语言由请求参数决定 |

例如：

    {
        "code": 90008,
        "name": "Futu&stock 8",
        "counter_broker_id": 5001,
        "create_time": 1446620585,
        "order_created": 1446620585,
        "order_id": "345673654",
        "order_modified": 1446620585,
        "price": "30.5",
        "quantity": 200,
        "side": "SELL",
        "id": 16,
        "side_text": "卖"
    }
