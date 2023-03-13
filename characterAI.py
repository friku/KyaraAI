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
from utils.voicevoxUtils import text2stream, makeWaveFile,voicevoxHelthCheck
from utils.playWaveManager import WavQueuePlayer
from utils.textEdit import remove_chars
from utils.conversationRule import ConversationTimingChecker
from utils.wavePlayerWithVolume import WavPlayerWithVolume
from utils.TextReplacer import replace_words


class OpenAILLM():
    def __init__(self, ):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def getResponce(self, context):
        for i in range(20):
            try:
                responce = openai.ChatCompletion.create(
                    # model="gpt-3.5-turbo",
                    model="gpt-3.5-turbo-0301",
                    messages=context
                )
                break
            except openai.error.RateLimitError:
                print("rate limit error")
                time.sleep(5)
            except openai.error.APIError:
                print("API error")
                time.sleep(5)
        
        
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
        with open(self.filename, 'r', encoding='utf-8_sig') as f:
            data = json.load(f)
            return data

    def init(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump([], f)


class CharacterAI():
    def __init__(self, LLM, characterName: str, contextDBClass: contextDB_json, speakerID: int, speedScale: float = 1.0, fifoPlayer = None, TachieViewer = None, charaNameEN = 'test'):
        self.LLM = LLM
        self.characterName = characterName
        self.charaNameEN = charaNameEN
        self.characterDir = Path('./characterConfig') / characterName
        self.contextPath = self.characterDir / 'context.json'
        self.identityPath = self.characterDir / 'identity.txt'
        if not Path(f'./characterConfig/{characterName}').exists():
            assert False, f'キャラクターの設定ディレクトリが存在しません。{characterName}'
        self.contextDB = contextDBClass(self.contextPath)
        if self.contextDB.get() == []:
            self.addIdentity(self.identityPath)
        self.speakerID = speakerID
        self.speedSclae = speedScale
        self.fifoPlayer = fifoPlayer
        self.TachieViewer = TachieViewer
        self.playTachieViewer()
        self.yt_comment = ''

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
        return {"formatResponse": formatResponse, "talkResponse": talkResponse}

    def getResponse(self):
        prompt = self.makePrompt()
        start = time.time()
        response = self.LLM.getResponce(prompt)
        print(f"getResponce time: {time.time() - start}")
        formatResponse = self.formatResponse(response)["formatResponse"]
        print(formatResponse)
        talkResponse = self.formatResponse(response)["talkResponse"]
        self.text2VoiceObject(talkResponse)
        return formatResponse
    
    def text2VoiceObject(self, text: str):
        cleanedTalkResponse = replace_words(text, 'dictionary.json')
        cleanedTalkResponse = remove_chars(cleanedTalkResponse, "「」 『』・") # 会話の中にある特殊文字を削除
        wavPath =  Path("./tmpWaveDir") / self.getFileName('wav')
        makeWaveFile(self.speakerID, cleanedTalkResponse,wavPath, self.speedSclae) # 音声合成
        self.setVoiceObject(wavPath, text) # 音声合成した音声をキューに追加
    

    def setVoiceObject(self, wavPath:Path, text = None):
        if self.fifoPlayer is None or self.tachieViewer is None:
            return
        self.fifoPlayer.setObject(WavPlayerWithVolume(wavPath, self.tachieViewer.setMouthOpenFlag, text, self.characterName, self.yt_comment))
    
    def addContext(self, role, message):
        self.contextDB.add(role, message)

    def addIdentity(self, identityPath):
        with open(identityPath, 'r', encoding="utf-8") as f:
            identityContext = f.read()
        self.contextDB.add("system", identityContext)

    def makePrompt(self):
        context = self.contextDB.get()
        if len(context) >= 14:
            prompt = context[0:2] + context[-12:]
        else:
            prompt = context
        return prompt

    def text2speach(self, text: str):
        text2stream(self.speakerID, text)
    
    def playTachieViewer(self):
        if self.TachieViewer is None:
            return
        self.tachieViewer = self.TachieViewer(self.characterDir / 'images', self.charaNameEN)
        self.tachieViewer.play()
        
    def getFileName(self, extention: str):
        FileName = time.strftime(
            '%Y%m%d_%H%M%S', time.localtime()) + f'_({self.characterName}).{extention}'
        return FileName
        


class ChatController():
    def __init__(self, characterAIs: list):
        self.characterAIs = characterAIs
        self.speakerID = 0
        self.chatLogsDir = Path('./chatLogs')
        self.makeChatLog()
        self.latest_yt_comment = ''

    def initContextAll(self):
        for characterAI in self.characterAIs:
            characterAI.initContext()

    def addContextAll(self, role, message):  # 発言を全員(自分も含める)の文脈に追加する
        for characterAI in self.characterAIs:
            characterAI.addContext(role, message)
        self.addChatLog(message)
    
    def addComment(self, role, message):
        self.addContextAll(role, f'[コメント欄]\n{message}')
        self.latest_yt_comment = message
        
        

    def getCharacterResponse(self, characterAI):
        characterAI.yt_comment = self.latest_yt_comment
        response = characterAI.getResponse()
        self.addContextAll("user", response)
        characterAI.yt_comment = ''
        return response
    
    def postCharacterChat(self, characterAI, message):
        characterAI.text2VoiceObject(message)
        response = f'[{characterAI.characterName}としての発言]\n{message}'
        self.addContextAll("user", response)


    def selectSpeaker(self):
        pre_speakerID = self.speakerID
        self.speakerID = random.randint(0, len(self.characterAIs)-1)
        if pre_speakerID == self.speakerID:
            self.speakerID = pre_speakerID
            self.selectSpeaker()
        return self.characterAIs[self.speakerID]

    def getNextCharacterResponse(self):  # 次のキャラクターの発言を取得し文脈に追加
        speaker = self.selectSpeaker()
        response = self.getCharacterResponse(speaker)
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
    if not voicevoxHelthCheck(): return
    try:
        audioPlayer = WavQueuePlayer('./tmpWaveDir')
        audioPlayer.play()
        
        LLM = OpenAILLM()
        ryuseiAI = CharacterAI(LLM, "龍星", contextDB_json, 13, 1.2)
        metanAI = CharacterAI(LLM, "めたん", contextDB_json, 6, 1.2)
        tumugiAI = CharacterAI(LLM, "つむぎ", contextDB_json, 8, 1.2)
        zundamonAI = CharacterAI(LLM, "ずんだもん", contextDB_json, 7, 1.2)

        characterAIs = [ryuseiAI, metanAI, tumugiAI, zundamonAI]

        conversationTimingChecker = ConversationTimingChecker()
        chatController = ChatController(characterAIs)
        chatController.initContextAll()
        chatController.addContextAll(
            'system', "[プロデューサーとしての発言]\nあなたたちはラジオ出演者です。好きなアーティストに関してトークしてください。適宜話題は変更してください。")

        
        
        for i in range(100):
            try:
                conversationTimingChecker.check_conversation_timing_with_delay(audioPlayer.get_file_queue_length)
                chatController.getNextCharacterResponse()
                # time.sleep(10)

                if i % 8 == 0:
                    chatController.addContextAll(
                        'system', "[プロデューサーとしての発言]\n別の話題を提案して、話してください。")
                elif i % 4 == 0:
                    chatController.addContextAll(
                        'system', "[プロデューサーとしての発言]\n話の深堀をしてください。")

            except openai.error.RateLimitError:
                print("rate limit error")
                time.sleep(5)
            except openai.error.APIError:
                print("API error")
                time.sleep(5)
                
    except KeyboardInterrupt:
        audioPlayer.stop()

if __name__ == '__main__':
    main()

