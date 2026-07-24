import csv
from datetime import datetime
import json
import os
import re
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from simulation.generate_csv import generate_simulation_data
from strategies.tw_ma_strategy import TWFuturesMAStrategy
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData
from vnpy_ctastrategy.backtesting import BacktestingEngine

# Windows 終端機 UTF-8 相容處置
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_json_config(filepath: str) -> dict:
    """
    載入並解析包含單行或行尾註解 (// 或 #) 之 JSON 設定檔
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到設定檔：{filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # 去除全行或行尾註解
        line_clean = re.sub(r'^\s*//.*$', '', line)
        line_clean = re.sub(r'^\s*#.*$', '', line_clean)
        line_clean = re.sub(r'\s*//(?=(?:[^"]*"[^"]*")*[^"]*$).*$', '', line_clean)
        line_clean = re.sub(r'\s*#(?=(?:[^"]*"[^"]*")*[^"]*$).*$', '', line_clean)
        cleaned_lines.append(line_clean)

    cleaned_content = "\n".join(cleaned_lines)
    return json.loads(cleaned_content)


def read_csv_bars(file_path: str) -> list:
    """讀取歷史 K 線數據 CSV 檔案"""
    bars = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
            bars.append({
                "datetime": dt,
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row["volume"]),
                "open_interest": float(row["open_interest"])
            })
    return bars


def run_vnpy_backtest(csv_bars: list, config_path: str = os.path.join("config", "cta_strategy_setting.json")):
    """使用 VeighNa (vnpy_ctastrategy) 歷史回測引擎執行回測"""
    configs = load_json_config(config_path)
    strategy_config = configs.get("TWFuturesMAStrategy_TX00", {})

    backtest_setting = strategy_config.get("backtest_setting", {})
    setting = strategy_config.get("setting", {})

    # 解析 K 線週期
    interval_str = backtest_setting.get("interval", "1m")
    interval = Interval.MINUTE if interval_str == "1m" else Interval.DAILY

    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol=strategy_config.get("vt_symbol", "TX00.LOCAL"),
        interval=interval,
        start=csv_bars[0]["datetime"],
        end=csv_bars[-1]["datetime"],
        rate=float(backtest_setting.get("rate", 0.00002)),
        slippage=float(backtest_setting.get("slippage", 1.0)),
        size=float(backtest_setting.get("size", 200)),
        pricetick=float(backtest_setting.get("pricetick", 1.0)),
        capital=float(backtest_setting.get("capital", 1_000_000)),
    )

    engine.add_strategy(TWFuturesMAStrategy, setting)

    # 轉換數據為 vnpy BarData 並寫入引擎歷史紀錄
    vnpy_bars = []
    for b in csv_bars:
        bar = BarData(
            symbol="TX00",
            exchange=Exchange.LOCAL,
            datetime=b["datetime"],
            interval=Interval.MINUTE,
            open_price=b["open"],
            high_price=b["high"],
            low_price=b["low"],
            close_price=b["close"],
            volume=b["volume"],
            open_interest=b["open_interest"],
            gateway_name="SIM"
        )
        vnpy_bars.append(bar)

    engine.history_data = vnpy_bars
    engine.run_backtesting()
    df = engine.calculate_result()
    stats = engine.calculate_statistics()

    # 提取圖表數據
    if df is not None and not df.empty:
        dates = list(df.index)
        equity = list(df["balance"]) if "balance" in df.columns else [backtest_setting.get("capital", 1000000)] * len(dates)
        drawdown = list(df["drawdown"]) if "drawdown" in df.columns else [0] * len(dates)
    else:
        dates = [b["datetime"] for b in csv_bars]
        equity = [backtest_setting.get("capital", 1000000)] * len(dates)
        drawdown = [0] * len(dates)

    report_data = {
        "dates": dates,
        "equity": equity,
        "drawdown": drawdown
    }

    return stats, report_data


def generate_png_report(dates: list, equity: list, drawdown: list, output_path: str = "backtest_result.png"):
    """使用 matplotlib 生成視覺化 PNG 報告"""
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

        # 圖表 1: 權益曲線 (Equity Curve)
        ax1.plot(dates, equity, color="#1f77b4", linewidth=1.8, label="Net Equity (NT$)")
        ax1.set_title("Futures Trading System - Backtest Performance Report", fontsize=14, fontweight="bold", pad=12)
        ax1.set_ylabel("Account Balance (NT$)", fontsize=11)
        ax1.legend(loc="upper left")
        ax1.grid(True, linestyle="--", alpha=0.6)

        # 圖表 2: 回撤百分比曲線 (Drawdown Curve)
        ax2.fill_between(dates, drawdown, 0, color="#d62728", alpha=0.35, label="Drawdown (%)")
        ax2.plot(dates, drawdown, color="#d62728", linewidth=1.2)
        ax2.set_ylabel("Drawdown (%)", fontsize=11)
        ax2.set_xlabel("Date", fontsize=11)
        ax2.legend(loc="lower left")
        ax2.grid(True, linestyle="--", alpha=0.6)

        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        fig.autofmt_xdate()
        plt.tight_layout()

        plt.savefig(output_path, dpi=200)
        plt.close()
        print(f"\n[Visual Report] Successfully exported chart report to: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"\n[Visual Report Warning] Visual chart export skipped ({e})")


def print_stats_report(stats: dict):
    """列印控制台格式化報告"""
    if not stats:
        print("無可用統計數據。")
        return
    print("\n" + "=" * 55)
    print("        TAIFEX Strategy Backtest Performance Report")
    print("=" * 55)
    print(f"Start Time     : {stats.get('start_date', stats.get('start_time', 'N/A'))}")
    print(f"End Time       : {stats.get('end_date', stats.get('end_time', 'N/A'))}")
    print(f"Initial Capital: NT$ {stats.get('capital', 0.0):,.2f}")
    print(f"Final Balance  : NT$ {stats.get('end_balance', stats.get('final_balance', 0.0)):,.2f}")
    print(f"Net PnL        : NT$ {stats.get('total_net_pnl', stats.get('net_pnl', stats.get('total_pnl', 0.0))):,.2f}")
    print(f"Total Return   : {stats.get('total_return', 0.0):.2f} %")
    print(f"Total Trades   : {stats.get('total_trade_count', stats.get('total_trades', 0))}")
    print(f"Win Rate       : {stats.get('winning_rate', stats.get('win_rate', 0.0)):.2f} %")
    print(f"Profit/Loss    : {stats.get('profit_loss_ratio', 0.0):.2f}")
    print(f"Max Drawdown   : {stats.get('max_ddpercent', stats.get('max_drawdown', 0.0)):.2f} %")
    print(f"Total Fee      : NT$ {stats.get('total_commission', stats.get('total_fee', 0.0)):,.2f}")
    print(f"Total Slippage : NT$ {stats.get('total_slippage', 0.0):,.2f}")
    print("=" * 55)


def main():
    csv_file = os.path.join("simulation", "FITX.csv")
    if not os.path.exists(csv_file):
        print("未檢測到 simulation/FITX.csv，正自動生成模擬數據...")
        generate_simulation_data()

    print(f"Loading TAIFEX simulation data from {csv_file}...")
    csv_bars = read_csv_bars(csv_file)
    print(f"Loaded {len(csv_bars)} bars successfully.")

    stats, report_data = run_vnpy_backtest(csv_bars)
    print("\nSuccessfully executed via VeighNa (vnpy) backtesting engine.")

    print_stats_report(stats)
    generate_png_report(report_data["dates"], report_data["equity"], report_data["drawdown"])


if __name__ == "__main__":
    main()
