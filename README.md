# KyaraAI
誰でも簡単に複数のキャラクターAIの開発、運用、配信をするためのリポジトリです。


# 機能
複数の人格と記憶を持ったキャラクターを作成<br>
複数キャラが会話するためのコントロールシステムを作成
- 他のキャラの発言を記憶
- 発言の順番をコントロール
- systemロールの発言を全員に記憶させる

VOICEVOXによる会話の読み上げ<br>
会話順に沿った音声の再生機能<br>
キャラクターの立ち絵を表示、自動瞬き機能、自動口パク機能<br>
発話の文字数調整機能<br>
OBSとの連携
- Youtubeのコメントを表示
- キャラの発言を表示
- 発言キャラ名を表示


# requirements
Windows11を推奨(動作確認済み)<br>
(Ubuntu22.04で動作検証した場合、立ち絵が表示されないバグを確認)

環境構築
anacondaで仮想環境を作成
```
conda create -n kyara python=3.9 anaconda
conda activate kyara
git clone git@github.com:friku/KyaraAI.git
pip install -r requirements.txt
```

VOICEVOXのインストール<br>
https://voicevox.hiroshiba.jp/<br>
VOICEVOXをインストールし起動してください。(VOICEVOXはGUIを起動すると自動的に、APIサーバーが立ち上がります。KyaraAIではVOICEVOXのAPIを利用しています。)

OPENAIのAPIキーを環境変数に追加する。<br>
https://platform.openai.com/account/api-keys<br>
でAPIキーを作成します。
WINDOWSの場合、「環境変数の設定」で環境変数名を「OPENAI_API_KEY」とし、変数値に作成したAPIキーを登録します。

# quick start
下記のコマンドを実行します。
```
python commandDebugTalk.py
```
キャラクターの立ち絵画面が4枚表示され、各キャラクターのボイスが出力されれば正常に動作しています。

# 会話に参加するキャラクターを選ぶ
https://github.com/friku/KyaraAI/blob/a25e0c822439e1a0972aae98d5873825f85177e1/commentDebugTalk.py#L42
この行のように作成されたキャラクターをcharacterAIsのリストに入れてください。


# 独自の人格を持ったキャラクターAIを作る
キャラクターに関する情報は
characterConfig/<character name>
にあります。このディレクトリにはキャラクターの設定を記述するidentity.txtとキャラクターの立ち絵画像を入れるimagesディレクトリをおいてください。また、コードを実行するとキャラクターの記憶となるcontext.jsonが生成されます。


# プロンプトの設定
プロンプトは
https://github.com/friku/KyaraAI/blob/a25e0c822439e1a0972aae98d5873825f85177e1/utils/PromptMaker.py#L11
で作成されます。<br>
デフォルトではプロンプトは下記の構成となっております。<br>
- キャラ設定
- f"下記はここまでの会話です\n"
- 直前の会話以外の会話履歴(直近の会話を除く)
- キャラの出力フォーマット指定
- f"下記は直前の会話です。\n*{self.characterName}として必ず20字以内で発言すること!\n"
- 直前の会話文



# Future work
- [ ] Talking Head Animeへの対応
- [ ] 長期記憶の実装
- [ ] Koeiromapへの対応

# ライセンス
このコードはMIT licenseで提供されています。ただし、characterConfigディレクトリの中の画像ファイル、テキストファイル、jsonファイルはMIT licenseではありません。ただ、開発やデバッグ用のサンプルデータとして使用することは可能です。


