# 快速開始指南

## 📋 前置要求

- Python 3.8+
- Node.js（可選，用於前端開發工具）
- Claude API 密鑰（從 [Anthropic](https://console.anthropic.com) 取得）

---

## 🚀 快速開始

### 步驟 1：安裝依賴

```bash
cd backend
pip install -r requirements.txt
```

### 步驟 2：設置 API 密鑰

複製 `.env.example` 為 `.env`：

```bash
cp .env.example .env
```

編輯 `.env` 文件，添加您的 Claude API 密鑰：

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 步驟 3：啟動後端

```bash
# 在 backend 目錄中
python -m uvicorn app.main:app --reload
```

後端將在 `http://localhost:8000` 啟動

訪問 API 文檔：`http://localhost:8000/docs`

### 步驟 4：啟動前端

在新終端窗口中：

```bash
cd frontend

# 使用 Python 的 HTTP 服務器（Python 3.8+）
python -m http.server 8001

# 或者使用 Node 的 http-server
npx http-server -p 8001
```

前端將在 `http://localhost:8001` 可用

---

## 🧪 測試資料結構實現

在 backend 目錄中運行：

```bash
python app/data_structures.py
```

這將運行所有資料結構的單元測試。

---

## 📚 項目結構

```
Project1-ConversationMemoryAgent/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # 包初始化
│   │   ├── main.py                  # FastAPI 主程序
│   │   ├── data_structures.py        # 資料結構實現
│   │   ├── agent.py                 # AI Agent 邏輯
│   │   └── session_manager.py        # 會話管理（可選）
│   ├── requirements.txt              # Python 依賴
│   ├── .env.example                 # 環境變數示例
│   └── .env                         # 環境變數（需要創建）
├── frontend/
│   ├── index.html                   # 主 HTML
│   ├── style.css                    # 樣式文件
│   └── app.js                       # 前端邏輯
├── README.md                        # 項目文檔
└── QUICKSTART.md                    # 本文件
```

---

## 🔌 API 端點

### 會話管理

- `POST /sessions/{session_id}` - 建立新會話
- `GET /sessions/{session_id}` - 獲取會話信息
- `DELETE /sessions/{session_id}` - 刪除會話
- `GET /sessions` - 列出所有活躍會話

### 對話

- `POST /sessions/{session_id}/messages` - 發送消息
- `GET /sessions/{session_id}/history` - 獲取對話歷史
- `POST /sessions/{session_id}/undo` - 撤回最後消息
- `DELETE /sessions/{session_id}/clear` - 清空對話
- `GET /sessions/{session_id}/summary` - 獲取對話摘要

### 統計

- `GET /stats` - 獲取系統統計信息
- `GET /health` - 健康檢查

---

## 💡 使用示例

### 建立會話

```bash
curl -X POST http://localhost:8000/sessions/user123 \
  -H "Content-Type: application/json" \
  -d '{"user_name": "Alice"}'
```

### 發送消息

```bash
curl -X POST http://localhost:8000/sessions/user123/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "你好！"}'
```

### 獲取對話歷史

```bash
curl http://localhost:8000/sessions/user123/history
```

---

## 🐛 常見問題

### 連接被拒絕

確保後端服務已啟動：
```bash
python -m uvicorn app.main:app --reload
```

### CORS 錯誤

CORS 已在後端配置。如果仍有問題，檢查前端 URL 是否正確。

### API 密鑰錯誤

確保：
1. `.env` 文件存在
2. `ANTHROPIC_API_KEY` 被正確設置
3. API 密鑰有效且有足夠的配額

---

## 📖 下一步

1. ✅ 完成基礎功能（本指南）
2. 📝 實現持久化存儲（數據庫）
3. 🔒 添加身份驗證和授權
4. 🚀 部署到生產環境
5. 📊 添加更多功能（優先隊列、複雜對話流等）

---

## 📞 獲得幫助

- 查看 API 文檔：`http://localhost:8000/docs`
- 檢查控制台日誌找出問題
- 查看項目 README 了解更多信息

**祝你學習愉快！🎓**
