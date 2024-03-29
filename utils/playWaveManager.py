import glob
import os
import pdb
import time

import pydub
from pydub.playback import play

if __name__ == "__main__":
    from fire_and_forget import fire_and_forget
else:
    from utils.fire_and_forget import fire_and_forget


class WavQueuePlayer:
    def __init__(self, directory: str = "./tmpWaveDir"):
        """
        指定されたディレクトリ内のWAVファイルを再生するWavQueuePlayerオブジェクトを初期化します。

        Args:
            directory (str): WAVファイルが格納されたディレクトリのパス
        """
        self.directory = directory
        self.file_queue = []
        self._clear_directory()

    def get_file_queue_length(self):
        """
        キュー内のファイルの数を返します。

        Returns:
            int: キュー内のファイルの数
        """
        return len(self.file_queue)

    @fire_and_forget
    def play(self, resident: bool = True, pause: float = 0.4):
        """
        ファイルキュー内の全てのWAVファイルを再生します。

        Args:
            pause (float, optional): 各ファイルの再生後に、一時停止する秒数。デフォルトは0.4秒。
        """
        self.resident = resident
        while self.resident:
            self.update_file_queue()
            if len(self.file_queue) > 0:
                file_path = self.file_queue.pop(0)
                sound = pydub.AudioSegment.from_wav(file_path)
                play(sound)
                os.remove(file_path)
                time.sleep(pause)
            else:
                time.sleep(1)

    def update_file_queue(self):
        """
        ファイルキューを更新し、再生待ちのWAVファイルのリストを作成します。
        """
        self.file_queue = [
            os.path.join(self.directory, f)
            for f in os.listdir(self.directory)
            if f.endswith(".wav")
        ]
        self.file_queue.sort()

    def _clear_directory(self):
        """ディレクトリ内のすべての WAV ファイルを削除する"""
        for file_path in glob.glob(os.path.join(self.directory, "*.wav")):
            os.remove(file_path)

    def stop(self):
        self.resident = False


if __name__ == "__main__":
    # Example usage:
    player = WavQueuePlayer("./tmpWaveDir")

    # Play all WAV files in the queue
    player.play()
