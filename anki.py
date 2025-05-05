import genanki
import csv
import random
import os
import re

def create_anki_CSV(csv_path, output_apkg_name):
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'Comment'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><i>{{Comment}}</i>',
            },
        ])

    deck = genanki.Deck(
        deck_id,
        os.path.splitext(output_apkg_name)[0]
    )
    # 創建 output 資料夾
    output_folder = '.\\apkgs'
    os.makedirs(output_folder, exist_ok=True)  # 如果資料夾不存在，則創建它

    output_path = os.path.join(output_folder, output_apkg_name)  # 合併路徑

    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=2):  # idx從2開始，因為第1行是表頭
            try:
                question = re.sub(r'(\(\d+\))', r'<br>\1', row.get('question', '').strip())#遇到選擇題選項換行
                correct_ans = row.get('correct_ans', '').strip()
                comment = row.get('comment', '').strip()
            except ImportError:
                print("error data in line",idx)
                continue
            fields = [question, correct_ans, comment]
            # continue

            note = genanki.Note(
                model=model,
                fields=fields
            )
            deck.add_note(note)
    genanki.Package(deck).write_to_file(output_path)
    print(f"✅{output_path} 成功匯出")
def create_anki_CSV_IMG(csv_path, output_apkg_name):
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    # 定義 Anki 的模型（題目 + 答案 + 備註）
    model = genanki.Model(
        model_id,
        'car sign OX question',
        fields=[
            {'name': 'Question'},
            {'name': 'Image'},
            {'name': 'Answer'},
            {'name': 'Comment'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<br><br>{{Image}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><br><i>{{Comment}}</i>'
            },
        ])

    deck = genanki.Deck(
        deck_id,
        os.path.splitext(output_apkg_name)[0]
    )
    # 創建 output 資料夾
    output_folder = './apkgs'
    os.makedirs(output_folder, exist_ok=True)  # 如果資料夾不存在，則創建它

    output_path = os.path.join(output_folder, output_apkg_name)  # 合併路徑

    media_files = []  # 用來存放圖片檔案

    # 讀取 CSV，加入卡片
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=2):  # idx從2開始，因為第1行是表頭
            try:
                question = row.get('question', '').strip()
                correct_ans = row.get('correct_ans', '').strip()
                comment = row.get('comment', '').strip()
                image_file = row.get('image_path', '').strip()  # CSV 中有一欄叫 "image_path"
                card_fill_img = ''
                # 將圖片檔案加到 media_files 列表中
                if image_file and os.path.exists(image_file):
                    media_files.append(os.path.abspath(image_file))
                    card_fill_img = f'<img src="{os.path.basename(image_file)}"/>'
            except Exception as e:
                print(f"⚠️ 第 {idx} 行資料錯誤: {e}")
                continue
            fields = [question, card_fill_img,correct_ans, comment] # 加入圖片欄位
            note = genanki.Note(
                model=model,
                fields=fields
            )
            deck.add_note(note)
    my_package = genanki.Package(deck)
    my_package.media_files =media_files
    my_package.write_to_file(output_path)
    print(f"✅ 成功匯出 {output_path}")