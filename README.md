# 横スクロールシューティングゲーム（pygame 製）

## 概要

本リポジトリは、Python のゲームライブラリ「pygame」を用いて開発された、横スクロール型のシューティングゲームです。プレイヤーは自機を操作し、敵やボスを倒しながらスコアを稼ぎ、ゲームクリアを目指します。

## ゲーム内容

-   **ジャンル**: 横スクロールシューティング
-   **操作方法**: キーボードで自機を上下左右に移動し、スペースキーで弾を発射します。
-   **難易度選択**: ゲーム開始時に「Easy」「Normal」「Hard」から難易度を選択できます。
-   **敵とボス**: 一定スコアに到達すると多彩な攻撃パターンを持つボスが出現します。
-   **パワーアップ**: ゲーム中に出現するアイテムを取得すると、以下のような一時的な強化効果を得られます。
    -   マルチショット（弾が複数発射される）
    -   斜めショット（斜め方向にも弾を発射）
    -   スピードアップ（移動速度上昇）
    -   シールド（一定時間無敵）
-   **ゲームクリア・ゲームオーバー**: ボスを倒すとゲームクリア、HP が 0 になるとゲームオーバーです。
-   **サウンド**: BGM や効果音も実装されています。
