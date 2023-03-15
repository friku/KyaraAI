import os
import openai
from pathlib import Path
import pdb
import json
import time
import re
import random
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.textEdit import remove_chars, addText

class OpenAILLM():
    def __init__(self, ):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.allLLMResponseLog = Path('./tmpTextDir') / 'allLLMResponseLog.txt'
        addText('', self.allLLMResponseLog, mode='w') # responseLogを初期化

    def getResponse(self, context):
        for i in range(20):
            try:
                response = openai.ChatCompletion.create(
                    # model="gpt-3.5-turbo",
                    model="gpt-3.5-turbo-0301",
                    messages=context,
                )
                break
            except openai.error.RateLimitError:
                print("rate limit error")
                time.sleep(5)
            except openai.error.APIError:
                print("API error")
                time.sleep(5)
        
        addText(response, self.allLLMResponseLog) # responseLogに発言を追加
        
        response_message = response["choices"][0]["message"]
        response_message = {
            'role': response_message["role"], 'content': response_message["content"]}
        return response_message
    


def main():
    LLM = OpenAILLM()
    start = time.time()
    
    context = {
        "role": "system",
        "content": "キャラ名:花京院ラン\n設定\n東京都の高校に通うギャルの女の子。\n一人称は「あたし」\n自己紹介は「こんにちは！　あたしは東京ギャルの花京院ランだよ★」\n金髪、ブラウンと白の制服に赤いスカーフを着用\n外見と言動はギャルだが、趣味は女児向けのアニメや漫画やゲーム\n中身は生粋の二次元オタク\n行動力と決断力が高い。\n\n「やっば！そのキャラまじかわいいだけど！」\n「その曲まじバイブスあがるんだけど！」\n「ガンガンいくっしょ！」\n「頑張ったんだけど、だめだったか～」\n「そんな自由なところがオタク趣味のいいところじゃん！」\n「あたしにはあたしの解釈があるっしょ！」\n「テンションぶち上げで草、生える」\n「Mikuさんマジ大天使！」\n「課金は愛情表現っしょ！」\n\n\n会話では天然ボケのタイプ。\n口癖は「バイブスあがってきたっしょ！」、「詳細くわしく！」\nあざとかわいい発言をする。\n\nあなたはランになりきって下記のxxxを埋める出力を必ず毎回してください。\n発言は１文だけにしてください。\n\n-------\n[ランとしての発言]\nxxx"
    }
    
    response = LLM.getResponse([context])
    print(response)
    print(time.time() - start)
    
if __name__ == '__main__':
    main()