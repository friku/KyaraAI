import glob
import re

def extract_english(text):
    # 英語の正規表現パターンを定義する
    pattern = r'[a-zA-Z]+'
    # 正規表現パターンにマッチする英語の単語を抽出する
    english_words = re.findall(pattern, text)
    return english_words


unique_words = set()

alphabetWords = []

# chatLogディレクトリ内のtxtファイルをすべて取得して、各ファイルに対して処理を実行する
for file_path in glob.glob('./chatLogs/*.txt'):
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        # ファイルから文字列を読み込んで、アルファベットで書かれた単語を抽出する
        # 文章が長い場合はストップワード除外や正規表現等の前処理を追加することが望ましい
        text = file.read()
        words = extract_english(text)
        
        alphabetWords += words
        
     
        

# 既に出現した単語を重複してカウントしないように、ユニークな単語だけを集める
unique_words = unique_words.union(alphabetWords)
unique_words = sorted(unique_words)
# 結果を表示する
print(unique_words)
print(len(unique_words))
