# -*- coding: utf-8 -*-

# Account 常量
# 账户类型 Account.type
ACCOUNTTYPE_SIM = 0  # 模拟账户
ACCOUNTTYPE_STOCK = 1  # 股票账户
ACCOUNTTYPE_FUTURE = 2  # 期货账户
ACCOUNTTYPE_OPTION = 3  # 期权账户
ACCOUNTTYPE_DIGITAL = 4  # 数字货币

# Case常量
# 资金变动原因
# Cash.change_reason
CASHCHANGEREASON_UNKNOWN = 0  # 不明
CASHCHANGEREASON_TRADE = 1  # 交易
CASHCHANGEREASON_INOUT = 2  # 出入金

# Position常量
# Position.side 持仓类型
POSITIONSIDE_UNKNOWN = 0  # 不明
POSITIONSIDE_LONG = 1  # 多头
POSITIONSIDE_SHORT = 2  # 空头

# 仓位变动原因
# Position.change_reason
POSITIONCHANGEREASON_UNKNOW = 0  # 不明
POSITIONCHANGEREASON_TRADE = 1  # 交易
POSITIONCHANGEREASON_LIQUIDATION = 2  # 强平
POSITIONCHANGEREASON_INOUT = 3  # 出入仓

# Order常量
# Order.side 委托方向
ORDERSIDE_UNKNOWN = 0  # 不明
ORDERSIDE_BUY = 1  # 买入
ORDERSIDE_SELL = 2  # 卖出

# Order.position_effect　开平标志
ORDERPOSITIONEFFECT_UNKNOWN = 0  # 不明
ORDERPOSITIONEFFECT_OPEN = 1  # 开仓
ORDERPOSITIONEFFECT_CLOSE = 2  # 平仓
ORDERPOSITIONEFFECT_CLOSETODAY = 3  # 今平仓

# Order.type 委托类型
ORDERTYPE_UNKNOWN = 0  # 不明
ORDERTYPE_LIMIT = 1  # 限价
ORDERTYPE_MARKET = 2  # 市价
ORDERTYPE_FAK = 3  # 即时成交剩余撤销
ORDERTYPE_FOK = 4  # 即时全额成交或撤销
ORDERTYPE_BOC = 5  # 对方最优价格
ORDERTYPE_BOP = 6  # 己方最优价格
ORDERTYPE_B5TC = 7  # 最优五档剩余撤销
ORDERTYPE_B5TL = 8  # 最优五档剩余转限价

# Order.source 委托来源
ORDERSOURCE_MANUAL = 0  # 手动下单
ORDERSOURCE_STRATEGY = 1  # 策略下单
ORDERSOURCE_STOP = 2  # 止盈止损单

#  Order.status 委托状态
ORDERSTATUS_UNKNOWN = 0  # 不明
ORDERSTATUS_CREATED = 1  # 创建
ORDERSTATUS_REPORTED = 2  # 已报
ORDERSTATUS_CANCELED = 3  # 已撤销订单
ORDERSTATUS_DEALED = 4  # 全部成交
ORDERSTATUS_REJECTED = 5  # 已拒绝
ORDERSTATUS_PENDINGCANCEL = 6  # 待撤销订单
ORDERSTATUS_PARTIALDEALED = 7  # 部分成交
ORDERSTATUS_PENDINGNEW = 8  # 待报
ORDERSTATUS_EXPIRED = 9  # 已过期
ORDERSTATUS_SUSPENDED = 10  # 挂起
# Order.rej_reason
# 拒绝原因
ORDERREJECTREASON_UNKNOWN = 0  # 未知原因
ORDERREJECTREASON_RISKRULECHECKFAILED = 1  # 不符合风控规则
ORDERREJECTREASON_NOENOUGHCASH = 2  # 资金不足
ORDERREJECTREASON_NOENOUGHPOSITION = 3  # 仓位不足
ORDERREJECTREASON_ILLEGALACCOUNTID = 4  # 非法账户ID
ORDERREJECTREASON_ILLEGALSTRATEGYID = 5  # 非法策略ID
ORDERREJECTREASON_ILLEGALSYMBOL = 6  # 非法交易标的
ORDERREJECTREASON_ILLEGALVOLUME = 7  # 非法委托量
ORDERREJECTREASON_ILLEGALPRICE = 8  # 非法委托价
ORDERREJECTREASON_ACCOUNTDISABLED = 9  # 账户被禁止交易
ORDERREJECTREASON_ACCOUNTDISCONNECTED = 10  # 账户未连接
ORDERREJECTREASON_ACCOUNTLOGGEDOUT = 11  # 账户未登录
ORDERREJECTREASON_NOTINTRADINGSESSION = 12  # 非交易时间段
ORDERREJECTREASON_ORDERTYPENOTSUPPORTED = 13  # 委托类型不支持
ORDERREJECTREASON_THROTTLE = 14  # 流控限制

# Execution 常量
# Execution.position_effect 开平标记
EXECUTIONPOSITIONEFFECT_UNKNOWN = 0  # 不明
EXECUTIONPOSITIONEFFECT_OPEN = 1  # 开仓
EXECUTIONPOSITIONEFFECT_CLOSE = 2  # 平仓
EXECUTIONPOSITIONEFFECT_CLOSETODAY = 3  # 今平仓

# Execution.side 买卖方向
EXECUTIONSIDE_UNKNOWN = 0  # 不明
EXECUTIONSIDE_BUY = 1  # 买入
EXECUTIONSIDE_SELL = 2  # 卖出

# OrderStop 常量
# OrderStop.stop_type 止损类型
ORDERSTOP_STOP_TYPE_UNKNOWN = 0  # 不明
ORDERSTOP_STOP_TYPE_POINT = 1  # point
ORDERSTOP_STOP_TYPE_PERCENT = 2  # percent

# OrderStop.trailing_type
ORDERSTOP_TRAILING_UNKNOW = 0
ORDERSTOP_TRAILING_POINT = 1
ORDERSTOP_TRAILING_PERCENT = 2

# OrderStop.side 买卖方向
ORDERSTOP_SIDE_UNKNOWN = 0  # 不明
ORDERSTOP_SIDE_BUY = 1  # 买入
ORDERSTOP_SIDE_SELL = 2  # 卖出

# OrderStop.stop_order_type 止损/止盈 跟踪止盈类型
ORDERSTOP_STOP_TYPE_UNKNOW = 0
ORDERSTOP_STOP_TYPE_LOSS = 1  # 止损单类型
ORDERSTOP_STOP_TYPE_PROFIT = 2  # 止盈单类型
ORDERSTOP_STOP_TYPE_TRAILING = 3  # 跟踪止盈单类型

# OrderStop.order_type 委托类型
ORDERSTOP_ORDER_TYPE_UNKNOWN = 0  # 不明
ORDERSTOP_ORDER_TYPE_LIMIT = 1  # 限价
ORDERSTOP_ORDER_TYPE_MARKET = 2  # 市价

# OrderStop.execute_type 执行汇报类型
ORDERSTOPEXECTYPE_HOLDING = 1  # 保持
ORDERSTOPEXECTYPE_CANCELED = 2  # 已撤销
ORDERSTOPEXECTYPE_PENDINGCANCEL = 3  # 待撤销
ORDERSTOPEXECTYPE_ACTIVE = 4  # 激活
ORDERSTOPEXECTYPE_TRAILING = 5  # 追踪中
ORDERSTOPEXECTYPE_TRIGGER = 6  # 已触发

# 其他常量
# 复权类型
FQ_NA = 0  # 不复权
FQ_FORWARD = 1  # 前复权
FQ_BACKWARD = 2  # 后复权

# 市价单成交方式
# 直接成交
MARKETORDER_DIRECT = 0
# 对方最优价
MARKETORDER_NONME_BEST_PRICE = 1
# 己方最优价
MARKETORDER_ME_BEST_PRICE = 2

# 限价单成交方式
# 直接成交
LIMITORDER_DIRECT = 0
# 下一个 bar 内没有价格时，撤单处理
LIMITORDER_NOPRICE_CANCEL = 1
