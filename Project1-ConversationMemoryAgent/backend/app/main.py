"""
FastAPI 主程序
提供 REST API 接口供前端調用
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from .agent import MultiSessionAgent
from .data_structures import SessionCache

# 初始化 FastAPI 應用
app = FastAPI(
    title="對話記憶管理系統",
    description="具備記憶和上下文管理的 AI Agent",
    version="1.0.0"
)

# 添加 CORS 中間件（允許前端跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局初始化
multi_agent = MultiSessionAgent()
session_cache = SessionCache()


# ============ 數據模型 ============

class MessageRequest(BaseModel):
    """用戶消息請求"""
    content: str


class MessageResponse(BaseModel):
    """Agent 回應"""
    response: str


class ConversationHistoryResponse(BaseModel):
    """對話歷史響應"""
    messages: List[dict]
    length: int


class SessionCreateRequest(BaseModel):
    """建立會話請求"""
    user_name: Optional[str] = None


class SessionInfo(BaseModel):
    """會話信息"""
    session_id: str
    user_name: Optional[str]
    message_count: int


# ============ API 路由 ============

@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "對話記憶管理系統 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {"status": "healthy"}


# ============ 會話管理 API ============

@app.post("/sessions/{session_id}")
async def create_session(session_id: str, request: SessionCreateRequest):
    """
    建立新會話

    Args:
        session_id: 會話 ID（通常是 user_id）
        request: 會話創建請求

    Returns:
        會話信息
    """
    if session_cache.session_exists(session_id):
        raise HTTPException(status_code=400, detail="會話已存在")

    # 創建新會話
    multi_agent.create_session(session_id)
    session_cache.create_session(
        session_id,
        {"user_name": request.user_name}
    )

    return {
        "session_id": session_id,
        "message": "會話建立成功",
        "user_name": request.user_name
    }


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    獲取會話信息

    Args:
        session_id: 會話 ID

    Returns:
        會話信息
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    agent = multi_agent.get_session(session_id)
    session_info = session_cache.get_session(session_id)

    return {
        "session_id": session_id,
        "user_name": session_info.get("metadata", {}).get("user_name"),
        "message_count": agent.get_conversation_length()
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    刪除會話

    Args:
        session_id: 會話 ID

    Returns:
        刪除確認
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    multi_agent.delete_session(session_id)
    session_cache.delete_session(session_id)

    return {"message": "會話已刪除", "session_id": session_id}


@app.get("/sessions")
async def list_sessions():
    """
    列出所有活躍會話

    Returns:
        會話 ID 列表
    """
    sessions = multi_agent.get_all_sessions()
    return {
        "sessions": sessions,
        "count": len(sessions)
    }


# ============ 對話 API ============

@app.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, request: MessageRequest):
    """
    發送消息並獲得回應

    Args:
        session_id: 會話 ID
        request: 消息內容

    Returns:
        Agent 回應
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    if not request.content.strip():
        raise HTTPException(status_code=400, detail="消息內容不能為空")

    try:
        response = multi_agent.generate_response(session_id, request.content)
        return MessageResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"處理消息時出錯: {str(e)}")


@app.get("/sessions/{session_id}/history")
async def get_history(session_id: str, limit: Optional[int] = None):
    """
    獲取對話歷史

    Args:
        session_id: 會話 ID
        limit: 限制返回的消息數（可選）

    Returns:
        對話歷史
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    agent = multi_agent.get_session(session_id)
    history = agent.get_conversation_history()

    if limit and limit > 0:
        history = history[-limit:]

    return ConversationHistoryResponse(
        messages=history,
        length=len(history)
    )


@app.post("/sessions/{session_id}/undo")
async def undo_message(session_id: str):
    """
    撤回最後一條消息

    Args:
        session_id: 會話 ID

    Returns:
        撤回的消息或錯誤信息
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    agent = multi_agent.get_session(session_id)

    # 撤回兩條消息（用戶消息 + Agent 回應）
    msg1 = agent.undo_last_message()
    msg2 = agent.undo_last_message()

    if msg1 is None and msg2 is None:
        raise HTTPException(status_code=400, detail="沒有可撤回的消息")

    return {
        "message": "最後一個對話已撤回",
        "undo_count": 2 if msg2 else 1
    }


@app.delete("/sessions/{session_id}/clear")
async def clear_history(session_id: str):
    """
    清空對話歷史

    Args:
        session_id: 會話 ID

    Returns:
        清空確認
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    multi_agent.clear_session(session_id)

    return {"message": "對話歷史已清空", "session_id": session_id}


@app.get("/sessions/{session_id}/summary")
async def get_summary(session_id: str):
    """
    獲取對話摘要

    Args:
        session_id: 會話 ID

    Returns:
        對話摘要
    """
    if not session_cache.session_exists(session_id):
        raise HTTPException(status_code=404, detail="會話不存在")

    agent = multi_agent.get_session(session_id)
    summary = agent.summarize_conversation()

    return {
        "session_id": session_id,
        "summary": summary,
        "message_count": agent.get_conversation_length()
    }


# ============ 統計 API ============

@app.get("/stats")
async def get_stats():
    """
    獲取系統統計信息

    Returns:
        統計信息
    """
    all_sessions = multi_agent.get_all_sessions()
    total_messages = sum(
        multi_agent.get_session(sid).get_conversation_length()
        for sid in all_sessions
    )

    return {
        "active_sessions": len(all_sessions),
        "total_messages": total_messages,
        "sessions": all_sessions
    }


# ============ 錯誤處理 ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 異常處理"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
