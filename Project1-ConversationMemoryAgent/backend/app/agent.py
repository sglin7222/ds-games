"""
AI Agent 核心邏輯
使用 Claude API 進行對話推理
"""

import anthropic
from typing import Optional, List, Dict, Any
from .data_structures import ConversationStack


class ConversationAgent:
    """
    對話 Agent 類
    管理與用戶的多轉對話，使用棧管理對話歷史
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Agent

        Args:
            api_key: Claude API 密鑰，默認從環境變數讀取
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_stack = ConversationStack()
        self.model = "claude-3-5-sonnet-20241022"

    def add_user_message(self, content: str) -> None:
        """添加用戶消息到對話棧"""
        self.conversation_stack.add_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        """添加 Assistant 消息到對話棧"""
        self.conversation_stack.add_message("assistant", content)

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """獲取完整對話歷史"""
        return self.conversation_stack.get_conversation_history()

    def undo_last_message(self) -> Optional[Dict[str, str]]:
        """撤回最後一條消息"""
        return self.conversation_stack.undo_last_message()

    def get_recent_context(self, n: int = 10) -> List[Dict[str, str]]:
        """獲取最近的 n 條消息作為上下文"""
        return self.conversation_stack.get_recent_messages(n)

    def generate_response(self, user_input: str, use_full_history: bool = True) -> str:
        """
        使用 Claude API 生成回應

        Args:
            user_input: 用戶輸入
            use_full_history: 是否使用完整對話歷史（True）或只用最近消息（False）

        Returns:
            Agent 的回應文本
        """
        # 添加用戶消息到棧
        self.add_user_message(user_input)

        # 準備對話歷史
        if use_full_history:
            messages = self.get_conversation_history()
        else:
            messages = self.get_recent_context(n=10)

        # 調用 Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system="你是一個有幫助的 AI 助手。用繁體中文回應。簡潔而有用。",
                messages=messages
            )

            # 提取回應文本
            assistant_response = response.content[0].text

            # 添加 Assistant 回應到棧
            self.add_assistant_message(assistant_response)

            return assistant_response

        except Exception as e:
            error_message = f"錯誤: {str(e)}"
            self.add_assistant_message(error_message)
            return error_message

    def clear_conversation(self) -> None:
        """清空對話歷史"""
        self.conversation_stack.clear()

    def get_conversation_length(self) -> int:
        """獲取對話長度（消息數）"""
        return self.conversation_stack.size()

    def summarize_conversation(self) -> str:
        """
        使用 Claude 生成對話摘要

        Returns:
            對話摘要
        """
        history = self.get_conversation_history()

        if len(history) == 0:
            return "沒有對話歷史"

        # 格式化對話歷史
        conversation_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in history
        ])

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system="你是一個文本分析助手。簡要總結以下對話的關鍵要點。用繁體中文回應。",
                messages=[{
                    "role": "user",
                    "content": f"請總結這個對話:\n\n{conversation_text}"
                }]
            )

            return response.content[0].text

        except Exception as e:
            return f"無法生成摘要: {str(e)}"


class MultiSessionAgent:
    """
    多會話 Agent 管理器
    使用雜湊表管理多個用戶的獨立對話
    """

    def __init__(self):
        """初始化多會話管理器"""
        self.agents: Dict[str, ConversationAgent] = {}

    def create_session(self, session_id: str) -> ConversationAgent:
        """
        為新用戶建立會話

        Args:
            session_id: 會話 ID（通常是 user_id）

        Returns:
            新建立的 Agent
        """
        if session_id not in self.agents:
            self.agents[session_id] = ConversationAgent()
        return self.agents[session_id]

    def get_session(self, session_id: str) -> Optional[ConversationAgent]:
        """
        獲取現有會話

        Args:
            session_id: 會話 ID

        Returns:
            Agent 或 None
        """
        return self.agents.get(session_id)

    def session_exists(self, session_id: str) -> bool:
        """檢查會話是否存在"""
        return session_id in self.agents

    def delete_session(self, session_id: str) -> bool:
        """
        刪除會話

        Returns:
            是否成功刪除
        """
        if session_id in self.agents:
            del self.agents[session_id]
            return True
        return False

    def get_all_sessions(self) -> List[str]:
        """獲取所有活躍會話 ID"""
        return list(self.agents.keys())

    def generate_response(self, session_id: str, user_input: str) -> str:
        """
        為特定會話生成回應

        Args:
            session_id: 會話 ID
            user_input: 用戶輸入

        Returns:
            Agent 回應
        """
        # 如果會話不存在，自動建立
        if not self.session_exists(session_id):
            self.create_session(session_id)

        agent = self.get_session(session_id)
        return agent.generate_response(user_input)

    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """獲取特定會話的對話歷史"""
        agent = self.get_session(session_id)
        if agent:
            return agent.get_conversation_history()
        return []

    def clear_session(self, session_id: str) -> bool:
        """清空特定會話的對話"""
        agent = self.get_session(session_id)
        if agent:
            agent.clear_conversation()
            return True
        return False


# ============ 測試函數 ============

def test_conversation_agent():
    """測試對話 Agent"""
    print("\n===== 測試 ConversationAgent =====")

    agent = ConversationAgent()

    # 模擬對話
    print("\n用戶: 你好！")
    # response1 = agent.generate_response("你好！")
    # print(f"Agent: {response1}")

    print("\n用戶: 介紹一下資料結構")
    # response2 = agent.generate_response("介紹一下資料結構")
    # print(f"Agent: {response2}")

    print(f"\n對話長度: {agent.get_conversation_length()}")
    # print(f"\n對話摘要:\n{agent.summarize_conversation()}")


def test_multi_session_agent():
    """測試多會話 Agent"""
    print("\n===== 測試 MultiSessionAgent =====")

    manager = MultiSessionAgent()

    # 模擬多個用戶的對話
    print("\n用戶 1 的會話:")
    # response1 = manager.generate_response("user1", "你好，我叫 Alice")
    # print(f"回應: {response1}")

    print("\n用戶 2 的會話:")
    # response2 = manager.generate_response("user2", "你好，我叫 Bob")
    # print(f"回應: {response2}")

    print(f"\n活躍會話: {manager.get_all_sessions()}")


if __name__ == "__main__":
    test_conversation_agent()
    test_multi_session_agent()
