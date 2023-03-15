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
from utils.YTComment import YTComment


def main():
    if not voicevoxHelthCheck():
        return
    try:
        yt_url = 'https://www.youtube.com/watch?v=OcuwIJrZy3k' # youtubeのURL
        youtubeChat = YTComment(yt_url)
        
        # キャラクターがwavファイルを作成する
        # キャラクターのwavファイルを順番に再生する
        # 立ち絵を動かす
        fifoPlayer = FIFOPlayer()
        fifoPlayer.playWithFIFO()


        LLM = OpenAILLM()
        ruminesAI = CharacterAI(LLM, "ルミネス", contextDB_json,
                               13, 1.2, fifoPlayer, TachieViewer, 'rumines')
        rianAI = CharacterAI(LLM, "リアン", contextDB_json,
                              6, 1.2, fifoPlayer, TachieViewer, 'rian')
        ranAI = CharacterAI(LLM, "ラン", contextDB_json,
                               8, 1.2, fifoPlayer, TachieViewer, 'ran')
        neonAI = CharacterAI(
            LLM, "ネオン", contextDB_json, 7, 1.2, fifoPlayer, TachieViewer, 'neon')

        characterAIs = [ruminesAI, rianAI, ranAI, neonAI]

        conversationTimingChecker = ConversationTimingChecker()
        chatController = ChatController(characterAIs)
        chatController.initContextAll()
        chatController.addContextAll(
            'system', "[場面説明]\nあなたたちはyoutubeの配信者で,今デビュー配信中です。洋楽について雑談してください。")
        
        
        chatController.addContextAll(
            'system', "[場面説明]\nこんにちわ、ルミネスです。今日は洋楽について雑談しましょう。")
        
        

        for i in range(40):
            print("i: ", i)
            try:
                conversationTimingChecker.check_conversation_timing_with_delay(
                    fifoPlayer.get_file_queue_length)
                
                while True:
                    latestChat = youtubeChat.get_comment()
                    print(latestChat)
                    
                    if latestChat is not None:
                        break
                    time.sleep(1)

                # latestChat = youtubeChat.get_comment()
                if latestChat is not None:
                    latestMsg = latestChat["message"]
                    chatController.addComment( 'system', f"{latestMsg}")

                
                chatController.getNextCharacterResponse()



            except openai.error.RateLimitError:
                print("rate limit error")
                time.sleep(5)
            except openai.error.APIError:
                print("API error")
                time.sleep(5)
        print("end")
    
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
