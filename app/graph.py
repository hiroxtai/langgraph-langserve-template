"""LangGraphワークフロー定義モジュール.

StateGraphを使用してチャットエージェントのワークフローを定義します。
START -> agent -> ENDの単純な線形フローで構成されています。
"""

from langchain_core.messages import BaseMessage
from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.models import create_chat_model
from app.state import AgentState


def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:
    """エージェントノード - チャットモデルで応答を生成.

    メッセージ履歴をチャットモデルに渡して応答を生成します。

    Args:
        state: 現在のグラフステート（メッセージ履歴を含む）

    Returns:
        応答メッセージを含む辞書: {"messages": [response_message]}
    """
    messages = state.messages

    # チャットモデルを取得して応答を生成
    llm = create_chat_model()
    response = llm.invoke(messages)

    return {"messages": [response]}


# グラフの構築（入力・出力スキーマを明示的に指定）
workflow = StateGraph(AgentState)

# ノードの追加
workflow.add_node("agent", agent_node)

# エッジの定義
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# グラフのコンパイル
graph = workflow.compile()
