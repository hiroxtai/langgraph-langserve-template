"""アプリケーション設定モジュール.

Pydantic Settingsを使用して.envファイルから環境変数を読み込み、
型安全にアクセスできる設定クラスを提供します。
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定クラス.

    .envファイルから環境変数を読み込み、型安全にアクセスできるようにします。

    Attributes:
        openai_api_key: OpenAI APIキー（SecretStrで保護）
        openai_model: 使用するOpenAIモデル名
        openai_temperature: モデルの温度パラメータ
        openai_max_tokens: 最大トークン数
        openai_timeout: APIタイムアウト秒数
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI API 設定
    openai_api_key: SecretStr
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: int | None = None
    openai_timeout: float = 60.0


# シングルトンインスタンス
# 注意: 実際に使用する際は .env ファイルで OPENAI_API_KEY を設定してください
try:
    settings = Settings()  # type: ignore
except Exception as e:
    raise RuntimeError(
        "設定の読み込みに失敗しました。.env ファイルを確認してください。\n"
        f"エラー詳細: {e}"
    ) from e
