import os
import openai
from pathlib import Path
import json
import time
import re
import random
from utils.voicevoxUtils import text2stream, makeWaveFile, voicevoxHelthCheck
from utils.playWaveManager import WavQueuePlayer
from utils.textEdit import remove_chars
from utils.conversationRule import ConversationTimingChecker
from characterAI import OpenAILLM, contextDB_json, CharacterAI, ChatController
from utils.wavePlayerWithVolume import WavPlayerWithVolume
from utils.tachieViewer import TachieViewer
from utils.FIFOPlayer import FIFOPlayer


def main():
    if not voicevoxHelthCheck():
        return
    try:
        # キャラクターがwavファイルを作成する
        # キャラクターのwavファイルを順番に再生する
        # 立ち絵を動かす
        fifoPlayer = FIFOPlayer()
        fifoPlayer.playWithFIFO()

        # imagesDirPath = Path('characterConfig/test/images')
        # tachieViewer = TachieViewer(imagesDirPath)
        # tachieViewer.play()

        LLM = OpenAILLM()
        ryuseiAI = CharacterAI(LLM, "龍星", contextDB_json,
                               13, 1.2, fifoPlayer, TachieViewer, 'ryusei')
        metanAI = CharacterAI(LLM, "めたん", contextDB_json,
                              6, 1.2, fifoPlayer, TachieViewer, 'metan')
        tumugiAI = CharacterAI(LLM, "つむぎ", contextDB_json,
                               8, 1.2, fifoPlayer, TachieViewer, 'tumugi')
        zundamonAI = CharacterAI(
            LLM, "ずんだもん", contextDB_json, 7, 1.2, fifoPlayer, TachieViewer, 'zundamon')

        characterAIs = [ryuseiAI, metanAI, tumugiAI, zundamonAI]

        conversationTimingChecker = ConversationTimingChecker()
        chatController = ChatController(characterAIs)
        chatController.initContextAll()
        chatController.addContextAll(
            'system', "[プロデューサーとしての発言]\nあなたたちはラジオ出演者です。好きなボカロ曲に関してトークしてください。")

        for i in range(100):
            try:
                conversationTimingChecker.check_conversation_timing_with_delay(
                    fifoPlayer.get_file_queue_length)
                chatController.getNextCharacterResponse()
                # time.sleep(10)

                if i % 8 == 0:
                    # chatController.addContextAll(
                    #     'system', "[プロデューサーとしての発言]\n別の話題を提案して、話してください。")
                    chatController.addContextAll(
                        'system', "[プロデューサーとしての発言]\nさらにボカロ曲関連の話の深堀をして、話してください。")
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
        pass


if __name__ == '__main__':
    main()
