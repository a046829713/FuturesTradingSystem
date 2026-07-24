# 🎟️ Ticket 規格書：`run_backtest.py` 歷史回測與 PNG 報告產出模組 (`spec/build_run_backtest.md`)

## 1. Ticket 概述與目標 (Ticket Overview & Goals)

本 Ticket 旨在基於 **VeighNa (`vnpy`) 生態系**（`vnpy_ctastrategy.backtesting` 模組）建置可執行的歷史回測腳本 **`run_backtest.py`**。

### 核心目標與決策：
1. **數據來源 (Data Source)**：直接讀取 `simulation/FITX.csv` 歷史模擬數據檔案，轉換為 `vnpy.trader.object.BarData` 格式並寫入/注入回測引擎。
2. **優先導出 PNG 圖表報告**：回測完成後，利用 `matplotlib` 生成多合一視覺化圖表報告（`backtest_result.png`），包含資金權益曲線 (Equity Curve)、回撤曲線 (Drawdown Curve) 與每日盈虧直方圖。
3. **無參數最佳化 (No Optimization)**：此階段專注於單次回測流程與 PNG 績效報表產出，暫不安裝/執行網格尋優或遺傳演算法。
4. **台指期合約規格**：設定符合台指期 (TX) 之交易參數（合約乘數 Size=200、最小變動點=1.0、滑點=1.0、手續費率或定額手續費、初始資金 NT$ 1,000,000）。

---

## 2. 詳細架構與設計規格 (Detailed Specifications)

### 2.1 數據讀取與解析 (`simulation/FITX.csv`)
- **檔案路徑**: `simulation/FITX.csv`
- **CSV 欄位格式規格**:
  ```csv
  datetime,open,high,low,close,volume,open_interest
  2024-01-02 08:46:00,17850,17865,17840,17860,1250,15000
  2024-01-02 08:47:00,17860,17875,17855,17870,980,15020
  ```
- **載入機制**:
  - `run_backtest.py` 啟動時檢查 `simulation/FITX.csv`。
  - 若檔案存在則直接解析；若不存在則自動備妥/創建示範用的 `simulation/FITX.csv` 檔案供立即驗證。
  - 將 CSV 資料轉置為 `BarData` 物件陣列並注入 `BacktestingEngine`（或經由 SQLite 載入引擎）。

### 2.2 回測引擎參數設定 (`Engine Configuration`)

| 配置項目 | 參數名稱 | 設定數值 | 說明 |
| :--- | :--- | :--- | :--- |
| **合約代碼** | `vt_symbol` | `TX00.LOCAL` | 台指期合約代碼 |
| **K 線週期** | `interval` | `Interval.MINUTE` | 1 分鐘 K 線 |
| **手續費** | `rate` | `0.00002` (或手續費固定定額) | 單筆交易手續費率 |
| **交易滑點** | `slippage` | `1.0` | 1 點 (每口 NT$ 200 損益) |
| **合約乘數** | `size` | `200` | 台指期每點 NT$ 200 |
| **最小跳動** | `pricetick` | `1.0` | 1 點 |
| **初始資本** | `capital` | `1,000,000` | 初始資金 NT$ 1,000,000 |

### 2.3 回測策略整合 (`Strategy Integration`)
- **策略名稱**: `TWFuturesMAStrategy`（雙均線策略）或自訂範例策略。
- **預設參數**: 快線 `fast_window=10`，慢線 `slow_window=30`，停損點數 `sl_points=30`，停利點數 `tp_points=60`。

### 2.4 PNG 視覺化報表產出 (`PNG Chart Report`)
回測結束後，系統除於 Console 列印統計數據外，將調用 `matplotlib` 自動導出 **`backtest_result.png`**：
1. **Top Panel**: 帳戶累計權益曲線 (Net Equity Curve vs Capital)。
2. **Middle Panel**: 最大回撤趴數曲線 (Drawdown Percentage Curve)。
3. **Bottom Panel**: 每日盈虧金額柱狀圖 (Daily PnL Bar Chart)。

---

## 3. 實作任務拆解 (Task Breakdown)

- [x] **Task 1**: 更新 `spec/build_run_backtest.md` 規格書（直接讀取 `simulation/FITX.csv`，優先產出 PNG，排除最佳化）。
- [ ] **Task 2**: 創建 `simulation/` 目錄與範例數據生成/讀取機制 (`simulation/FITX.csv`)。
- [ ] **Task 3**: 撰寫策略檔案 `strategies/tw_ma_strategy.py`。
- [ ] **Task 4**: 實作 `run_backtest.py` 主程式（讀取 CSV -> 初始化 BacktestingEngine -> 執行回測）。
- [ ] **Task 5**: 實作 `matplotlib` 權益與回撤圖表繪製邏輯，導出 `backtest_result.png`。
- [ ] **Task 6**: 執行 `python run_backtest.py` 驗證回測流程與 PNG 圖表產出。
