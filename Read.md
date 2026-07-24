# 📈 台指期量化交易與回測平台 (Futures Trading System)

本專案是一個基於 Python 開源量化交易框架 **VeighNa (`vnpy`)** 構建的**台灣期貨（台指期 TX / 小台 MTX / 微台 TMF）程式交易與回測系統**。提供從歷史數據管理、策略開發、參數最佳化回測到 Qt 桌面 GUI 監控的完整量化交易解決方案。

---

## 🌟 系統核心功能與特色

1. **📊 歷史數據管理**：支援臺灣期貨交易所 (TAIFEX) 歷史數據解析、轉換與 SQLite 資料庫寫入。
2. **💡 專業 CTA 策略**：內建台指期專用策略，包含雙均線趨勢策略與唐奇安通道突破策略，並具備當沖強制平倉與風控停損機制。
3. **⚡ 批量回測與參數最佳化**：提供腳本化歷史回測，支援網格搜尋 (Grid Search) 與遺傳演算法 (Genetic Algorithm) 進行參數尋優。
4. **🖥️ 現代化 Qt 桌面 UI**：整合 `vnpy_qt` 提供強大的 GUI 圖形化介面，方便實時監控、策略調參、K線繪圖與數據庫管理。

---

## 🏗️ 系統架構與專案結構

```text
FuturesTradingSystem/
├── config/                         # 系統與策略配置目錄
│   ├── vt_setting.json             # vnpy 核心系統設置（資料庫設定、日誌等級）
│   └── cta_strategy_setting.json   # CTA 策略與合約代碼配置檔
├── core/                           # 核心擴充與資料處理模組
│   ├── __init__.py
│   └── data_importer.py            # TAIFEX CSV 數據解析與 vnpy SQLite 寫入器
├── strategies/                     # CTA 交易策略目錄
│   ├── __init__.py
│   ├── tw_ma_strategy.py          # 策略 1：台指期雙均線趨勢策略
│   └── tw_breakout_strategy.py    # 策略 2：台指期唐奇安通道突破當沖策略
├── spec/                           # 專案規格文件目錄
│   └── build.md                    # 系統建置規格書
├── run_gui.py                      # 啟動主程式：Qt 桌面圖形介面平台 (vnpy GUI)
├── run_backtest.py                 # 腳本式歷史回測與參數最佳化入口
├── requirements.txt                # 專案套件依賴說明
└── README.md                       # 專案說明文件
```

---

## 🛠️ 技術棧 (Technology Stack)

| 類別 | 套件 / 工具 | 說明 |
| :--- | :--- | :--- |
| **開發語言** | Python 3.10+ | 主要程式語言 |
| **核心框架** | `vnpy` / `vnpy_evtengine` | 事件驅動量化交易核心 |
| **策略與回測** | `vnpy_ctastrategy`, `vnpy_ctabacktester` | CTA 策略架構與回測引擎 |
| **數據管理** | `vnpy_datamanager`, `vnpy_sqlite` | 數據管理 UI 與 SQLite 資料庫 |
| **圖形介面** | `PySide6` | Qt 視窗介面架構 |
| **數據處理** | `pandas`, `numpy` | 數據清洗、轉置與數值計算 |

---

## 🚀 快速開始 (Quick Start)

### 1. 環境準備與安裝依賴

建議使用 Python 3.10+ 虛擬環境，並安裝相關依賴套件：

```bash
pip install -r requirements.txt
```

### 2. 歷史數據導入

將 TAIFEX 歷史 K 線數據轉入 SQLite 資料庫：

```bash
python -m core.data_importer
```

### 3. 執行策略歷史回測與最佳化

執行腳本進行台指期策略回測與參數網格搜尋：

```bash
python run_backtest.py
```

### 4. 啟動 Qt 桌面圖形介面 (GUI)

啟動整合 `CtaStrategy`、`CtaBacktester` 與 `DataManager` 的視窗應用程式：

```bash
python run_gui.py
```

---

## 📈 內建策略說明

### 1. 雙均線趨勢策略 (`TWFuturesMAStrategy`)
- **核心指標**：快均線 (`fast_window`)、慢均線 (`slow_window`)。
- **交易邏輯**：快均線上穿慢均線平空做多；快均線下穿慢均線平多做空。
- **風控特點**：內建固定點數停損停利 (`sl_points`, `tp_points`)，並於預設 13:45 進行當沖自動平倉。

### 2. 唐奇安通道突破策略 (`TWFuturesBreakoutStrategy`)
- **核心指標**：唐奇安通道 (`donchian_window`)、ATR 波動度過濾。
- **交易邏輯**：突破近 N 週期最高價開多，跌破近 N 週期最低價開空。

---

## 📄 詳細規格文件

詳細模組規範與建置細節請參閱：[spec/build.md](spec/build.md)。
