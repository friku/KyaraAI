import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.contextDB import contextDB_json
from pathlib import Path
import pdb
from utils.textEdit import addText


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

    def getOutputFormat(self, outputNum:int = 20): # 出力フォーマットの取得
        self.outputNum = outputNum
        context = f"""
{self.characterName}として下記の[YOUR OUTPUT]を埋める出力をしてください。
*発言は必ず{self.outputNum}字以内ですること。

-------

[{self.characterName}としての発言]
[YOUR OUTPUT]
"""
        outputFormat = {"role": "system", "content": context}
        return outputFormat
    

    
    def getPrompt(self, contextNum: int = 22, outputNum: int = 20):
        prompt = []
        context = self.contextDB.get()[-contextNum:]
        outputFormat = self.getOutputFormat(outputNum)
        
        
        prompt.append(self.identity)
        
        prompt.append({"role": "system", "content": f"下記はここまでの会話です。\n"})
        prompt += context[:-1]
        prompt.append(outputFormat)
        prompt.append({"role": "system", "content": f"下記は直前の会話です。\n*{self.characterName}として必ず{self.outputNum}字以内で発言すること!\n"})
        prompt += context[-1:]
        
        addText(prompt, Path("tmpTextDir/tmpprompt.txt"), encoding="utf-8", mode='a')
        addText(f'プロンプトの数{len(prompt)}, 制限文字数:{self.outputNum}字', Path("tmpTextDir/tmpprompt.txt"), encoding="utf-8", mode='a')
        
        return prompt
        


def main():
    contextDB = contextDB_json(Path("characterConfig/ネオン/context.json"))
    promptMaker = PromptMaker(
        contextDB, "characterConfig/ネオン/identity.txt", "ネオン")
    print(promptMaker.getPrompt())


if __name__ == '__main__':
    main()
