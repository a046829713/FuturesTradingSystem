# Antigravity Agent 專案開發與風格規範 (Project Development & Style Rules)

本文件定義 Antigravity AI Agent 於 `FuturesTradingSystem` 專案中的行為規範、開發流程與環境配置指令。AI Agent 於此專案進行任何操作時均需嚴格遵守本規範。

---

## 1. Python 解釋器與虛擬環境規範 (CRITICAL)

### 1.1 虛擬環境定位原則
* **嚴禁使用系統全域 Python / pip**（例如直接呼叫 `python` 或 `pip`）。
* **強制使用專案虛擬環境**：專案上層目錄即為 Python 虛擬環境，AI Agent 必須自動搜尋並使用該虛擬環境下的 Python 解釋器。
  * **相對路徑**：`..\Scripts\python.exe` / `..\Scripts\pip.exe`
  * **絕對路徑**：`c:\Users\user\Desktop\workspace\FuturesTradingSystem\Scripts\python.exe`

### 1.2 套件安裝與管理規範
* **套件安裝指令**：不論安裝、更新或移除任何 Python 套件，必須在專案虛擬環境下運作。
  * ✅ **標準安裝指令**：`..\Scripts\python.exe -m pip install <package_name>`
  * ✅ **需求清單安裝指令**：`..\Scripts\python.exe -m pip install -r requirements.txt`
  * ❌ **禁止指令**：`pip install ...` 或 `python -m pip install ...`

### 1.3 程式與腳本執行規範
* **腳本執行指令**：執行專案內任何 Python 腳本（例如回測 `run_backtest.py`、策略模組測試、驗證腳本等），必須明確指定虛擬環境解釋器。
  * ✅ **標準執行指令**：`..\Scripts\python.exe run_backtest.py`
  * ❌ **禁止指令**：`python run_backtest.py`

---

## 2. 語言與溝通規範 (Language & Communication)

1. **繁體中文回應**：所有與使用者的對話、問題解答、變更摘要與說明一律使用台灣繁體中文。
2. **註解與文件**：新增或修改代碼中的 Docstring、註解及說明文件時，統一使用繁體中文。
3. **精確與簡潔**：回應需重點突出、條理清晰，避免冗長無關的文字。

---

## 3. 開發與代碼風格規範 (Coding Standards)

1. **模組與目錄結構**：
   * `strategies/`：交易策略邏輯與指標計算。
   * `simulation/`：回測引擎、績效分析與模擬交易環境。
   * `config/`：專案與交易參數設定檔。
   * `spec/`：規格說明與系統需求文件。
2. **代碼完整性**：
   * 修改代碼時，必須完整維護現有函式簽名與 API 合約，避免無意間造成 Side Effects。
   * 保留既有註解與邏輯說明，嚴禁無故刪除非相關註解。
3. **錯誤處理與日誌**：
   * 嚴禁靜默吞掉例外（Silent Catch / Empty Except block）。
   * 所有錯誤捕捉必須記錄完整 Exception 訊息或進行合適處置。

---

## 4. 驗證與交付流程 (Verification Workflow)

1. **先檢查再修改**：進行修改前，應先檢視相關檔案與現有邏輯，不得假設未確認的變數或檔名。
2. **實體執行驗證**：代碼修改完成後，**必須**使用專案虛擬環境解釋器（`..\Scripts\python.exe`）執行測試或回測腳本進行實體驗證。
3. **成果回報**：確認執行成功、無語法或執行期錯誤後，方可向使用者回報任務完成，並提供明確的變更摘要與驗證結果。
