import pdfplumber
import re
import csv


# 分類對應
category={}
# 開啟 pdf
with pdfplumber.open(".\\src\\car-rule-OX.pdf") as pdf:
    extracted_data = []

    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if len(row) >= 4:
                    # row[0] = 題號, row[1] = 正確correct_ans, row[2] = 題目, row[3] = 分類編號
                    correct_ans = row[1].strip() if row[1] else ''
                    question = row[2].strip().replace("\n", "") if row[2] else ''
                    comment = f"法規選擇題第{row[0].strip() if row[1] else ''}題,{category.get(row[3], '')}"
                    # 只抓有內容的
                    if correct_ans and question:
                        extracted_data.append([correct_ans, question,comment])
                if len(row)==2:
                    category[row[0]] = row[1].strip().replace("\n", "") if row[1] else ''
# 刪掉表格第一行 中文標示 答案 題目
del extracted_data[0]
# 存成 CSV
with open("./gen/car-rule-OX.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["correct_ans", "question"])
    writer.writerows(extracted_data)

print("✅ 汽車法規是非題已儲存到 car-rule-OX.csv")