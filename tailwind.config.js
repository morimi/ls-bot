/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // フロントエンドアプリケーション
    './apps/frontend/src/**/*.{js,jsx,ts,tsx}',
    // 共有UIコンポーネント（将来的に追加予定）
    './packages/ui-components/src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      // LS-BOTブランドカラー
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#1428ff', // メインカラー
          600: '#1018cc',
          700: '#0c1299',
        },
      },
    },
  },
  plugins: [],
}; 