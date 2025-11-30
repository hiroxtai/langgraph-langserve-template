# Copilot Instructions

## プロジェクト概要

Python 3.13 と `uv`パッケージマネージャーを使用したプロジェクトです。

## 開発環境

### パッケージ管理
- **依存関係管理には必ず`uv`を使用してください**（pipやpoetryは使用しない）
- 依存関係のインストール: `uv sync`
- パッケージの追加: `uv add <パッケージ名>`
- 開発用依存関係の追加: `uv add --dev <パッケージ名>`
- Pythonバージョンは3.13に固定（`.python-version`で指定）

### プロジェクトの実行
- メインスクリプトの実行: `uv run python main.py`
- uvの省略記法: `uv run main.py`

### コード品質・フォーマット
- **Ruffを使用してリント・フォーマットを実施**
- リント実行: `uv run ruff check .`
- 自動修正: `uv run ruff check --fix .`
- フォーマット: `uv run ruff format .`
- 設定は`pyproject.toml`の`[tool.ruff]`セクションに記載
- Black互換の設定（行長88文字、ダブルクォート優先）

### 型チェック
- **Pyrightを使用して静的型チェックを実施**
- 型チェック実行: `uv run pyright`
- 型チェックモード: `standard`（basic, standard, strictから選択可能）
- 設定は`pyproject.toml`の`[tool.pyright]`セクションに記載
- VSCodeではPylance（Pyright統合）が自動的に型エラーを表示

## 主要な規約

### コード構成
- `pyproject.toml`を使用した最新のPythonパッケージング標準に準拠
- コードスタイル: Ruffでリント・フォーマット（Black互換の設定）
- 行長: 88文字
- インデント: スペース4つ
- クォート: ダブルクォート優先
- 型ヒント: Python 3.13の型ヒントを積極的に使用（Pyrightで検証）

### 依存関係

## よくあるタスク

### 新機能の追加
1. `uv add`で必要な依存関係をインストール
2. `main.py`を更新するか、プロジェクトルートに新しいモジュールを作成
3. `uv run python <スクリプト名.py>`でローカルテスト

### 環境セットアップ
- Python 3.13が利用可能であることを確認（`python --version`で確認）
- `uv sync`を実行して仮想環境を作成し、依存関係をインストール
- uvは`.venv/`に仮想環境を自動管理します

### VSCode設定
- Ruff拡張機能がインストール済み（`charliermarsh.ruff`）
- Pylance（Pyright）で型チェックを実施（Python拡張に内蔵）
- `.vscode/settings.json`で保存時の自動フォーマット・リントを設定
- Pythonインタープリターは`.venv/bin/python`を使用
- 保存時に自動的にインポート整理とコード修正が実行されます
- 型エラーはエディタ上でリアルタイムに表示されます

## AIエージェント向けの注意事項

- これはグリーンフィールドプロジェクトです - アーキテクチャの決定は LangGraph のベストプラクティスに従ってください
- 適切な場合はPython 3.13の最新機能を使用してください（型ヒント、パターンマッチングなど）
- 複雑さがモジュール/パッケージへの整理を必要とするまで、プロジェクト構造をシンプルに保ってください
