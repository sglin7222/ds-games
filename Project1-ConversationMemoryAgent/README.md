# 專案 1：對話記憶管理系統

## 📌 專案概述

構建一個具備**對話記憶、上下文管理**的 AI Agent，使用基礎資料結構（棧、佇列、雜湊表）來管理對話狀態和任務。

---

## 🎯 學習目標

- ✅ 理解並實現：**棧（Stack）、佇列（Queue）、雜湊表（Hash Table）**
- ✅ 實現**對話歷史管理**（基於棧的回溯機制）
- ✅ 實現**任務佇列系統**（基於隊列的任務調度）
- ✅ 實現**用戶會話快取**（基於雜湊表）
- ✅ 整合 AI Agent（使用 Claude API）
- ✅ 構建前後端交互系統

---

## 📁 項目結構

```
Project1-ConversationMemoryAgent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI 主程序
│   │   ├── data_structures.py       # 自實現的資料結構
│   │   ├── agent.py                # AI Agent 核心邏輯
│   │   ├── session_manager.py       # 會話管理
│   │   └── models.py               # 數據模型
│   ├── requirements.txt             # 依賴包
│   └── test.py                      # 單元測試
├── frontend/
│   ├── index.html                  # 聊天界面
│   ├── style.css                   # 樣式
│   └── app.js                      # 前端邏輯
└── README.md                        # 本文件
```

---

## 🔧 資料結構設計

### 1. **棧（Stack）** - 對話歷史
```python
class ConversationStack:
    """管理對話歷史，支持回溯"""
    - push(message)    # 添加新消息
    - pop()            # 撤回最後一條消息
    - peek()           # 查看最後一條消息
    - get_history()    # 取得完整歷史
```

### 2. **佇列（Queue）** - 任務隊列
```python
class TaskQueue:
    """管理待處理任務"""
    - enqueue(task)    # 添加任務
    - dequeue()        # 執行下一個任務
    - peek()           # 查看下一個任務
    - size()           # 隊列長度
```

### 3. **雜湊表（Hash Table）** - 會話快取
```python
class SessionCache:
    """快速查詢用戶會話"""
    - set_session(user_id, data)
    - get_session(user_id)
    - remove_session(user_id)
    - session_exists(user_id)
```

---

## 🚀 核心功能

### Backend (Python FastAPI)
1. **會話管理** - 建立/恢復對話
2. **消息處理** - 接收用戶輸入，管理對話歷史
3. **AI 推理** - 調用 Claude API 生成回應
4. **任務佇列** - 管理後台任務（可選）
5. **上下文恢復** - 回溯到之前的對話狀態

### Frontend (React/Vue)
1. **聊天界面** - 實時對話展示
2. **對話歷史面板** - 查看和回溯對話
3. **會話管理** - 創建新會話/切換會話
4. **實時狀態** - 顯示任務佇列狀態

---

## 📊 實現步驟

### 階段 1：資料結構實現（第 1-2 週）
- [ ] 實現 Stack 類
- [ ] 實現 Queue 類
- [ ] 實現 Hash Table 類
- [ ] 編寫單元測試

### 階段 2：後端開發（第 2-3 週）
- [ ] 設置 FastAPI 項目
- [ ] 實現會話管理器
- [ ] 連接 Claude API
- [ ] 實現消息路由

### 階段 3：前端開發（第 3-4 週）
- [ ] 構建聊天界面
- [ ] 實現消息發送/接收
- [ ] 添加對話歷史功能
- [ ] 美化 UI

### 階段 4：集成與優化（第 4-5 週）
- [ ] 前後端集成
- [ ] 性能測試
- [ ] 錯誤處理
- [ ] 部署

---

## 💻 運行說明

### 後端啟動
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 前端運行
```bash
cd frontend
# 用簡單 HTTP 服務器
python -m http.server 8000
# 或使用 Live Server (VSCode 擴展)
```

訪問 `http://localhost:8000`

---

## 📖 預期學習成果

完成此專案後，你將：
1. 深入理解棧、佇列、雜湊表的實現原理
2. 掌握這些資料結構在實際系統中的應用
3. 理解 AI Agent 的基本架構
4. 掌握全棧開發基礎（後端 API + 前端）
5. 能獨立設計和實現類似系統

---

## 🎓 進階擴展

完成基礎版後，可以嘗試：
- 添加**優先權佇列**（高優先任務先執行）
- 實現**永久儲存**（數據庫持久化）
- 添加**多用戶支持**（並發會話管理）
- 實現**複雜對話流**（狀態機）

---

## 📚 參考資源

- Python 官方文檔
- FastAPI 教程
- Claude API 文檔
- 《Python 資料結構與演算法》

---

**讓我們開始吧！🚀**
