import time

class ConversationTimingChecker:
    def __init__(self, threshold: int = 1):
        self.threshold = threshold

    def check_conversation_timing(self, num_conversations: int) -> bool:
        if num_conversations >= self.threshold:
            return False
        else:
            return True

    def check_conversation_timing_with_delay(self, get_num_conversations) -> bool:
        while True:
            i = 0
            num_conversations = get_num_conversations()
            if self.check_conversation_timing(num_conversations):
                return
            else:
                if i % 10 == 0:
                    print(f'発話待ち:{num_conversations}ファイル')
                time.sleep(1)  
                i = i + 1
                
                