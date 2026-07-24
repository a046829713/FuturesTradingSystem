# 系統建置規格書 (`spec/build.md`)

## 1. 系統概述與目標 (System Overview & Goals)
本專案旨在建構一個以 Python 開源量化交易框架 **VeighNa (`vnpy`)** 為核心的**台灣期貨（台指期 TX / 小台 MTX / 微台 TMF）程式交易與回測平台**。

### 主要功能目標：
1. **數據管理**：支援臺灣期貨交易所 (TAIFEX) 歷史數據解析、轉換與 SQLite 資料庫存儲。
2. **策略開發**：提供台指期專用的 CTA 策略範例（含均線趨勢、通道突破與當沖收盤平倉邏輯）。
3. **歷史回測**：支援腳本化批量歷史回測與參數最佳化（網格搜尋與遺傳演算法）。
4. **桌面 UI**：整合 `vnpy_qt` 提供完整的 GUI 監控、策略調參、視覺化回測與數據管理介面。

---

## 2. 系統架構與專案目錄結構 (Architecture & Directory Structure)

```
FuturesTradingSystem/
├── config/                         # 系統與策略配置檔案目錄
│   ├── vt_setting.json             # vnpy 核心系統設置（資料庫、日誌等級）
│   └── cta_strategy_setting.json   # CTA 策略與合約代碼配置檔
├── core/                           # 核心擴充與資料處理模組
│   ├── __init__.py
│   └── data_importer.py            # TAIFEX CSV 數據解析與 vnpy 資料庫寫入器
├── strategies/                     # CTA 交易策略目錄
│   ├── __init__.py
│   ├── tw_ma_strategy.py          # 策略 1：台指期雙均線趨勢策略
│   └── tw_breakout_strategy.py    # 策略 2：台指期唐奇安通道突破當沖策略
├── spec/                           # 專案規格文件目錄
│   └── build.md                    # 本建置規格文件
├── run_gui.py                      # 啟動主程式：Qt 桌面圖形介面平台 (vnpy GUI)
├── run_backtest.py                 # 腳本式歷史回測與參數最佳化入口
├── requirements.txt                # 專案套件依賴說明
└── README.md                       # 專案說明文件
```

---

## 3. 模組詳細規格 (Detailed Module Specifications)

### 3.1 歷史數據模組 (`core/data_importer.py`)
- **功能描述**：解析外部（如 TAIFEX 期交所官網）的歷史 K 線 CSV 或標準 Pandas DataFrame，轉換為 `vnpy.trader.object.BarData` 格式。
- **欄位規格**：
  - `symbol` (代碼，如 `TX00` / `MTX00`)
  - `exchange` (交易所，固定為 `Exchange.TAIFEX` 或 `Exchange.LOCAL`)
  - `datetime` (時間戳，支援 `YYYY-MM-DD HH:MM:SS`)
  - `interval` (週期，如 `Interval.MINUTE` 或 `Interval.DAILY`)
  - `open_price`, `high_price`, `low_price`, `close_price`, `volume`, `open_interest`
- **資料庫接入**：調用 `get_database()` 寫入 SQLite (`database.db`)，供 DataManager / CtaBacktester 讀取。

### 3.2 台指期專用 CTA 策略開發 (`strategies/`)
#### 策略一：`TWFuturesMAStrategy`（雙均線趨勢策略）
- **指標**：快均線 (`fast_window`)、慢均線 (`slow_window`)。
- **開平倉邏輯**：
  - 快均線上穿慢均線：平空做多。
  - 快均線下穿慢均線：平多做空。
- **風控機制**：固定點數停損停利 (`sl_points`, `tp_points`)，以及當沖平倉時間 (`exit_time`，預設 13:45 自動平倉)。

#### 策略二：`TWFuturesBreakoutStrategy`（唐奇安通道突破策略）
- **指標**：近 N 週期最高價與最低價通道 (`donchian_window`)、ATR 指流與波動度過濾。
- **開平倉邏輯**：突破通道上軌開多，跌破通道下軌開空。

### 3.3 歷史回測與參數最佳化 (`run_backtest.py`)
- **回測引擎配置**：
  - 合約代碼：`TX00.TAIFEX` / `MTX00.TAIFEX`
  - K線週期：1 分鐘 (`Interval.MINUTE`)
  - 交易成本：滑點 1 點 (Slippage)，手續費（每口定額或比例）
  - 資本金：NT$ 1,000,000
- **最佳化功能**：
  - 網格搜尋 (Grid Search) 最佳化策略參數。
  - 輸出績效統計（總收益率、年化收益率、夏普比率、最大回撤 MDD、勝率、盈虧比）。

### 3.4 Qt 桌面 UI 應用程式 (`run_gui.py`)
- **載入 App 模組**：
  - `CtaStrategyApp`：策略啟動、停止、參數修訂與監控。
  - `CtaBacktesterApp`：圖形化 K 線視覺化回測。
  - `DataManagerApp`：數據庫管理與查詢。
- **啟動流程**：初始化 `EventEngine` 與 `MainEngine` -> 載入 Apps -> 啟動 `PySide6` QApplication 主視窗。

---

## 4. 技術棧與依賴套件 (Technology Stack)

| 類別 | 套件 / 工具 | 說明 |
| :--- | :--- | :--- |
| **程式語言** | Python 3.10+ | 主要開發語言 |
| **量化框架** | `vnpy` / `vnpy_evtengine` | 事件驅動核心與主引擎 |
| **策略/回測** | `vnpy_ctastrategy`, `vnpy_ctabacktester` | CTA 策略模組與回測引擎 |
| **數據管理** | `vnpy_datamanager`, `vnpy_sqlite` | 數據管理 UI 與 SQLite 儲存 |
| **GUI 介面** | `PySide6` | Qt 圖形化視窗介面 |
| **資料處理** | `pandas`, `numpy` | 數據轉換與計算 |

---

## 5. 實作步驟與階段任務 (Implementation Plan)

1. **Step 1: 專案目錄與配置檔建置**
   - 建立專案目錄結構、`spec/build.md`、`requirements.txt` 與 `config/vt_setting.json`。
2. **Step 2: 數據導入模組 (`core/data_importer.py`)**
   - 實作台指期數據解析器，包含生成範例測試數據並寫入 SQLite 資料庫的功能。
3. **Step 3: 策略模組實作 (`strategies/`)**
   - 撰寫 `tw_ma_strategy.py` 與 `tw_breakout_strategy.py`，加入停損停利與 13:45 當沖結算邏輯。
4. **Step 4: 歷史回測腳本 (`run_backtest.py`)**
   - 實作回測執行流程與參數最佳化輸出。
5. **Step 5: Qt GUI 主程式 (`run_gui.py`)**
   - 整合 `vnpy` 各 App 模組，完成桌面應用程式啟動檔。
6. **Step 6: 系統測試與驗證**
   - 執行數據導入、策略回測與 GUI 介面啟動驗證。
