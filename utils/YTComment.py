import pytchat
import time
import pdb
import json


class YTComment():
    def __init__(self, video_id:str) -> None:
        self.chat = pytchat.create(video_id=video_id)
        if self.chat.is_alive() is not True:
            print('chat is not alive')
        
    def get_comment(self):
        try:
            data = json.loads(self.chat.get().json())
            if data == []:
                print('no comment')
                return None
            return {'userName':data[-1]['author']['name'],'message':data[-1]['message']}
        except:
            print('YTComment get error')
            return None


def main():
    yt_comment = YTComment('3lfNm7X6wLI')
    while True:
        print(yt_comment.get_comment())
        time.sleep(5)

if __name__ == '__main__':
    main()
        