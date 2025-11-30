"""チャットモデルファクトリモジュール.

LangChainのinit_chat_model()を使用してチャットモデルを作成します。
設定は環境変数から読み込み、@lru_cacheによりシングルトンとして管理されます。
"""

from functools import lru_cache

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from app.config import settings


@lru_cache(maxsize=1)
def create_chat_model() -> BaseChatModel:
    """設定に基づいてチャットモデルを作成.

    app.configから読み込んだ設定を使用してチャットモデルを初期化します。
    @lru_cacheによりシングルトンとして管理されます。

    Returns:
        設定済みのBaseChatModelインスタンス

    Raises:
        ValueError: 環境変数OPENAI_API_KEYが設定されていない場合
        ImportError: 必要なパッケージがインストールされていない場合
    """
    return init_chat_model(
        model=settings.openai_model,
        model_provider="openai",
        api_key=settings.openai_api_key.get_secret_value(),
        temperature=settings.openai_temperature,
        timeout=settings.openai_timeout,
    )
