'''
キャラクターAIに必要な機能の抽象を統合したクラス
統合する機能
・キャラクターの設定の読み込み
・コメントからユーザーの特定
・ユーザーごとの過去の会話の読み込み
・

'''
import os
import openai
from pathlib import Path
import json
import time
import re
import random


class OpenAILLM():
    def __init__(self, ):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def getResponce(self, context):
        responce = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context
        )
        responce_message = responce["choices"][0]["message"]
        responce_message = {
            'role': responce_message["role"], 'content': responce_message["content"]}
        return responce_message


class contextDB_json():
    def __init__(self, filename: Path):
        self.filename = filename
        print(self.filename.exists())
        if not self.filename.exists():
            with open(self.filename, 'w', encoding="utf-8") as f:
                print("init contextDB", self.filename)
                json.dump([], f)
        # jsonファイルの中身が空の場合、初期化する
        if os.stat(filename).st_size == 0:
            print(f'file is empty. {filename}')
            with open(self.filename, 'w', encoding="utf-8") as f:
                print("init contextDB", self.filename)
                json.dump([], f)

    def add(self, role, message):
        if message == "":
            return
        with open(self.filename, 'r', encoding="utf-8") as f:
            data = json.load(f)

        with open(self.filename, 'w', encoding="utf-8") as f:
            data.append({"role": role, "content": message})
            json.dump(data, f, ensure_ascii=False)

    def get(self) -> list:
        with open(self.filename) as f:
            data = json.load(f)
            return data

    def init(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump([], f)


class CharacterAI():
    def __init__(self, LLM, characterName: str, contextDBClass: contextDB_json):
        self.LLM = LLM
        self.characterName = characterName
        self.contextPath = Path('./characterConfig') / \
            characterName / 'context.json'
        self.identityPath = Path('./characterConfig') / \
            characterName / 'identity.txt'
        if not Path(f'./characterConfig/{characterName}').exists():
            assert False, f'キャラクターの設定ディレクトリが存在しません。{characterName}'
        self.contextDB = contextDBClass(self.contextPath)
        if self.contextDB.get() == []:
            self.addIdentity(self.identityPath)

    def initContext(self):
        self.contextDB.init()
        self.addIdentity(self.identityPath)

    def formatResponse(self, response):
        try:
            splitResponse = re.split("としての発言]|\n", response["content"])
            talkResponse = splitResponse[-1]
            formatResponse = f'[{self.characterName}としての発言]\n{talkResponse}'
        except:
            import pdb
            pdb.set_trace()
        return {"formatResponse": formatResponse}

    def getResponse(self):
        prompt = self.makePrompt()
        response = self.LLM.getResponce(prompt)
        formatResponse = self.formatResponse(response)["formatResponse"]
        return formatResponse

    def addContext(self, role, message):
        self.contextDB.add(role, message)

    def addIdentity(self, identityPath):
        with open(identityPath, 'r', encoding="utf-8") as f:
            identityContext = f.read()
        self.contextDB.add("system", identityContext)

    def makePrompt(self):
        context = self.contextDB.get()
        if len(context) >= 20:
            prompt = context[0:2] + context[-18:]
        else :
            prompt = context
        return prompt


class ChatController():
    def __init__(self, characterAIs: list):
        self.characterAIs = characterAIs
        self.speakerID = 0
        self.chatLogsDir = Path('./chatLogs')
        self.makeChatLog()

    def initContextAll(self):
        for characterAI in self.characterAIs:
            characterAI.initContext()

    def addContextAll(self, role, message):  # 発言を全員(自分も含める)の文脈に追加する
        for characterAI in self.characterAIs:
            characterAI.addContext(role, message)

    def getCharacterResponse(self, characterAI):
        return characterAI.getResponse()

    def selectSpeaker(self):
        pre_speakerID = self.speakerID
        self.speakerID = random.randint(0, len(self.characterAIs)-1)
        if pre_speakerID == self.speakerID:
            self.speakerID = pre_speakerID
            self.selectSpeaker()
        return self.characterAIs[self.speakerID]

    def getNextCharacterResponse(self):  # 次のキャラクターの発言を取得し文脈に追加
        speaker = self.selectSpeaker()
        response = speaker.getResponse()
        self.addContextAll("user", response)
        print(response)
        self.addChatLog(response)
        return response

    def makeChatLog(self):
        # すべての参加キャラの名前取得し、_でつなげる
        self.attendants = [
            characterAI.characterName for characterAI in self.characterAIs]
        allAttendants = '_'.join(self.attendants)
        self.logFileName = time.strftime(
            '%Y%m%d_%H%M%S', time.localtime()) + f'_({allAttendants}).txt'
        with open(self.chatLogsDir / self.logFileName, 'a', encoding="utf-8") as f:
            f.write(f'{allAttendants}\n')

    def addChatLog(self, response):
        with open(self.chatLogsDir / self.logFileName, 'a', encoding="utf-8") as f:
            f.write(f'{response}\n')


def main():
    LLM = OpenAILLM()
    ryuseiAI = CharacterAI(LLM, "ryusei", contextDB_json)
    metanAI = CharacterAI(LLM, "metan", contextDB_json)
    tumugiAI = CharacterAI(LLM, "tumugi", contextDB_json)
    zundamonAI = CharacterAI(LLM, "zundamon", contextDB_json)

    characterAIs = [ryuseiAI, metanAI, tumugiAI, zundamonAI]

    chatController = ChatController(characterAIs)
    chatController.initContextAll()
    chatController.addContextAll(
        'system', "[プロデューサーとしての発言]\nあなたたちはラジオ出演者です。好きなゲームに関してトークしてください。適宜話題は変更してください。")

    for i in range(100):
        try:
            chatController.getNextCharacterResponse()
            time.sleep(10)
            
            if i % 8 == 0:
                chatController.addContextAll('system', "[プロデューサーとしての発言]\n別の話題を提案して、話してください。")
            elif i % 4 == 0:
                chatController.addContextAll('system', "[プロデューサーとしての発言]\n話の深堀をしてください。")

        except openai.error.RateLimitError:
            print("rate limit error")
            time.sleep(20)


if __name__ == '__main__':
    main()
