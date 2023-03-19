import json
from characterAI import contextDB_json
from pathlib import Path


def test_contextDB_json():
    test_json_path = Path('context_test.json')
    with open(test_json_path, 'w') as f:
        json.dump([], f)
    contextDB = contextDB_json(test_json_path)
    data = contextDB.get()
    assert data == [], "contextDB_jsonの初期化が正しく行われていません。"
    contextDB.add("user", "これはテストです。")
    data = contextDB.get()
    assert data == [{"role": "user", "content": "これはテストです。"}
                    ], "contextDB_jsonのaddが正しく行われていません。"