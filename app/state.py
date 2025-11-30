"""LangGraphエージェントのステート定義モジュール.

LangGraphのグラフステートおよびLangServe APIの出力スキーマを定義します。
"""

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """LangGraphステート兼LangServe API入出力スキーマ.

    LangGraphのグラフ内部ステートとして機能し、
    add_messagesリデューサーによりメッセージ履歴を自動的にマージします。
    LangServe PlaygroundのチャットUIにも対応しています。

    Attributes:
        messages: メッセージ履歴のリスト（add_messagesリデューサーで管理）
    """

    model_config = {"arbitrary_types_allowed": True}

    messages: Annotated[list[BaseMessage], add_messages] = Field(
        ...,
        description="メッセージ履歴",
        json_schema_extra={"widget": {"type": "chat", "input": "messages"}},
    )
