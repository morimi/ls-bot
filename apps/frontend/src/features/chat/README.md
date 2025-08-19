# Chat Feature

## 概要

このディレクトリは、画面右下に常駐するチャットボタンおよびチャットウィンドウ機能を提供します。

- チャットボタン（`ChatButton`）は右下に常駐し、クリックでチャットウィンドウを開閉します。
- チャットウィンドウ（`ChatPopup`）はポップアップで開き、チャットログとメッセージ入力エリアを持ちます。
- メッセージは左（Bot）・右（ユーザー）に吹き出しで表示されます。
- 送信ボタンや主要なUIカラーは公式カラー（#1428FF）を使用しています。

## ディレクトリ構成

- `components/` ... UIコンポーネント（ボタン・ポップアップ）
- `ChatWidget.container.tsx` ... ロジック・状態管理

## 使い方

`App.tsx` で `ChatWidgetContainer` をレンダリングしてください。

```
import ChatWidgetContainer from './features/chat/ChatWidget.container';

function App() {
  return <ChatWidgetContainer />;
} 