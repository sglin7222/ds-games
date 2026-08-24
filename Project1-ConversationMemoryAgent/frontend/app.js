/**
 * 前端 JavaScript 應用
 * 管理 UI 交互和 API 調用
 */

const API_BASE = "http://localhost:8000";

// ============ 全局狀態 ============

let currentSessionId = null;
let currentSessionName = null;

// ============ DOM 元素 ============

const elements = {
    // 會話相關
    sessionIdInput: document.getElementById("sessionIdInput"),
    userNameInput: document.getElementById("userNameInput"),
    createSessionBtn: document.getElementById("createSessionBtn"),
    sessionsList: document.getElementById("sessionsList"),
    currentSession: document.getElementById("currentSession"),
    messageCount: document.getElementById("messageCount"),

    // 消息相關
    messagesContainer: document.getElementById("messagesContainer"),
    userInput: document.getElementById("userInput"),
    sendBtn: document.getElementById("sendBtn"),
    undoBtn: document.getElementById("undoBtn"),
    clearBtn: document.getElementById("clearBtn"),

    // 統計相關
    activeSessions: document.getElementById("activeSessions"),
    totalMessages: document.getElementById("totalMessages"),
    currentMessages: document.getElementById("currentMessages"),
    refreshStatsBtn: document.getElementById("refreshStatsBtn"),
};

// ============ 初始化 ============

document.addEventListener("DOMContentLoaded", () => {
    initializeEventListeners();
    updateStats();
    setInterval(updateStats, 10000); // 每 10 秒更新一次統計
});

function initializeEventListeners() {
    elements.createSessionBtn.addEventListener("click", createSession);
    elements.sendBtn.addEventListener("click", sendMessage);
    elements.undoBtn.addEventListener("click", undoMessage);
    elements.clearBtn.addEventListener("click", clearHistory);
    elements.refreshStatsBtn.addEventListener("click", updateStats);

    // 快捷鍵：Ctrl+Enter 發送消息
    elements.userInput.addEventListener("keydown", (e) => {
        if (e.ctrlKey && e.key === "Enter") {
            sendMessage();
        }
    });
}

// ============ 會話管理 ============

async function createSession() {
    const sessionId = elements.sessionIdInput.value.trim();
    const userName = elements.userNameInput.value.trim();

    if (!sessionId) {
        alert("請輸入會話 ID");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/sessions/${sessionId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user_name: userName || null,
            }),
        });

        if (response.ok) {
            selectSession(sessionId, userName);
            elements.sessionIdInput.value = "";
            elements.userNameInput.value = "";
            updateSessionsList();
            updateStats();
        } else {
            const error = await response.json();
            alert(`錯誤: ${error.detail || "建立會話失敗"}`);
        }
    } catch (error) {
        console.error("建立會話錯誤:", error);
        alert("建立會話時出錯");
    }
}

async function selectSession(sessionId, sessionName = null) {
    currentSessionId = sessionId;
    currentSessionName = sessionName;

    // 更新 UI
    elements.currentSession.textContent = `會話: ${sessionId}`;
    elements.userInput.disabled = false;
    elements.sendBtn.disabled = false;
    elements.undoBtn.disabled = false;
    elements.clearBtn.disabled = false;

    // 加載對話歷史
    await loadConversationHistory();
    updateSessionsList();
}

async function deleteSession(sessionId) {
    if (!confirm(`確定要刪除會話 ${sessionId} 嗎？`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/sessions/${sessionId}`, {
            method: "DELETE",
        });

        if (response.ok) {
            if (currentSessionId === sessionId) {
                currentSessionId = null;
                clearUI();
            }
            updateSessionsList();
            updateStats();
        }
    } catch (error) {
        console.error("刪除會話錯誤:", error);
        alert("刪除會話時出錯");
    }
}

async function updateSessionsList() {
    try {
        const response = await fetch(`${API_BASE}/sessions`);
        const data = await response.json();
        const sessions = data.sessions || [];

        const sessionsList = elements.sessionsList;
        if (sessions.length === 0) {
            sessionsList.innerHTML = '<p class="empty-state">沒有活躍會話</p>';
            return;
        }

        sessionsList.innerHTML = sessions
            .map((sessionId) => `
                <div class="session-item ${currentSessionId === sessionId ? "active" : ""}" onclick="selectSession('${sessionId}')">
                    <div class="session-item-info">
                        <span>${sessionId}</span>
                        <button class="session-item-delete" onclick="event.stopPropagation(); deleteSession('${sessionId}')">刪除</button>
                    </div>
                </div>
            `)
            .join("");
    } catch (error) {
        console.error("更新會話列表錯誤:", error);
    }
}

// ============ 消息管理 ============

async function sendMessage() {
    const content = elements.userInput.value.trim();

    if (!content) {
        alert("請輸入消息");
        return;
    }

    if (!currentSessionId) {
        alert("請先選擇或建立一個會話");
        return;
    }

    // 禁用輸入
    elements.sendBtn.disabled = true;
    elements.userInput.disabled = true;

    // 添加用戶消息到頁面
    addMessageToUI("user", content);
    elements.userInput.value = "";

    try {
        // 發送消息到後端
        const response = await fetch(
            `${API_BASE}/sessions/${currentSessionId}/messages`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ content }),
            }
        );

        if (response.ok) {
            const data = await response.json();
            // 添加 Assistant 回應到頁面
            addMessageToUI("assistant", data.response);
            updateStats();
        } else {
            const error = await response.json();
            addMessageToUI("assistant", `錯誤: ${error.detail || "無法獲得回應"}`);
        }
    } catch (error) {
        console.error("發送消息錯誤:", error);
        addMessageToUI("assistant", "發送消息時出錯");
    } finally {
        // 重新啟用輸入
        elements.sendBtn.disabled = false;
        elements.userInput.disabled = false;
        elements.userInput.focus();
    }
}

async function undoMessage() {
    if (!currentSessionId) {
        alert("請先選擇一個會話");
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE}/sessions/${currentSessionId}/undo`,
            {
                method: "POST",
            }
        );

        if (response.ok) {
            await loadConversationHistory();
            updateStats();
        } else {
            const error = await response.json();
            alert(`無法撤回: ${error.detail}`);
        }
    } catch (error) {
        console.error("撤回消息錯誤:", error);
        alert("撤回消息時出錯");
    }
}

async function clearHistory() {
    if (!currentSessionId) {
        alert("請先選擇一個會話");
        return;
    }

    if (!confirm("確定要清空所有對話歷史嗎？")) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE}/sessions/${currentSessionId}/clear`,
            {
                method: "DELETE",
            }
        );

        if (response.ok) {
            elements.messagesContainer.innerHTML =
                '<div class="welcome-message"><h3>👋 對話已清空</h3></div>';
            updateStats();
        }
    } catch (error) {
        console.error("清空對話錯誤:", error);
        alert("清空對話時出錯");
    }
}

async function loadConversationHistory() {
    if (!currentSessionId) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE}/sessions/${currentSessionId}/history`
        );
        const data = await response.json();

        elements.messagesContainer.innerHTML = "";

        if (data.messages.length === 0) {
            elements.messagesContainer.innerHTML =
                '<div class="welcome-message"><h3>👋 開始新對話</h3></div>';
            elements.messageCount.textContent = "消息: 0";
            return;
        }

        data.messages.forEach((msg) => {
            addMessageToUI(msg.role, msg.content, false);
        });

        elements.messageCount.textContent = `消息: ${data.length}`;
    } catch (error) {
        console.error("加載對話歷史錯誤:", error);
    }
}

function addMessageToUI(role, content, scroll = true) {
    const messageEl = document.createElement("div");
    messageEl.className = `message ${role}`;

    messageEl.innerHTML = `
        <div>
            <div class="message-role">${role === "user" ? "你" : "AI"}</div>
            <div class="message-content">${escapeHtml(content)}</div>
        </div>
    `;

    elements.messagesContainer.appendChild(messageEl);

    if (scroll) {
        elements.messagesContainer.scrollTop =
            elements.messagesContainer.scrollHeight;
    }
}

// ============ 統計與狀態 ============

async function updateStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();

        elements.activeSessions.textContent = data.active_sessions;
        elements.totalMessages.textContent = data.total_messages;

        if (currentSessionId) {
            const sessionResponse = await fetch(
                `${API_BASE}/sessions/${currentSessionId}`
            );
            const sessionData = await sessionResponse.json();
            elements.currentMessages.textContent = sessionData.message_count;
        }

        updateSessionsList();
    } catch (error) {
        console.error("更新統計錯誤:", error);
    }
}

function clearUI() {
    currentSessionId = null;
    elements.currentSession.textContent = "未選擇會話";
    elements.messagesContainer.innerHTML =
        '<div class="welcome-message"><h3>👋 歡迎使用對話記憶管理系統</h3><p>請先建立或選擇一個會話開始對話</p></div>';
    elements.userInput.value = "";
    elements.userInput.disabled = true;
    elements.sendBtn.disabled = true;
    elements.undoBtn.disabled = true;
    elements.clearBtn.disabled = true;
    elements.messageCount.textContent = "消息: 0";
}

// ============ 工具函數 ============

function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

// ============ 檢查後端連接 ============

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            console.log("✅ 後端連接正常");
            return true;
        }
    } catch (error) {
        console.error("❌ 無法連接後端:", error);
        alert("無法連接到後端服務。請確保後端服務在運行。");
        return false;
    }
}

// 在頁面加載時檢查連接
document.addEventListener("DOMContentLoaded", checkBackendConnection);
