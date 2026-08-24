# 學習指南：對話記憶管理系統

## 🎯 學習目標

完成此專案後，你將掌握：

### 1. **資料結構深度理解**
- ✅ 棧（Stack）的實現和應用
- ✅ 佇列（Queue）的實現和應用
- ✅ 雜湊表（Hash Table）的實現和應用
- ✅ 時間/空間複雜度分析

### 2. **系統設計思想**
- ✅ 如何設計資料結構為應用程序服務
- ✅ 如何組織代碼和模塊化
- ✅ 前後端分離架構

### 3. **AI Agent 開發**
- ✅ 理解 AI Agent 的基本構成
- ✅ 對話管理和上下文維護
- ✅ 與外部 API 的集成

### 4. **全棧開發技能**
- ✅ Python 後端開發（FastAPI）
- ✅ 前端開發（HTML/CSS/JavaScript）
- ✅ API 設計和實現

---

## 📚 學習路徑

### 第 1-2 週：資料結構基礎

#### 目標
理解三個核心資料結構的原理，並從零實現它們。

#### 任務

1. **學習棧（Stack）**
   - 理解 LIFO 原理
   - 看代碼：[data_structures.py](backend/app/data_structures.py) 中的 `Stack` 類
   - 運行測試：`python app/data_structures.py`
   - 練習：實現 `reverse_string()` 函數（用棧反轉字符串）

2. **學習佇列（Queue）**
   - 理解 FIFO 原理
   - 看代碼：`Queue` 類
   - 練習：實現 `print_tasks()` 函數（模擬任務打印隊列）

3. **學習雜湊表（Hash Table）**
   - 理解雜湊函數和碰撞解決
   - 看代碼：`HashTable` 類
   - 練習：比較雜湊表和列表的查詢性能

#### 代碼閱讀檢查表
- [ ] 能解釋 Stack.push() 和 Stack.pop() 的時間複雜度
- [ ] 能解釋 Queue.enqueue() 為什麼使用 deque 而不是列表
- [ ] 能解釋雜湊表的載因（load factor）
- [ ] 能說出三種資料結構各自的優缺點

#### 練習作業
```python
# 練習 1：用棧實現括號匹配
def is_balanced(s: str) -> bool:
    # 檢查字符串中的括號是否匹配
    pass

# 練習 2：用佇列實現 BFS
def bfs(graph, start):
    # 廣度優先搜尋
    pass

# 練習 3：用雜湊表實現頻率統計
def count_frequencies(arr: list) -> dict:
    # 統計列表中各元素出現的次數
    pass
```

---

### 第 2-3 週：AI Agent 邏輯

#### 目標
理解 AI Agent 的架構，學會使用 Claude API。

#### 任務

1. **理解 Agent 架構**
   - 讀代碼：[agent.py](backend/app/agent.py) 中的 `ConversationAgent` 類
   - 理解對話棧如何管理歷史
   - 理解多會話如何隔離用戶數據

2. **Claude API 集成**
   - 設置 API 密鑰
   - 理解 `generate_response()` 如何工作
   - 嘗試修改系統提示詞

3. **測試 Agent**
   - 運行後端：`python -m uvicorn app.main:app --reload`
   - 使用 Swagger UI：`http://localhost:8000/docs`
   - 手動測試各個 API 端點

#### 代碼理解檢查表
- [ ] 能解釋棧在對話管理中的作用
- [ ] 能說出 `get_recent_context()` 為什麼有 n=10 的限制
- [ ] 能解釋多會話管理為什麼使用雜湊表
- [ ] 能指出代碼中哪些地方使用了我們自己實現的資料結構

#### 練習作業
```python
# 練習 1：擴展 Agent 功能
# 在 ConversationAgent 中添加一個方法：
def get_user_questions(self) -> List[str]:
    """返回用戶問過的所有問題"""
    pass

# 練習 2：實現對話分類
# 分析對話並分類為：問候、提問、陳述
def categorize_conversation(self) -> dict:
    """返回各類型消息的統計"""
    pass
```

---

### 第 3-4 週：後端 API 開發

#### 目標
理解 REST API 設計，實現各個端點。

#### 任務

1. **理解 API 設計**
   - 讀代碼：[main.py](backend/app/main.py)
   - 理解 REST 原則
   - 理解請求/響應模型

2. **API 端點測試**
   - 使用 curl 或 Postman 測試所有端點
   - 理解各端點的業務邏輯
   - 測試錯誤場景

3. **擴展 API**
   - 添加新端點（例如：導出對話為文本）
   - 添加數據驗證
   - 添加更多統計信息

#### 代碼理解檢查表
- [ ] 能解釋為什麼某些端點使用 POST/GET/DELETE
- [ ] 能指出代碼中使用的資料結構
- [ ] 能修改 API 響應格式
- [ ] 能添加新的 API 端點

#### 練習作業
```python
# 練習 1：添加導出功能
@app.get("/sessions/{session_id}/export")
async def export_conversation(session_id: str):
    """導出對話為 JSON/CSV 格式"""
    pass

# 練習 2：添加搜索功能
@app.get("/sessions/{session_id}/search")
async def search_messages(session_id: str, keyword: str):
    """搜索對話中包含特定關鍵字的消息"""
    pass
```

---

### 第 4-5 週：前端開發與集成

#### 目標
構建用戶界面，連接後端 API。

#### 任務

1. **理解前端代碼**
   - 讀代碼：[app.js](frontend/app.js)
   - 理解事件處理
   - 理解 API 調用流程

2. **測試前端**
   - 啟動前端：`python -m http.server 8001`
   - 測試所有 UI 功能
   - 測試錯誤提示

3. **改進 UI**
   - 優化樣式
   - 添加新功能（例如：消息搜索、導出）
   - 改進用戶體驗

#### 代碼理解檢查表
- [ ] 能解釋 DOM 事件監聽器
- [ ] 能修改 CSS 樣式
- [ ] 能添加新的 UI 元素
- [ ] 能調試 JavaScript 錯誤

#### 練習作業
```javascript
// 練習 1：添加消息搜索功能
async function searchMessages(keyword) {
    // 在對話歷史中搜索包含 keyword 的消息
    pass
}

// 練習 2：添加導出按鈕
function exportConversation() {
    // 導出當前對話為文件
    pass
}

// 練習 3：改進 UI 響應
// 在 .css 中添加黑暗主題支持
```

---

## 🧠 關鍵概念解釋

### 為什麼用棧管理對話歷史？

```
對話順序：
1. 用戶：「你好」
2. AI：「你好！」
3. 用戶：「告訴我 Python」
4. AI：「Python 是一種...」
5. 用戶：「撤回」 ← 應該回到狀態 3

棧的特性（LIFO）完美滿足這個需求！
最後添加的消息（狀態 4）先被移除。
```

### 為什麼用佇列管理任務？

```
任務隊列：
Task 1 → Task 2 → Task 3 → Task 4

用佇列（FIFO）保證任務按順序執行。
第一個進入的任務（Task 1）先被執行。
```

### 為什麼用雜湊表快速查詢會話？

```
100 個活躍用戶，要找「user_50」

用列表：最壞情況需要檢查 100 次 → O(n)
用雜湊表：直接定位 → O(1) ✨

速度快 100 倍！
```

---

## 🔍 代碼演練

### 演練 1：追蹤一條消息的旅程

一個用戶輸入「你好」，它如何經過系統？

```
1. 前端 (app.js)
   用戶點擊「發送」
   → sendMessage() 被調用
   → 調用 POST /sessions/{session_id}/messages
   
2. 後端 (main.py)
   → send_message() 端點被觸發
   → 調用 multi_agent.generate_response()
   
3. Agent (agent.py)
   → add_user_message()         # 消息推入棧
   → client.messages.create()    # 調用 Claude API
   → add_assistant_message()     # 回應推入棧
   
4. 前端回應
   → 收到 JSON 回應
   → addMessageToUI() 顯示消息
   → 更新統計信息
```

### 演練 2：撤回一條消息

用戶點擊「撤回」按鈕，發生了什麼？

```
1. 前端 (app.js)
   → undoMessage() 被調用
   → 發送 POST /sessions/{session_id}/undo
   
2. 後端 (main.py)
   → undo_message() 端點
   → 調用 agent.undo_last_message() × 2
     （撤回用戶消息和 AI 回應）
   
3. Agent (agent.py)
   → conversation_stack.pop() ← 棧的 pop 操作！
   → 移除最後添加的消息
   
4. 前端更新
   → 重新加載對話歷史
   → 更新 UI
```

---

## 🎯 進度檢查

完成各階段後，檢查你是否能：

**第 1-2 週**
- [ ] 從零實現一個棧類
- [ ] 從零實現一個佇列類
- [ ] 從零實現一個雜湊表類
- [ ] 分析三種結構的時間複雜度

**第 2-3 週**
- [ ] 解釋 Agent 如何使用棧
- [ ] 修改 Claude API 調用參數
- [ ] 添加新的 Agent 方法
- [ ] 理解多會話隔離

**第 3-4 週**
- [ ] 添加新的 API 端點
- [ ] 使用 curl 測試 API
- [ ] 修改 API 響應格式
- [ ] 添加數據驗證

**第 4-5 週**
- [ ] 修改 HTML 結構
- [ ] 修改 CSS 樣式
- [ ] 添加新的 JavaScript 事件處理
- [ ] 調試前端錯誤

---

## 📊 性能分析

運行你的代碼時，思考這些問題：

```
對於 100 個活躍用戶，每個用戶 50 條消息：

1. 查詢特定用戶的會話
   用戶名→用戶ID的映射（雜湊表）：O(1) ✓
   
2. 獲取用戶的對話歷史
   對話棧的遍歷：O(n) ✓
   
3. 刪除一個會話
   雜湊表的刪除：O(1) ✓
   
4. 統計所有消息
   遍歷所有會話和消息：O(m×n) ✓
```

---

## 🚀 進階挑戰

完成基礎版後，嘗試這些：

1. **持久化存儲**
   - 使用 SQLite 或 PostgreSQL 存儲對話
   - 實現對話加載和恢復

2. **優先級隊列**
   - 用優先級隊列替代普通佇列
   - 高優先級任務先執行

3. **知識圖譜**（預示第 2 期專案）
   - 從對話中提取實體和關係
   - 構建知識圖譜

4. **多模態內容**
   - 支持圖像、文件上傳
   - 管理媒體資源

---

## 📖 推薦閱讀

- 《算法導論》（第 10 章：基本資料結構）
- 《Python 食譜》（第 1 章：資料結構和算法）
- FastAPI 官方文檔
- Claude API 文檔

---

## 💡 學習建議

1. **動手實踐** - 不要只讀代碼，要運行和修改它
2. **調試模式** - 使用 print() 追蹤變量變化
3. **小步前進** - 每次修改一個小地方，測試
4. **寫註釋** - 為自己的代碼寫清楚的註釋
5. **做練習** - 完成上面的所有練習作業

---

**祝你學習愉快！如有問題，在本項目目錄中查看 QUICKSTART.md 或查看代碼的詳細註釋。🎓**
