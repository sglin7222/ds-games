"""
資料結構實現模塊
- Stack（棧）：對話歷史管理
- Queue（佇列）：任務隊列
- HashTable（雜湊表）：快速查詢和快取
"""

from typing import Any, Optional, List
from collections import deque


class Stack:
    """
    棧（LIFO - Last In First Out）
    用途：管理對話歷史，支持撤回和回溯
    """

    def __init__(self):
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        """將元素添加到棧頂"""
        self._items.append(item)

    def pop(self) -> Optional[Any]:
        """移除並返回棧頂元素"""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self) -> Optional[Any]:
        """查看棧頂元素但不移除"""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """檢查棧是否為空"""
        return len(self._items) == 0

    def size(self) -> int:
        """返回棧中元素個數"""
        return len(self._items)

    def get_all(self) -> List[Any]:
        """返回棧中所有元素（順序）"""
        return self._items.copy()

    def clear(self) -> None:
        """清空棧"""
        self._items.clear()

    def __str__(self) -> str:
        return f"Stack({self._items})"


class Queue:
    """
    佇列（FIFO - First In First Out）
    用途：任務隊列，按順序執行任務
    """

    def __init__(self):
        self._items: deque = deque()

    def enqueue(self, item: Any) -> None:
        """將元素添加到隊尾"""
        self._items.append(item)

    def dequeue(self) -> Optional[Any]:
        """移除並返回隊頭元素"""
        if self.is_empty():
            return None
        return self._items.popleft()

    def peek(self) -> Optional[Any]:
        """查看隊頭元素但不移除"""
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        """檢查隊列是否為空"""
        return len(self._items) == 0

    def size(self) -> int:
        """返回隊列中元素個數"""
        return len(self._items)

    def get_all(self) -> List[Any]:
        """返回隊列中所有元素"""
        return list(self._items)

    def clear(self) -> None:
        """清空隊列"""
        self._items.clear()

    def __str__(self) -> str:
        return f"Queue({list(self._items)})"


class HashTable:
    """
    雜湊表（Hash Table）
    用途：快速查詢和快取會話資料
    實現：基於 Python 字典的簡單雜湊表
    """

    def __init__(self, capacity: int = 100):
        self._table: dict = {}
        self.capacity = capacity
        self._size = 0

    def _hash(self, key: str) -> int:
        """簡單的雜湊函數"""
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        """將鍵值對存入雜湊表"""
        if key not in self._table:
            self._size += 1
        self._table[key] = value

    def get(self, key: str) -> Optional[Any]:
        """根據鍵獲取值"""
        return self._table.get(key)

    def remove(self, key: str) -> Optional[Any]:
        """移除指定鍵的元素"""
        if key in self._table:
            self._size -= 1
            return self._table.pop(key)
        return None

    def contains(self, key: str) -> bool:
        """檢查鍵是否存在"""
        return key in self._table

    def size(self) -> int:
        """返回雜湊表中元素個數"""
        return self._size

    def keys(self) -> List[str]:
        """返回所有鍵"""
        return list(self._table.keys())

    def values(self) -> List[Any]:
        """返回所有值"""
        return list(self._table.values())

    def items(self) -> List[tuple]:
        """返回所有鍵值對"""
        return list(self._table.items())

    def clear(self) -> None:
        """清空雜湊表"""
        self._table.clear()
        self._size = 0

    def __str__(self) -> str:
        return f"HashTable({self._table})"


class ConversationStack(Stack):
    """
    對話棧的特殊實現
    存儲對話消息，支持回溯
    """

    def add_message(self, role: str, content: str) -> None:
        """添加對話消息"""
        message = {
            "role": role,  # "user" 或 "assistant"
            "content": content
        }
        self.push(message)

    def get_conversation_history(self) -> List[dict]:
        """獲取完整對話歷史"""
        return self.get_all()

    def undo_last_message(self) -> Optional[dict]:
        """撤回最後一條消息"""
        return self.pop()

    def get_recent_messages(self, n: int = 5) -> List[dict]:
        """獲取最近 n 條消息"""
        all_messages = self.get_all()
        return all_messages[-n:] if len(all_messages) > 0 else []


class TaskQueue(Queue):
    """
    任務隊列的特殊實現
    管理待執行的任務
    """

    def add_task(self, task_id: str, task_type: str, data: dict) -> None:
        """添加任務到隊列"""
        task = {
            "id": task_id,
            "type": task_type,
            "data": data,
            "status": "pending"
        }
        self.enqueue(task)

    def get_next_task(self) -> Optional[dict]:
        """獲取下一個待執行的任務"""
        return self.peek()

    def complete_task(self) -> Optional[dict]:
        """完成並移除下一個任務"""
        return self.dequeue()

    def get_pending_tasks(self) -> List[dict]:
        """獲取所有待執行任務"""
        return self.get_all()


class SessionCache(HashTable):
    """
    會話快取的特殊實現
    快速管理用戶會話
    """

    def create_session(self, user_id: str, session_data: dict) -> None:
        """建立新會話"""
        session = {
            "user_id": user_id,
            "conversation_stack": ConversationStack(),
            "task_queue": TaskQueue(),
            "metadata": session_data
        }
        self.put(user_id, session)

    def get_session(self, user_id: str) -> Optional[dict]:
        """獲取用戶會話"""
        return self.get(user_id)

    def session_exists(self, user_id: str) -> bool:
        """檢查會話是否存在"""
        return self.contains(user_id)

    def delete_session(self, user_id: str) -> None:
        """刪除會話"""
        self.remove(user_id)

    def get_all_users(self) -> List[str]:
        """獲取所有活躍用戶"""
        return self.keys()


# ============ 測試函數 ============

def test_stack():
    """測試棧"""
    print("\n===== 測試 Stack =====")
    stack = Stack()
    stack.push("Hello")
    stack.push("World")
    stack.push("!")

    print(f"棧內容: {stack}")
    print(f"棧頂: {stack.peek()}")
    print(f"彈出: {stack.pop()}")
    print(f"棧大小: {stack.size()}")
    print(f"棧歷史: {stack.get_all()}")


def test_queue():
    """測試佇列"""
    print("\n===== 測試 Queue =====")
    queue = Queue()
    queue.enqueue("Task 1")
    queue.enqueue("Task 2")
    queue.enqueue("Task 3")

    print(f"隊列內容: {queue}")
    print(f"隊頭: {queue.peek()}")
    print(f"出隊: {queue.dequeue()}")
    print(f"隊列大小: {queue.size()}")
    print(f"隊列歷史: {queue.get_all()}")


def test_hash_table():
    """測試雜湊表"""
    print("\n===== 測試 HashTable =====")
    ht = HashTable()
    ht.put("user1", {"name": "Alice", "age": 25})
    ht.put("user2", {"name": "Bob", "age": 30})

    print(f"獲取 user1: {ht.get('user1')}")
    print(f"包含 user2: {ht.contains('user2')}")
    print(f"所有鍵: {ht.keys()}")
    print(f"表大小: {ht.size()}")


def test_conversation_stack():
    """測試對話棧"""
    print("\n===== 測試 ConversationStack =====")
    conv = ConversationStack()
    conv.add_message("user", "你好")
    conv.add_message("assistant", "你好！有什麼我可以幫助你的嗎？")
    conv.add_message("user", "告訴我關於 Python")

    print(f"對話歷史: {conv.get_conversation_history()}")
    print(f"最近消息: {conv.get_recent_messages(2)}")
    print(f"撤回: {conv.undo_last_message()}")


def test_task_queue():
    """測試任務隊列"""
    print("\n===== 測試 TaskQueue =====")
    queue = TaskQueue()
    queue.add_task("task1", "analysis", {"topic": "AI"})
    queue.add_task("task2", "search", {"query": "機器學習"})

    print(f"待執行任務: {queue.get_pending_tasks()}")
    print(f"下一個任務: {queue.get_next_task()}")
    print(f"完成任務: {queue.complete_task()}")


def test_session_cache():
    """測試會話快取"""
    print("\n===== 測試 SessionCache =====")
    cache = SessionCache()
    cache.create_session("user123", {"language": "zh_TW"})
    cache.create_session("user456", {"language": "en"})

    session = cache.get_session("user123")
    print(f"會話存在: {cache.session_exists('user123')}")
    print(f"所有活躍用戶: {cache.get_all_users()}")
    print(f"會話大小: {cache.size()}")


if __name__ == "__main__":
    test_stack()
    test_queue()
    test_hash_table()
    test_conversation_stack()
    test_task_queue()
    test_session_cache()
    print("\n✅ 所有測試完成！")
