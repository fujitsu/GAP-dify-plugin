## 概要

本プラグインは、Dify 上で Generative AI Platform（GAP）API を利用可能にするためのプラグインです。
GAP API と Dify を統合することで、Dify のワークフロー内から GAP の LLM との会話機能を活用できます。

## プラグインの種類

本リポジトリでは以下の 2 種類のプラグインを提供しています：

| プラグイン種類       | 説明                                          | 利用可能な GAP API                         |
| -------------------- | --------------------------------------------- | ------------------------------------------ |
| **Model プラグイン** | GAP の LLM との会話を Dify のモデルとして利用 | Add Chat Messages, Create Next Ai Message  |
| **Tool プラグイン**  | GAP のルーム操作を Dify のツールとして利用    | Add Chat, Delete Chat, Remove Last Message |

## 動作環境

### 確認済み環境

- **Dify**: コミュニティ版
- **OS**: Linux(WSL で動作確認を実施しています)
- **Python**: 3.11 以上（認証ヘルパースクリプト実行用）
