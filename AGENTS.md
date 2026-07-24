# AGENTS.md - FuturesTradingSystem 開發與風格規範指南

本文件為 **FuturesTradingSystem** 專案的 AI Agent 操作與風格規範文件。

## 🎯 核心原則

1. **Python 虛擬環境強制規範 (CRITICAL)**：
   * **解釋器位置**：專案上層目錄 `..\Scripts\python.exe`（絕對路徑：`c:\Users\user\Desktop\workspace\FuturesTradingSystem\Scripts\python.exe`）。
   * **禁止使用全域 Python**：切勿使用系統 `python` 或 `pip` 命令。
   * **套件安裝命令**：必須使用 `..\Scripts\python.exe -m pip install <package_name>`。
   * **腳本執行命令**：必須使用 `..\Scripts\python.exe <script_path>`（例如：`..\Scripts\python.exe run_backtest.py`）。

2. **溝通與語言**：
   * 所有回應、註解說明與文檔一律使用 **繁體中文**。

3. **開發與驗證**：
   * 變更後必須透過專案虛擬環境執行驗證（例如執行回測腳本或測試單元）。
   * 保持代碼結構乾淨、錯誤訊息透明，不隱瞞 Exception。

詳細規範請參考 [.agents/rules.md](file:///c:/Users/user/Desktop/workspace/FuturesTradingSystem/FuturesTradingSystem/.agents/rules.md)。
