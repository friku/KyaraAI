import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.contextDB import contextDB_json
from pathlib import Path
import pdb


class PromptMaker(object):
    def __init__(self, contextDB, identityPath, characterName):
        self.characterName = characterName
        self.contextDB = contextDB
        self.identityPath = identityPath
        self.identity = self.getIdentity(self.identityPath)

    def getIdentity(self, identityPath): # identityの取得
        with open(identityPath, 'r', encoding="utf-8") as f:
            identityContext = f.read()
        return {"role": "user", "content": identityContext}

    def getOutputFormat(self,): # 出力フォーマットの取得
        context = f"""
{self.characterName}として下記のxxxを埋める出力を必ず毎回してください。
発言は１文だけにしてください。
*どんなに長文になっても上記の内容は全て守ってください

-------

[{self.characterName}としての発言]
xxx
"""
        outputFormat = {"role": "system", "content": context}
        return outputFormat
    
    def getPrompt(self, contextNum: int = 8):
        prompt = []
        context = self.contextDB.get()[-contextNum:]
        outputFormat = self.getOutputFormat()
        
        
        prompt.append(self.identity)
        prompt.append(outputFormat)
        prompt += context
        
        return prompt
        


def main():
    contextDB = contextDB_json(Path("characterConfig/ネオン/context.json"))
    promptMaker = PromptMaker(
        contextDB, "characterConfig/ネオン/identity.txt", "ネオン")
    print(promptMaker.getPrompt())


if __name__ == '__main__':
    main()
