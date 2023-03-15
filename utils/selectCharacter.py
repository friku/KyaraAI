import pdb
import random

def find_string_positions(text, words, removeWords=[]):
    """テキスト内からlistに入った文字列が存在するか判定し、存在する場合、各文字列ごとに位置を返却する関数。

    Args:
        text (str): 検索対象のテキスト。
        words (list): 検索する文字列を要素とするリスト。

    Returns:
        tuple: 最初に出現した文字列とその位置を持つタプル。

    """
    
    words = remove_matching_strings(words, removeWords)
    
    first_word = None
    first_position = len(text) + 1
    for word in words:
        position = text.find(word)
        if position != -1 and position < first_position:
            first_word = word
            first_position = position
    if first_word is not None:
        return {'first_word': first_word, 'first_position': first_position}
    else:
        return None


def remove_matching_strings(a_list, b_list):
    """
    リストAからリストBに入った文字列と一致するものを除いた新しいリストを返す。
    """
    return [s for s in a_list if s not in b_list]



def select_random_next_character(pre_speaker:str, participants:dict) -> dict:
    """
    次に喋るキャラクターをランダムに選択する。
    """
    # すでに喋ったキャラクターを除外する
    #pre_speakerに一致するキーのparticipantsを削除する
    candidates = remove_matching_strings(list(participants.keys()), [pre_speaker])
    # 候補が残っている場合、ランダムに選択する
    next_speaker_name = random.choice(candidates) if len(candidates) > 0 else pre_speaker
    next_speaker = participants[next_speaker_name]
    next_speaker_dict = {'name':next_speaker_name,'speaker':next_speaker}
    
    return next_speaker_dict
    



def main():
    text = "ねえ、ルミネス。あなたはどうしてネオンを助けたの？"
    words = ["ネオン", "ルミネス", "ラン", "cat"]
    result = find_string_positions(text, words)
    print(result)

if __name__ == '__main__':
    main()
    next_spkeaker = select_random_next_character("ルミネス", {"ルミネス":"ルミネス1", "ネオン":"ネオン1", "ラン":"ラン1", "cat":"cat1"})
    print(next_spkeaker)
