import genanki
import csv
import random
import os
import re

def create_anki_from_csv(csv_path, output_apkg_name):
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
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><small>{{Comment}}</small>',
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