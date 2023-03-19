import json


def replace_words(text, dictionary_file):
    """
    Replace words in Japanese text according to a dictionary.
    """
    with open(dictionary_file, 'r', encoding="utf-8") as f:
        dictionary = json.load(f)
        for word, replacement in dictionary.items():
            text = text.replace(word, replacement)
        return text


def main():
    dictionary_file = 'dictionary.json'

    text = "そうだな、最近は『Among Us』が人気だな。みんなで宇宙船内で人狼ゲームを楽しむの。ストラテジックな部分もあるし、トリッキーさも必要なんだ。俺も友達とプレイするのが好きだね。あと、『Minecraft』も人気があるね。自分で世界を創り上げるという自由度が高かったり、色々なMODがあるから色んな楽しみ方ができるんだ。どちらも面白いゲームだから、機会があれば試してみることをおすすめするよ。"

    # TextTranslatorクラスを使ってテキストを翻訳する
    translated_text = replace_words(text, dictionary_file)
    print(translated_text)  # 出力例: "I have a 犬 and a 猫. They are both cute."


if __name__ == '__main__':
    main()
