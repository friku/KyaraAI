# KyaraAI
複数のキャラクターAIに会話していただくためのリポジトリです。


# Feature
複数の人格と記憶を持ったキャラクターを作成
複数キャラが会話するためのコントロールシステムを作成
- 他のキャラの発言を記憶
- 発言の順番をコントロール
- systemロールの発言を全員に記憶させる

# setup
python >= 3.6
openai >= 0.27.0

pythonとopenaiが入っていれば動きます。

# quick start
set openai API key
```
export OPENAI_API_KEY=<your openai api key>
git clone git@github.com:friku/KyaraAI.git
cd KyaraAI
python characterAI.py
```

# 会話に参加するキャラクターを選ぶ
https://github.com/friku/KyaraAI/blob/82f167d0a858f5c32e0af02647b7d0cb43e0997a/characterAI.py#L148
この行の上で作成されたキャラクターをcharacterAIsのリストに入れてください。


# 独自の人格を持ったキャラクターAIを作る
キャラクターの人格に関する情報は
characterConfig/<character name>/identity.txt
の中に記述してください。
ここがキャラクターに最初に伝えるプロンプトとなります。

# 発言の形式を調整する。
出力は単純に発言のみを出力させるより、感情パラメータや思考を出力させてから、実際の発言をさせたほうがより良い発言になることがあります。(CoT)
そのため、ほかのキャラクターに伝える前に出力から実際の発言に変換する必要があります。
デフォルトでは下記の形式を前提として、`[<character Name>の発言]`の後のみを出力するように変換しています。
```
[<character Name>の心の声]
xxx

[<character Name>の発言]
xxx
```
この変換方法はプロンプトによって変わるので、変更したい場合は、
https://github.com/friku/KyaraAI/blob/82f167d0a858f5c32e0af02647b7d0cb43e0997a/characterAI.py#L87
を修正してください。


# キャラクターに伝えられるプロンプトの説明
キャラクターが返答する際には、characterConfig/<character name>/context.jsonの中身がプロンプトとして用いられます。
jsonの各要素はchatGPTに渡すmessageです。
一番最初の要素に各キャラクタのidentitiy.txtファイルの中身がmessageとして入っており、それ以降に発言が入ります。
他のキャラや自キャラが発言するたびにこのファイルに追加されます。

# 最大トークン数を超えないための対処
LLMに入力可能なトークン数が決まっており、openaiのchatGPTの場合4096が最大入力トークン数です。
chatGPTの場合、最大入力トークン数を超えた入力をするとエラーが返ってきます。


# Future work
- [x] トークン数が4096を超えないようにする。
- [ ] 長期記憶を持つ



