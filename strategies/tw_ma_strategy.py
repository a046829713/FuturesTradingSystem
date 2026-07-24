from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    ArrayManager,
)
from vnpy.trader.constant import Interval, Direction, Offset, Exchange


class TWFuturesMAStrategy(CtaTemplate):
    """
    台指期雙均線當沖與風控趨勢策略
    """
    author = "FuturesTradingSystem"

    # 策略參數
    fast_window = 10
    slow_window = 30
    sl_points = 30.0   # 停損點數
    tp_points = 60.0   # 停利點數

    # 策略變數
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    entry_price = 0.0

    parameters = [
        "fast_window",
        "slow_window",
        "sl_points",
        "tp_points"
    ]
    variables = [
        "fast_ma0",
        "fast_ma1",
        "slow_ma0",
        "slow_ma1",
        "entry_price"
    ]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.am = ArrayManager(size=100)

    def on_init(self):
        """策略初始化"""
        self.write_log("策略初始化完成")
        self.load_bar(10)

    def on_start(self):
        """策略啟動"""
        self.write_log("策略啟動成功")

    def on_stop(self):
        """策略停止"""
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """Tick 推送"""
        pass

    def on_bar(self, bar: BarData):
        """K 線推送與交易邏輯"""
        self.cancel_all()

        self.am.update_bar(bar)
        if not self.am.inited:
            return

        # 計算雙均線
        fast_ma = self.am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]

        slow_ma = self.am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        # 均線交叉訊號
        cross_over = (self.fast_ma1 <= self.slow_ma1) and (self.fast_ma0 > self.slow_ma0)
        cross_under = (self.fast_ma1 >= self.slow_ma1) and (self.fast_ma0 < self.slow_ma0)

        # 檢查台指期日盤收盤前平倉 (13:40 - 13:45)
        current_time = bar.datetime.time()
        if current_time.hour == 13 and current_time.minute >= 40:
            if self.pos > 0:
                self.sell(bar.close_price - 2, abs(self.pos))
            elif self.pos < 0:
                self.cover(bar.close_price + 2, abs(self.pos))
            return

        # 開平倉邏輯
        if self.pos == 0:
            if cross_over:
                self.buy(bar.close_price + 2, 1)
                self.entry_price = bar.close_price
            elif cross_under:
                self.short(bar.close_price - 2, 1)
                self.entry_price = bar.close_price
        elif self.pos > 0:
            if cross_under:
                self.sell(bar.close_price - 2, abs(self.pos))
                self.short(bar.close_price - 2, 1)
                self.entry_price = bar.close_price
            else:
                # 多單停損停利風控
                if bar.low_price <= self.entry_price - self.sl_points or bar.high_price >= self.entry_price + self.tp_points:
                    self.sell(bar.close_price - 2, abs(self.pos))
        elif self.pos < 0:
            if cross_over:
                self.cover(bar.close_price + 2, abs(self.pos))
                self.buy(bar.close_price + 2, 1)
                self.entry_price = bar.close_price
            else:
                # 空單停損停利風控
                if bar.high_price >= self.entry_price + self.sl_points or bar.low_price <= self.entry_price - self.tp_points:
                    self.cover(bar.close_price + 2, abs(self.pos))

        self.put_event()
