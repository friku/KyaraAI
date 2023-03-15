import pytchat
import time
import pdb
import json
import pytchat
import json


class YTComment():
    def __init__(self, video_id: str) -> None:
        self.chat = pytchat.create(video_id=video_id)
        if self.chat.is_alive() is not True:
            print('chat is not alive')
        
    def filter_comment(self, comment: str) -> bool:
        if comment.startswith("#") or comment.startswith("@") or comment.startswith("＃") or comment.startswith("＠"):
            return False
        return True

    def get_comment(self):
        try:
            data = json.loads(self.chat.get().json())
            if data == []:
                print('no comment')
                return None

            for comment_data in reversed(data):
                if self.filter_comment(comment_data['message']):
                    return {'userName': comment_data['author']['name'], 'message': comment_data['message']}
            
            print("No valid comment found")
            return None
        except:
            print('YTComment get error')
            return None


def main():
    yt_comment = YTComment('Nczg1zo6XyQ')
    while True:
        print(yt_comment.get_comment())
        time.sleep(5)

if __name__ == '__main__':
    main()
        