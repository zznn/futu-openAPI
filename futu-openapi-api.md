# 富途开放-交易接口

for 第三方开发者

author: july

<!-- MarkdownTOC -->
- [Token API 令牌接口](#token)
    - [save_token 保存令牌](#save_token)
    - [delete_token 删除令牌](#delete_token)
    - [trade_token 交易令牌](#trade_token)
- [Accounts API 账户接口](#accounts-api)
    - [get_account_detail 获取账户详情](#get-account-detail)
    - [get_account_cash 获取账户现金数据](#get-account-cash)
    - [get_account_portfolio 获取账户持仓](#get-account-portfolio)
    - [get_list_orders 获取订单列表](#get_list_orders)
    - [get_list_trades 获取成交列表](#get_list_trades)
- [Order API 订单接口](#order-api)
    - [place_order 下单](#place-order-下单)
    - [change_order 修改订单](#change-order-修改订单)
    - [cancle_order 撤单](#cancel-order-撤单)

- [附录](#附录)
    - [接口中涉及的数据结构](#接口中涉及的数据结构)
    - [签名生成](#签名生成)

<!-- /MarkdownTOC -->
