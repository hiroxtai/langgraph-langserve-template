# LangGraph + LangServe Template

[![CI](https://github.com/hiroxtai/langgraph-langserve-template/actions/workflows/ci.yml/badge.svg)](https://github.com/hiroxtai/langgraph-langserve-template/actions/workflows/ci.yml)
[![PR Checks](https://github.com/hiroxtai/langgraph-langserve-template/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/hiroxtai/langgraph-langserve-template/actions/workflows/pr-checks.yml)

LangGraphエージェントをLangServeでREST API化するテンプレートプロジェクト

## 概要

このプロジェクトは、LangGraphで構築したチャットエージェントをLangServeを使用してREST APIとして公開するサンプル実装です。
Python 3.13とuvパッケージマネージャーを使用し、最新のベストプラクティスに従っています。

## 特徴

- 🌐 **REST API**: LangServeによるLangGraphエージェントのAPI化
- 💬 **Playground対応**: LangServe PlaygroundでチャットUIを提供
- 🔐 **セキュア**: Pydantic SecretStrによるAPIキーの安全な管理
- 🎯 **型安全**: Python 3.13の型ヒント + Pyrightによる静的型チェック
- 🚀 **プロバイダー非依存**: init_chat_model()による柔軟なLLM切り替え
- 🛠️ **開発環境完備**: Dev Container、VSCodeデバッグ構成、推奨拡張機能
- 📦 **モダンツール**: uv、Ruff、Pyrightによる高速で快適な開発体験

## 開発環境

- **Python**: 3.13
- **パッケージマネージャー**: uv
- **リンター/フォーマッター**: Ruff (Black互換設定、行長88文字)
- **型チェッカー**: Pyright (standardモード)
- **LLM**: OpenAI GPT-4o-mini (init_chat_modelで他のプロバイダーにも切り替え可能)

## セットアップ

### 1. 依存関係のインストール
```bash
uv sync
```

### 2. 環境変数の設定
`.env.example`をコピーして`.env`を作成し、APIキーを設定:
```bash
cp .env.example .env
# .envファイルを編集してOPENAI_API_KEYを設定
```

### 3. サーバーの起動

```bash
# FastAPIサーバーの起動
uv run python server.py

# または開発モード（自動リロード）
uv run uvicorn server:app --reload
```

サーバーは `http://localhost:8000` で起動します。

## 利用可能な機能

### API ドキュメント (Swagger UI)
ブラウザで `http://localhost:8000/docs` にアクセスすると、自動生成されたAPIドキュメントを確認できます。

### Playground
ブラウザで `http://localhost:8000/agent/playground/` にアクセスすると、チャット形式でエージェントと対話できるPlaygroundが利用できます。

### REST API エンドポイント

主なエンドポイントは以下の通りです:

- **Invoke (単発実行)**: `POST /agent/invoke`
- **Stream (ストリーミング実行)**: `POST /agent/stream`
- **Batch (バッチ実行)**: `POST /agent/batch`
- **Input Schema**: `GET /agent/input_schema`
- **Output Schema**: `GET /agent/output_schema`
- **Health Check**: `GET /health`

#### リクエスト例

```bash
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {
          "type": "human",
          "content": "こんにちは"
        }
      ]
    },
    "config": {}
  }'
```

#### レスポンス例

```json
{
  "output": {
    "messages": [
      {
        "type": "human",
        "content": "こんにちは"
      },
      {
        "type": "ai",
        "content": "こんにちは！どういったことをお手伝いできますか？"
      }
    ]
  }
}
```

## プロジェクト構造

```
langgraph-langserve-template/
├── app/                          # アプリケーションコード
│   ├── __init__.py              # パッケージ初期化
│   ├── config.py                # 設定管理 (Pydantic Settings)
│   ├── models.py                # チャットモデルファクトリ
│   ├── state.py                 # State定義 (AgentState)
│   └── graph.py                 # グラフ定義とコンパイル
├── server.py                     # LangServe FastAPIサーバー
├── pyproject.toml                # 依存関係とツール設定
├── uv.lock                       # ロックファイル
├── .python-version               # Pythonバージョン指定 (3.13)
├── .env.example                  # 環境変数テンプレート
├── .devcontainer/
│   └── devcontainer.json        # Dev Container設定
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI/CDパイプライン
│   │   ├── pr-checks.yml       # PRコード品質チェック
│   │   └── dependency-review.yml # 依存関係脆弱性チェック
│   └── copilot-instructions.md  # GitHub Copilot設定
└── .vscode/
    ├── settings.json            # エディタ設定
    ├── launch.json              # デバッグ構成
    └── extensions.json          # 推奨拡張機能
```

## 実装済み機能

### Phase 1 (完了) ✅

#### コア機能
- **設定管理** (`app/config.py`)
  - Pydantic Settingsによる型安全な環境変数管理
  - SecretStr型でAPIキーをセキュアに取り扱い
  - .envファイルからの自動読み込み

- **チャットモデル** (`app/models.py`)
  - `init_chat_model()`でプロバイダー非依存のモデル作成
  - LRUキャッシュによるインスタンス再利用
  - OpenAI GPT-4o-mini統合

- **State定義** (`app/state.py`)
  - LangGraph用のAgentState (Pydantic BaseModel)
  - add_messagesリデューサーでメッセージ履歴管理

- **グラフ実装** (`app/graph.py`)
  - シンプルな単一ノード構成 (START → agent → END)
  - チャットモデルによるメッセージ処理

- **LangServe API** (`server.py`)
  - FastAPIによるREST API公開
  - Swagger UI自動生成 (`/docs`)
  - Playground UI (`/agent/playground/`)
  - ヘルスチェックエンドポイント (`/health`)

#### 開発環境
- **Dev Container**: Python 3.13、uv、VSCode拡張機能の自動セットアップ
- **VSCodeデバッグ構成**: 5つの起動構成（メイン、現在のファイル、モジュール実行など）
- **推奨拡張機能**: Python、Pylance、Ruff、debugpy、Even Better TOML

### Phase 2 (未実装)
- ノード関数の分離 (`app/nodes/`)
- 条件分岐ロジックの分離 (`app/edges/`)
- 複数ノードによる処理チェーン
- エラーハンドリングの強化

### Phase 3 (未実装)
- ツール統合 (`app/tools/`)
  - 検索、計算、API呼び出しなど
- 外部APIとの連携
- RAG (Retrieval-Augmented Generation) 実装

## 開発ツール

### VSCodeでの開発

#### デバッグ実行
F5キーまたは「実行とデバッグ」パネルから以下の構成を選択:
- **Python: メインプログラム** - main.pyを実行
- **Python: 現在のファイル** - 開いているファイルを実行
- **Python: モジュールとして実行** - `python -m main`として実行
- **Python: デバッグ（外部ライブラリ含む）** - LangChain/LangGraph内部もステップ実行

#### Dev Container
VSCodeで「Dev Containers: Reopen in Container」を実行すると:
- Python 3.13環境が自動構築
- 依存関係が自動インストール（uv sync）
- 推奨拡張機能が自動インストール

### コード品質

#### リント・フォーマット
```bash
# チェック
uv run ruff check .

# 自動修正
uv run ruff check --fix .

# フォーマット
uv run ruff format .
```

**設定**: `pyproject.toml` の `[tool.ruff]`
- 行長: 88文字（Black互換）
- クォート: ダブルクォート優先
- インデント: スペース4つ

#### 型チェック
```bash
uv run pyright
```

**設定**: `pyproject.toml` の `[tool.pyright]`
- モード: standard
- Python バージョン: 3.13
- 全関数に型ヒント必須

## 依存関係

### 本番環境
- `langchain>=1.0.7` - チャットモデルのユニバーサル初期化
- `langchain-core>=1.0.5` - LangChainコア機能
- `langchain-openai>=1.0.3` - OpenAI統合
- `langgraph>=1.0.3` - グラフベースのワークフロー
- `langserve[all]>=0.3.3` - REST API公開
- `fastapi>=0.115.0` - Webフレームワーク
- `uvicorn>=0.32.0` - ASGIサーバー
- `pydantic-settings>=2.12.0` - 型安全な設定管理
- `python-dotenv>=1.2.1` - 環境変数読み込み

### 開発環境
- `pyright>=1.1.407` - 型チェッカー
- `ruff>=0.14.5` - リンター/フォーマッター

## アーキテクチャ

### LangGraphの基本概念

**State**
- グラフ全体で共有されるデータ構造
- このプロジェクトでは`AgentState` (Pydantic BaseModel)を使用
- `add_messages`リデューサーでメッセージ履歴を自動管理

**Nodes**
- 実際の処理を行う関数
- このプロジェクトでは`agent_node`がチャットモデルで応答を生成

**Edges**
- ノード間の遷移を定義
- このプロジェクトではシンプルな線形フロー (START → agent → END)

### LangServeの仕組み

**API公開**
```python
# add_routesで自動的にエンドポイントを生成
add_routes(
    app,
    runnable.with_types(input_type=AgentState),
    path="/agent",
)
```

**enabled_endpoints（本番環境推奨設定）**
```python
enabled_endpoints=[
    "invoke",          # 同期実行
    "stream",          # ストリーミング実行
    "input_schema",    # 入力スキーマ取得
    "output_schema",   # 出力スキーマ取得
]
```

**セキュリティ設定**
```python
enable_feedback_endpoint=False,           # フィードバック無効
enable_public_trace_link_endpoint=False,  # トレース無効
```

## CI/CD

### GitHub Actions

このプロジェクトでは3つのワークフローが自動実行されます:

#### 1. CI (`ci.yml`)
- **トリガー**: mainブランチへのpush、PRの作成・更新
- **実行内容**:
  - コードフォーマットチェック（Ruff）
  - リント（Ruff）
  - 型チェック（Pyright）
  - サーバー起動テスト（OPENAI_API_KEY設定時）

#### 2. PR Checks (`pr-checks.yml`)
- **トリガー**: PRの作成・更新
- **実行内容**:
  - コード品質チェック（フォーマット、リント、型チェック）
  - PRへの結果コメント自動投稿

#### 3. Dependency Review (`dependency-review.yml`)
- **トリガー**: mainブランチへのPR
- **実行内容**:
  - 依存関係の脆弱性チェック
  - 中程度以上の脆弱性で失敗
  - 問題発見時はPRにコメント

### Secrets設定

GitHub Actionsでアプリケーションテストを実行する場合:

1. GitHubリポジトリの Settings → Secrets and variables → Actions
2. `New repository secret` をクリック
3. Name: `OPENAI_API_KEY`、Secret: APIキーを入力

### ローカルでのCI実行

GitHub Actionsと同じチェックをローカルで実行:

```bash
# 全チェックを一括実行
uv run ruff format --check . && \
uv run ruff check . && \
uv run pyright
```

## トラブルシューティング

### エラー: "Tool replace_string_in_file is currently disabled"
開発中に編集ツールが無効化されている場合は、手動で変更を適用してください。

### APIキーエラー
`.env`ファイルに`OPENAI_API_KEY`が正しく設定されているか確認してください。

### ポート競合
既に8000番ポートが使用されている場合:
```bash
uv run uvicorn server:app --reload --port 8001
```

## 参考リンク

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangServe Documentation](https://python.langchain.com/docs/langserve)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangServe GitHub](https://github.com/langchain-ai/langserve)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

