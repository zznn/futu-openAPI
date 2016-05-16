# 富途开放-交易接口

for 第三方开发者

author: july

<!-- MarkdownTOC -->
- [Token API 令牌接口](#token)
    - [save_token 保存令牌](#save_token)
    - [delete_token 删除令牌](#delete_token)
    - [trade_token 交易令牌](#trade_token)
- [Accounts API 账户接口](#accounts-api)
    - [get_account_detail 获取账户详情](#get_account_detail)
    - [get_account_cash 获取账户现金数据](#get_account_cash)
    - [get_account_portfolio 获取账户持仓](#get_account_portfolio)
    - [get_list_orders 获取订单列表](#get_list_orders)
    - [get_list_trades 获取成交列表](#get_list_trades)
- [Order API 交易接口](#order-api)
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
**备注：若未获得tradetoken而直接调用以下3种接口，将返回如下信息**
```python
{
    "ClientWarning":"didn't get tradetoken" 
}
```
