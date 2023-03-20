import json
import os
import pdb
from pathlib import Path


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


def main():
    contextDB = contextDB_json(Path("characterConfig/ネオン/context.json"))
    contextDB.add("user", "こんにちは")
    print(contextDB.get())

if __name__ == '__main__':
    main()