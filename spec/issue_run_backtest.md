# 🎟️ Issue 規格書：`run_backtest.py` 重構與規範化 (`spec/issue_run_backtest.md`)

## 1. Issue 概述與背景 (Overview & Background)

本 Issue 旨在對現有的 `run_backtest.py` 進行重構與規範化清理，使其完全符合專案架構規範（VeighNa 生態系標準）與 Python 社群規範 (PEP 8)。

---

## 2. 重構要點與變更目標 (Key Refactoring Requirements)

### 2.1 移除獨立自建回測引擎 (`run_standalone_backtest`)
- **現狀**：`run_backtest.py` 包含 `run_standalone_backtest()` 函式作為未安裝 `vnpy` 時的備用 fallback 機制。
- **問題**：此自訂引擎違反專案統一使用 VeighNa (`vnpy`) 生態系的核心風格，雙套回測邏輯增加維護成本並可能導致統計數據不一致。
- **調整**：完全刪除 `run_standalone_backtest()` 函式及其相關 fallback 分支，強制統一透過 `vnpy_ctastrategy.backtesting.BacktestingEngine` 執行歷史回測。

### 2.2 參數模組化與配置檔註解支援 (`config/cta_strategy_setting.json`)
- **現狀**：`run_backtest.py` 中硬編碼 (Hardcode) 了許多回測引擎參數（如 `vt_symbol`, `rate`, `slippage`, `size`, `pricetick`, `capital`）與策略參數（如 `fast_window`, `slow_window`, `sl_points`, `tp_points`）。
- **調整**：
  1. 擴充與規範 `config/cta_strategy_setting.json` 設定檔，整合回測引擎參數 (engine parameters) 與策略參數 (strategy parameters)。
  2. **註解功能支援 (CRITICAL)**：在 `config/cta_strategy_setting.json` 配置檔中支援參數功能註解（例如：滑點 `slippage`、手續費率 `rate`、合約乘數 `size`、初始資金 `capital` 等說明）。已於 `run_backtest.py` 讀取 JSON 時實現安全過濾 `//` / `#` 註解行。
  3. `run_backtest.py` 啟動時動態讀取並解析 `config/cta_strategy_setting.json`，將參數正確傳入 `BacktestingEngine` 及 `add_strategy()` 中。

### 2.3 Import 集中與 PEP 8 規範化 (Import Restructuring)
- **現狀**：`run_backtest.py` 將部分 import（例如 `from simulation.generate_csv ...`、`from vnpy_ctastrategy.backtesting ...`、`import matplotlib.pyplot ...`）散落在函式內部或條件判斷式中。
- **調整**：遵循 Python 社群最佳實踐 (PEP 8)，將所有模組與套件的 `import` 宣告統一移至 `run_backtest.py` 檔案開頭位置。

---

## 3. 實作任務拆解 (Task Breakdown)

- [x] **Task 1**: 撰寫與同步 `spec/issue_run_backtest.md` 規格內容（包含設定檔註解需求）。
- [x] **Task 2**: 更新 `config/cta_strategy_setting.json` 設定檔，導入回測引擎與策略所需之完整配置參數並加上欄位說明註解。
- [x] **Task 3**: 重構 `run_backtest.py` 腳本：
  - 將所有 `import` 集中移至檔案頭部。
  - 移除 `run_standalone_backtest` 及其 fallback 調用邏輯。
  - 實作安全過濾與解析含註解之 JSON 設定檔 (`config/cta_strategy_setting.json`) 讀取邏輯。
- [x] **Task 4**: 使用專案虛擬環境執行 `..\Scripts\python.exe run_backtest.py` 驗證回測流程與 `backtest_result.png` 圖表產出。
