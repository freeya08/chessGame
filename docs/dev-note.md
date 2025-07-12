# 開發者筆記：VS Code 設定與開發環境配置（2025-07-12）

## 1. Python 專案環境建立流程

### 建立虛擬環境
python -m venv .venv

### 啟用虛擬環境 (PowerShell)
.\.venv\Scripts\Activate.ps1

### 若出現執行權限問題：
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

### 安裝套件後匯出
pip install black
pip freeze > requirements.txt

## 2. VS Code 編輯器設定與顏色調整

### .vscode/settings.json 推薦內容
```
{
  "editor.fontSize": 22,
  "debug.console.fontSize": 18,
  "terminal.integrated.fontSize": 16,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```
- 使用 formatOnSave 可自動排版

## 3. Git 操作流程與原則

### 初始化 Git 倉庫
git init

### 加入遠端倉庫（選擇性）
git remote add origin <repo-url>

### 提交與推送
git add .
git commit -m "Initial commit"
git push -u origin main

✅ 每個專案建議使用獨立的 .venv 與 Git 倉庫

✅ 可建立 docs/dev-notes.md 保存設定與學習紀錄

❌ 不建議將太多開發設定寫入 README.md，會影響專案清晰度

## 4. 專案結構建議

```chessGame/
├── .vscode/                  ← VS Code 個別設定
│   └── settings.json
├── src/                      ← Python 原始碼
│   └── main.py
├── docs/                     ← 紀錄技術設定與開發筆記
│   └── dev-notes.md
├── requirements.txt          ← 套件清單
├── .gitignore
├── README.md                 ← 專案主說明文件
```
## 5. 小提醒筆記

- .venv 中安裝的套件只屬於該專案（不會互通）

- 若要節省空間可以刪掉 .venv，日後用 requirements.txt 還原

- VS Code 的 settings.json 是 JSON 格式，要注意逗號與縮排