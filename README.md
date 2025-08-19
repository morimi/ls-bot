# LS-BOT

IDOLY PRIDE公式サイト用のチャットボットシステム

## 📖 概要

LS-BOTは、IDOLY PRIDE公式サイトに設置するゲーム問い合わせチャットボットです。RAG（Retrieval-Augmented Generation）技術を活用し、公式サイトの情報を基にユーザーの質問に回答します。

### 主要機能

- 公式サイト右下に常駐するチャットボタン
- カテゴリー別質問対応（キャラクター、ライブイベント、グッズ、楽曲、生放送、その他）
- キャラクター名の表記揺れ対応
- RAGによる正確な情報検索と回答生成

## 🛠 技術スタック

### フロントエンド
- **React** - UIライブラリ
- **TypeScript** - 型安全性の確保
- **Tailwind CSS** - スタイリング
- **Vite** - ビルドツール
- **Jotai** - 状態管理（必要に応じて）

### バックエンド
- **Python** - プログラミング言語
- **FastAPI** - Webフレームワーク
- **ChromaDB** - ベクトルデータベース
- **OpenAI GPT-4o** - 言語モデル
- **BeautifulSoup4** - Webスクレイピング

### インフラストラクチャ
- **Vercel** - 本番環境
- **Docker** - ローカル開発環境

## 🏗 プロジェクト構造（モノレポ構成）

```
ls-bot/
├── package.json             # ルートpackage.json（ワークスペース管理）
├── tsconfig.json           # 共通TypeScript設定
├── tailwind.config.js      # 共通Tailwind CSS設定
├── postcss.config.js       # 共通PostCSS設定
├── apps/                   # アプリケーション
│   ├── frontend/           # Reactフロントエンドアプリ
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── features/chat/  # チャット機能
│   │   │   └── ...
│   │   └── ...
│   └── backend/            # FastAPI バックエンドAPI
│       ├── requirements.txt
│       ├── rag/           # RAG関連ロジック
│       │   ├── chat.py   # チャットエンドポイント
│       │   └── search.py # 検索エンドポイント
│       ├── models/       # データモデル
│       ├── data_loader/  # データ収集・前処理
│       └── main.py      # FastAPIアプリケーション
├── packages/              # 共有パッケージ
│   └── shared-types/     # API通信用共通型定義
│       ├── package.json
│       ├── src/index.ts
│       └── dist/
└── README.md
```

## 🚀 セットアップ

### 事前準備

1. **必要なツール**
   - Node.js (v18以上)
   - Python (v3.9以上)
   - Docker (ローカル開発用)

2. **環境変数の設定**
   ```bash
   # .envファイルをバックエンドディレクトリに作成
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### モノレポのセットアップ

```bash
# ルートディレクトリで全依存関係をインストール
npm install

# 共有型定義をビルド
npm run build --workspace=@ls-bot/shared-types

# バックエンドのPython依存関係をインストール
npm run install:backend
```

### 開発サーバーの起動

```bash
# フロントエンドのみ起動
npm run dev:frontend

# バックエンドのみ起動
npm run dev:backend

# フロントエンド・バックエンド同時起動
npm run dev:all
```

フロントエンド開発サーバーは `http://localhost:5173` で起動します。

### バックエンド

#### ローカル環境（Docker）

```bash
# バックエンドディレクトリに移動
cd apps/backend

# Dockerコンテナのビルドと起動
docker build -t ls-bot-backend .
docker run -p 8000:8000 ls-bot-backend
```

#### Python環境

```bash
# バックエンドディレクトリに移動
cd apps/backend

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# サーバー起動
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

APIサーバーは `http://localhost:8000` で起動します。

### データベースの準備

```bash
# バックエンドディレクトリで実行
cd apps/backend/data_loader

# スクレイピングの実行
python scrape_idolypride.py

# データの前処理
python preprocess_for_rag.py

# ChromaDBの構築
python build_chromadb.py
```

## 🎯 API仕様

### エンドポイント

#### POST /chat
チャット機能のメインエンドポイント

**リクエスト:**
```json
{
  "category": "キャラクター",
  "message": "小美山愛について教えて"
}
```

**レスポンス:**
```json
{
  "reply": "小美山愛さんは..."
}
```

#### POST /search
情報検索エンドポイント

**リクエスト:**
```json
{
  "query": "小美山愛",
  "n_results": 5
}
```

**レスポンス:**
```json
{
  "results": [
    {
      "id": "doc_id",
      "text": "検索結果のテキスト",
      "score": 0.85,
      "url": "https://idolypride.jp/character/ai-komiyama"
    }
  ]
}
```

## 🎨 UI/UXデザイン

### デザインガイドライン
- **メインカラー**: #1428FF（青色）
- **デザインテイスト**: フラットデザイン、四角形ベース
- **チャットボタン**: 右下固定、背景色#1428FF、白アイコン
- **メッセージ表示**: 左側（Bot）・右側（ユーザー）の吹き出し形式

### レスポンシブ対応
- モバイル・タブレット・デスクトップに対応
- チャットウィンドウのサイズ調整

## 🔍 データ収集仕様

### スクレイピング対象
IDOLY PRIDE公式サイトの以下ページからデータを収集：

- `/character/kana` - カナ
- `/character/ai-komiyama` - 小美山愛  
- `/character/aoi-igawa` - 井川葵
- `/character/chisa-shiraishi` - 白石千紗
- `/character/haruko-saeki` - 佐伯遙子

### データ処理ルール
- `<article>`タグ内のテキストを抽出
- `aria-label`、`alt`、`title`属性も対象
- `<nav>`タグは除外
- 改行を句読点まで連結
- 画像・動画は対象外

## 🤖 RAG（検索拡張生成）

### 検索戦略
1. **キーワード検索**: 完全一致・部分一致による高速検索
2. **ベクトル検索**: OpenAI embeddings + ChromaDBによるセマンティック検索
3. **表記揺れ対応**: キャラクター名のエイリアス辞書による正規化

### キャラクター名表記揺れ対応例
- **小美山愛**
  - ひらがな: こみやまあい
  - ローマ字: KOMIYAMA AI、AI KOMIYAMA
  - 誤字: 小宮山愛

## 📊 開発・運用

### スクリプト

**モノレポ全体:**
```bash
npm run dev              # フロントエンド開発サーバー起動
npm run dev:frontend     # フロントエンドのみ起動
npm run dev:backend      # バックエンドのみ起動
npm run dev:all          # フロントエンド・バックエンド同時起動
npm run build            # フロントエンドビルド
npm run lint             # フロントエンドリント実行
npm run lint:all         # 全パッケージでリント実行
npm run type-check       # 全パッケージで型チェック実行
npm run clean            # 全パッケージのビルド結果削除
npm run setup            # 初回セットアップ
```

**個別パッケージ:**
```bash
npm run dev --workspace=@ls-bot/frontend        # フロントエンド開発
npm run build --workspace=@ls-bot/shared-types  # 共有型定義ビルド
npm run type-check --workspace=@ls-bot/frontend # 型チェック
```

**バックエンド:**
```bash
# データ更新（apps/backend/data_loaderディレクトリで実行）
python scrape_idolypride.py     # 最新データのスクレイピング
python preprocess_for_rag.py    # データ前処理
python build_chromadb.py        # ベクトルDB再構築

# サーバー起動（apps/backendディレクトリで実行）
uvicorn main:app --reload       # 開発モード
uvicorn main:app --host 0.0.0.0 --port 8000  # 本番モード
```

### ログ・モニタリング
- FastAPIの自動生成ドキュメント: `http://localhost:8000/docs`
- チャット履歴の記録と分析
- API使用量の監視

## 🚢 デプロイ

### Vercel（推奨）
1. GitHubリポジトリと連携
2. 環境変数（OPENAI_API_KEY）の設定
3. 自動デプロイの設定

### Docker
```bash
# 本番用Dockerイメージのビルド
docker build -t ls-bot-backend -f apps/backend/Dockerfile apps/backend/
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ls-bot-backend
```

## 🔧 トラブルシューティング

### よくある問題

1. **OpenAI API エラー**
   - API キーの確認
   - 使用量制限の確認

2. **ChromaDB 接続エラー**
   - データベースファイルの存在確認
   - ファイルパーミッションの確認

3. **CORS エラー**
   - FastAPI CORS設定の確認
   - フロントエンドのAPIベースURL確認
