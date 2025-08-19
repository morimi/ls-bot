/**
 * LS-BOT共有型定義
 * フロントエンドとバックエンド間でのAPI通信で使用される型を定義
 */

// ===== チャット関連の型定義 =====

/**
 * チャットカテゴリの列挙型
 */
export type ChatCategory = 
  | 'キャラクター'
  | 'ライブイベント'
  | 'グッズ'
  | '楽曲'
  | '生放送'
  | 'その他';

/**
 * チャットリクエストの型定義
 */
export interface ChatRequest {
  /** ユーザーからのメッセージ */
  message: string;
  /** チャットのカテゴリ */
  category: ChatCategory;
  /** セッションID（オプション） */
  sessionId?: string;
}

/**
 * チャットレスポンスの型定義
 */
export interface ChatResponse {
  /** ボットからの返答 */
  reply: string;
  /** セッションID */
  sessionId?: string;
  /** レスポンス生成時刻 */
  timestamp?: string;
}

// ===== 検索関連の型定義 =====

/**
 * 検索リクエストの型定義
 */
export interface SearchRequest {
  /** 検索クエリ */
  query: string;
  /** 取得する結果数（デフォルト: 5） */
  n_results?: number;
  /** 検索対象カテゴリ（オプション） */
  category?: ChatCategory;
}

/**
 * 検索結果アイテムの型定義
 */
export interface SearchResultItem {
  /** ドキュメントID */
  id: string;
  /** 検索結果のテキスト */
  text: string;
  /** 関連度スコア */
  score: number;
  /** 元のURL（オプション） */
  url?: string;
  /** メタデータ（オプション） */
  metadata?: Record<string, any>;
}

/**
 * 検索レスポンスの型定義
 */
export interface SearchResponse {
  /** 検索結果の配列 */
  results: SearchResultItem[];
  /** 検索にかかった時間（ミリ秒） */
  searchTime?: number;
  /** 総件数 */
  totalCount?: number;
}

// ===== エラーハンドリング関連の型定義 =====

/**
 * APIエラーレスポンスの型定義
 */
export interface ApiError {
  /** エラーメッセージ */
  message: string;
  /** エラーコード */
  code?: string;
  /** 詳細情報 */
  details?: any;
  /** エラー発生時刻 */
  timestamp?: string;
}

/**
 * API標準レスポンス型（成功時）
 */
export interface ApiSuccessResponse<T = any> {
  /** 成功フラグ */
  success: true;
  /** レスポンスデータ */
  data: T;
  /** メッセージ（オプション） */
  message?: string;
}

/**
 * API標準レスポンス型（エラー時）
 */
export interface ApiErrorResponse {
  /** 成功フラグ */
  success: false;
  /** エラー情報 */
  error: ApiError;
}

/**
 * API統合レスポンス型
 */
export type ApiResponse<T = any> = ApiSuccessResponse<T> | ApiErrorResponse;

// ===== ユーティリティ型 =====

/**
 * 部分的にオプションにする型
 */
export type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

/**
 * 必須項目を指定する型
 */
export type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;
