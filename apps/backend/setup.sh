#!/bin/bash
set -e

# 仮想環境作成
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# 依存インストール
pip install --upgrade pip
pip install -r requirements.txt

# dataディレクトリ作成
mkdir -p data

# スクレイピング
python data_loader/scrape_idolypride.py

# 前処理
python data_loader/preprocess_for_rag.py

# ベクトルDB構築
python data_loader/build_chromadb.py

 