"""LangServe FastAPIサーバーモジュール.

LangGraphエージェントをREST APIとして公開します。

Endpoints:
    GET /: APIドキュメントへのリダイレクト
    GET /docs: Swagger UIドキュメント
    POST /agent/invoke: エージェントの同期実行
    POST /agent/stream: エージェントのストリーミング実行
    GET /agent/playground: LangServe Playground UI
    GET /health: ヘルスチェック
"""

from typing import Any

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain_core.messages import messages_from_dict, messages_to_dict
from langchain_core.runnables import RunnableLambda
from langserve import add_routes

from app.graph import graph
from app.state import AgentState


def transform_input(data: dict[str, Any]) -> dict[str, Any]:
    """入力メッセージを正しいBaseMessage形式に変換する.

    LangServe Playgroundから送信されるメッセージは、BaseMessageを継承した
    オブジェクトですが、正しいサブクラス（HumanMessage等）のインスタンスではありません。
    このため、LangChainのトレーサーがメッセージ形式を認識できずエラーが発生します。

    この関数は以下の手順でメッセージを再構築します:
    1. messages_to_dict(): 不正なBaseMessageオブジェクトを辞書形式に変換
    2. messages_from_dict(): 辞書から正しいHumanMessage/AIMessage等に再構築

    Args:
        data: messagesキーにメッセージリストを含む辞書

    Returns:
        正しいBaseMessageインスタンスに変換されたメッセージを含む辞書
    """
    messages = data.get("messages", [])
    return {"messages": messages_from_dict(messages_to_dict(messages))}


# FastAPIアプリケーションの作成
app = FastAPI(
    title="LangGraph Agent API",
    version="1.0.0",
    description="LangGraphエージェントのREST APIサーバー",
)


@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    """ルートパスから/docsへリダイレクト."""
    return RedirectResponse("/docs")


# メッセージ変換をグラフに適用
runnable = RunnableLambda(transform_input) | graph

# LangServeでグラフをREST APIとして公開
add_routes(
    app,
    runnable.with_types(input_type=AgentState),  # type: ignore[arg-type]
    path="/agent",
    enable_feedback_endpoint=False,
    enable_public_trace_link_endpoint=False,
    playground_type="default",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """ヘルスチェックエンドポイント."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
