import requests
import json
import pytest
from pathlib import Path
# from playsound import playsound
import time
import pyaudio # wavファイルを再生する




def send_audio_query(speaker: int, text: str) -> requests.Response:
    """
    指定されたspeakerとtextを使用して、audio_queryのRESTリクエストを送信します。

    Parameters
    ----------
    speaker : int
        発話者のIDを表す整数値。
    text : str
        発話内容を表す文字列。

    Returns
    -------
    response : requests.Response
        POSTリクエストのレスポンスを表すrequests.Responseオブジェクト。
    """
    # リクエストヘッダーの情報を定義
    url = 'http://localhost:50021/audio_query'
    headers = {'Content-Type': 'application/json'}

    # リクエストパラメータの情報を定義
    params = {
        'text': text,
        'speaker': speaker

    }

    # POSTリクエストを送信
    response = requests.post(url, headers=headers, params=params)

    # レスポンスを返す
    return response

# pytestのテスト関数を定義する


def test_send_audio_query():
    # speaker=1, text='こんにちわ'でリクエストを送信して、レスポンスのステータスコードを確認する
    response = send_audio_query(1, 'こんにちわ')
    print(response.text)
    assert response.status_code == 200

    # speaker=2, text='Good morning'でリクエストを送信して、レスポンスのステータスコードを確認する
    response = send_audio_query(2, 'Good morning')
    assert response.status_code == 200


def synthesis(speaker: int, audio_query: dict) -> requests.Response:
    """
    指定されたspeakerとaudio_queryを使用して、synthesisのRESTリクエストを送信します。

    Parameters
    ----------
    speaker : int
        発話者のIDを表す整数値。
    audio_query : dict
        音声合成に必要な情報を格納した辞書。

    Returns
    -------
    response : requests.Response
        POSTリクエストのレスポンスを表すrequests.Responseオブジェクト。
    """
    # リクエストヘッダーの情報を定義
    url = 'http://localhost:50021/synthesis'
    headers = {'Content-Type': 'application/json'}

    # リクエストパラメータの情報を定義
    params = {
        'speaker': speaker
    }

    # POSTリクエストを送信
    response = requests.post(url, headers=headers,
                             params=params, data=json.dumps(audio_query))

    # レスポンスを返す
    return response


def synthesis2waveFile(synthesisRes: requests.Response, saveFilePath: Path) -> None:
    with open(saveFilePath, mode='wb') as f:
        f.write(synthesisRes.content)


def makeWaveFile(speaker: int, text: str, saveFilePath: Path) -> None:
    query = send_audio_query(speaker, text)
    synthesisRes = synthesis(speaker, query.json())
    synthesis2waveFile(synthesisRes, saveFilePath)
    
    
def text2stream(speaker: int, text: str) -> None:

    query = send_audio_query(speaker, text)

    synthesisRes = synthesis(speaker, query.json())

    p = pyaudio.PyAudio()
    # ストリームを開く
    stream = p.open(format=pyaudio.paInt16,  # 16ビット整数で表されるWAVデータ
                    channels=1,  # モノラル
                    rate=24000,  # サンプリングレート
                    output=True)
    # 再生を少し遅らせる（開始時ノイズが入るため）
    time.sleep(0.2) # 0.2秒遅らせる
    # WAV データを直接再生する
    stream.write(synthesisRes.content)  

    # ストリームを閉じる
    stream.stop_stream()
    stream.close()

    # PyAudio のインスタンスを終了する
    p.terminate()


def main():
    text2stream(1, 'こんにちわ,わたしはずんだもんなのだ。よろしくなのだ')



if __name__ == '__main__':
    main()
