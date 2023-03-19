import time
import requests
import json
import os
from pathlib import Path


# 事前に取得したYouTube API key
YT_API_KEY = os.environ['YT_API_KEY']


def get_chat_id(yt_url):
    '''
    https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
    '''
    video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
    print('video_id : ', video_id)

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': YT_API_KEY, 'id': video_id,
              'part': 'liveStreamingDetails'}
    data = requests.get(url, params=params).json()

    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        print('get_chat_id done!')
    else:
        chat_id = None
        print('NOT live')

    return chat_id


def get_chat(chat_id, pageToken, log_file):
    '''
    https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
    '''
    url = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': YT_API_KEY, 'liveChatId': chat_id,
              'part': 'id,snippet,authorDetails'}
    if type(pageToken) == str:
        params['pageToken'] = pageToken

    data = requests.get(url, params=params).json()

    chat_data = []
    try:
        for item in data['items']:
            channelId = item['snippet']['authorChannelId']
            msg = item['snippet']['displayMessage']
            usr = item['authorDetails']['displayName']

            log_text = '[by {}  https://www.youtube.com/channel/{}]\n  {}'.format(
                usr, channelId, msg)
            chat_dict = {'usr': usr, 'msg': msg, 'time':item['snippet']['publishedAt']}
            chat_data.append(chat_dict)

        if data['nextPageToken'] == None:
            return None
        else :
            last_time = data['items'][-1]['snippet']['publishedAt']
        
        print('nextPageToken : ', data['nextPageToken'])

    except:
        
        print('error')
        print('data : ', data)
        return None

    return {'nextPageToken': data['nextPageToken'], 'chat_data': chat_data, 'last_time': last_time}


class YoutubeChat:
    def __init__(self, yt_url):
        self.yt_url = yt_url
        self.nextPageToken = None
        self.chat_id = get_chat_id(yt_url)
        self.log_file = Path("youtube_chat_log.txt")
        self.last_time = '2000-01-01T01:00:00.000000+00:00'  # とりあえず適当な値を入れておく

    def getChat(self):
        response = get_chat(self.chat_id, self.nextPageToken, self.log_file)
        if response is None:
            print('no chat')
            return None
        latest_chat = self.filter_for_NewChat( response['chat_data'])
        self.nextPageToken = response['nextPageToken']
        self.last_time = response['last_time']
        print("self.last_time",self.last_time)
        
        return latest_chat
    
    def filter_for_NewChat(self, chat_data):
        # 最新のチャットを取得する
        new_chat = []
        for chat in chat_data:
            if chat['time'] > self.last_time:
                new_chat.append(chat)
            # print(chat['time'],self.last_time)
        return new_chat
    
    def getSelectedChat(self):
        chat_data = self.getChat()
        if chat_data is None:
            return None
        
        # 適切なチャットを取得する
        selected_chat = chat_data[0]
        
        for chat in chat_data:
            if len(chat['msg']) > len(selected_chat['msg']):
                selected_chat = chat
        return selected_chat
        
        
        
        


def main(yt_url):
    chat = YoutubeChat(yt_url)
    while True:
        print(chat.getSelectedChat())
        time.sleep(10)


# def main(yt_url):
#     slp_time        = 10 #sec
#     iter_times      = 90 #回
#     take_time       = slp_time / 60 * iter_times
#     print('{}分後　終了予定'.format(take_time))
#     print('work on {}'.format(yt_url))

#     log_file = yt_url.replace('https://www.youtube.com/watch?v=', '') + '.txt'
#     with open(log_file, 'a') as f:
#         print('{} のチャット欄を記録します。'.format(yt_url), file=f)
#     chat_id  = get_chat_id(yt_url)

#     nextPageToken = None
#     for ii in range(iter_times):
#         #for jj in [0]:
#         try:
#             print('\n')
#             nextPageToken = get_chat(chat_id, nextPageToken, log_file)
#             time.sleep(slp_time)
#         except:
#             break


if __name__ == '__main__':
    yt_url = input('Input YouTube URL > ')
    main(yt_url)
