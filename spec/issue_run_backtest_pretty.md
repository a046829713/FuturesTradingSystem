# 議題討論與規劃：`run_backtest.py` 專業化視覺呈現與 vn.py UI 圖表實作分析

本文件紀錄關於 `run_backtest.py` 回測視覺化提升與 vn.py 官方 GUI 介面實作原理的討論與技術分析結果。

---

## 一、 vn.py 官方 GUI 介面實作原理分析

在官方網站與文檔中看到的暗黑風格專業回測介面（如 `vnpy_ctabacktester` 模組），其底層架構與實現機制如下：

### 1. 核心技術棧
- **GUI 框架**：`PySide6`（或 `PyQt5`）—— Qt 6 for Python 視窗與 UI 元件庫。
- **高速動態繪圖庫**：`pyqtgraph` —— 專為 Python 科學計算與金融數據打造的高效能 2D 圖表繪製庫，支援極高幀率的縮放 (Zoom)、拖拽 (Pan) 與游標跨線 (Crosshair) 聯動。
- **UI 元件模組**：`vnpy.trader.ui` / `vnpy_ctabacktester` —— 包含 `BacktesterChart` 與 `CtaBacktesterApp` 視窗管理元件。

### 2. 畫面區域拆解與圖表構成
官方介面主要由三大區塊組成：
1. **左側與中央控制/統計面板**：
   - **策略與合約參數設定**：交易策略選單、本地代碼 (如 `IF888.CFFEX` / `TX00.LOCAL`)、K線週期、回測起訖日期、手續費率、滑點、合約乘數等。
   - **KPI 關鍵統計指標**：首末交易日、勝率、盈虧比、總收益率、年化收益率、最大回撤、總手續費與總滑點等。
   - **實時 Log 日誌視窗**：顯示歷史數據載入進度、回放百分比、逐日盯市結算日誌。
2. **右側四大專業圖表 (pyqtgraph 繪製)**：
   - **賬戶淨值 (Account Capital / Net Equity Curve)**：折線圖，即時反應資金曲線增長情況。
   - **淨值回撤 (Net Value Drawdown Curve)**：下壓陰影填充圖 (Area Plot)，直觀顯示資金回撤幅度與復甦期。
   - **每日盈虧 (Daily PnL Bar Chart)**：紅綠雙色柱狀圖，呈現日盈虧波動與極端盈虧天數。
   - **盈虧分佈 (PnL Distribution Graph)**：機率密度/頻率直方圖，展示單次或單日盈虧的常態分佈與偏態。

---

## 二、 現有虛擬環境套件相容性評估

針對使用者提問：「**是否需要再安裝 qt6 或是其他套件才能實現？**」

經執行專案虛擬環境 (`c:\Users\user\Desktop\workspace\FuturesTradingSystem\Scripts\python.exe`) 檢測：
- **`PySide6`**：已成功安裝（提供 Qt6 基礎架構）。
- **`pyqtgraph`**：已成功安裝（提供圖表繪製引擎）。

**結論**：**無需再額外安裝 Qt6 或 PySide6 套件**，現有環境已具備運行與呈現官方級別 Qt 圖表的所有基礎依賴！

---

## 三、 `run_backtest.py` 視覺專業化提升方案

目前 [run_backtest.py](file:///c:/Users/user/Desktop/workspace/FuturesTradingSystem/FuturesTradingSystem/run_backtest.py) 產生的 Matplotlib 圖片較為簡略（僅有白底雙圖）。為了達到官方 GUI 般專業且高品質的呈現效果，提出以下三種優化路徑：

### 方案 A：原生 PySide6 + pyqtgraph 互動視窗 (完全還原官方圖表)
- **說明**：利用已安裝的 `PySide6` 與 `pyqtgraph`，在執行 `run_backtest.py` 後呼叫 `BacktestingEngine.show_chart()`，彈出原汁原味的 4 大暗黑主題互動圖表視窗。
- **優勢**：可滑動、放大縮小、游標觀看每日數值，互動體驗最佳。
- **適用場景**：在地開發者手動執行回測與實時分析。

### 方案 B：專業暗黑風格 (Dark Theme) Matplotlib 4 圖 PNG Dashboard 導出
- **說明**：重構 [run_backtest.py](file:///c:/Users/user/Desktop/workspace/FuturesTradingSystem/FuturesTradingSystem/run_backtest.py) 中的 `generate_png_report` 函數：
  1. 改用高對比深色背景 (Dark Slate `#1e1e1e`) 與金融質感調色盤。
  2. 補全為 4 大圖表（淨值曲線、回撤陰影圖、每日盈虧紅綠柱狀圖、盈虧分佈直方圖/密度圖）。
  3. 側邊或頂部繪製 **KPI Metric Summary Cards**（文字與數據方塊，如總收益、最大回撤、夏普比率、勝率等）。
- **優勢**：無需開啟視窗，離線自動生成高畫質、可直接放進報告或簡報的 PNG 圖片。
- **適用場景**：自動化回測、批量參數優化報告導出。

### 方案 C：互動式 Web HTML Dashboard 導出 (Plotly Dark Theme)
- **說明**：使用 `plotly` 生成單一離線 HTML 報告，內建暗黑主題與多圖聯動 (Subplots)。
- **優勢**：可在任何瀏覽器開啟，兼具互動性（Tooltip/Zoom）與跨平台便利性。
- **適用場景**：跨裝置展示與團隊分享。

---

## 四、 後續建議行動計畫 (Next Steps)

1. **升級 `run_backtest.py`**：
   - 整合 PySide6 事件迴圈，確保 `show_chart()` 視窗可穩定顯示並持續互動。
   - 將導出的 PNG 報告升級為 **Dark Theme 4 圖+統計卡片** 的專業風格。
2. **保持規範**：
   - 繼續維持 `..\Scripts\python.exe` 虛擬環境執行。
   - 保持模組化與繁體中文說明。

---
*討論紀錄同步時間：2026-07-24*
