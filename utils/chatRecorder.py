
from pathlib import Path
import json
import os


class DictRecorder():
    def __init__(self, filename: Path):
        self.filename = filename
        print(self.filename.exists())
        if not self.filename.exists():
            print(f'init: {filename}')
            self.init()
        # jsonファイルの中身が空の場合、初期化する
        if os.stat(filename).st_size == 0:
            print(f'file is empty. {filename}')
            self.init()
        self.init()
        

    def add(self, dictRecord: dict) -> None:
        with open(self.filename, 'r', encoding="utf-8") as f:
            data = json.load(f)

        with open(self.filename, 'w', encoding="utf-8") as f:
            data.append(dictRecord)
            json.dump(data, f, ensure_ascii=False)

    def get(self) -> list:
        with open(self.filename, 'r', encoding='utf-8_sig') as f:
            data = json.load(f)
            return data
    
    def get_last(self) -> dict:
        return self.get()[-1]

    def init(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump([], f)
        