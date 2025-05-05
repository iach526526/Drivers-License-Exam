import pdfplumber
import csv
import re
from anki import create_anki_CSV,create_anki_CSV_IMG
def no_img_pdf(filename):
    # 分類對應
    category={}
    # 開啟 pdf
    with pdfplumber.open(f".\\src\\{filename}.pdf") as pdf:
        extracted_data = []

        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if len(row) >= 4:
                        # row[0] = 題號, row[1] = 正確correct_ans, row[2] = 題目, row[3] = 分類編號
                        correct_ans = row[1].strip() if row[1] else ''
                        question = row[2].strip().replace("\n", "") if row[2] else ''
                        comment = f"選擇題第{row[0].strip() if row[1] else ''}題，分類{row[3]}|{category.get(row[3], '')}"
                        # 只抓有內容的題目，不要抓到表頭欄位名，只要第 0 欄是數字就是題目
                        if row[0].isnumeric():
                            extracted_data.append([correct_ans, question,comment])
                    if len(row)==2:#在第一頁拿出分類標籤做成字典，提供
                        category[row[0]] = row[1].strip().replace("\n", "") if row[1] else ''
    # 存成 CSV
    with open(f"./gen/{filename}.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["correct_ans", "question", "comment"])
        writer.writerows(extracted_data)

    print(f"✅ 汽車法規題目 {filename}.pdf 已儲轉換到 {filename}.csv")
    return f"./gen/{filename}.csv"
def pdf_with_images(filename):
    # 分類對應
    category = {}
    
    extracted_data = []
    # 開啟 pdf
    with pdfplumber.open(f".\\src\\{filename}.pdf") as pdf:
        # 第一頁:分類頁，沒有題目，只有分類定義，拿出來放字典
        first_page = pdf.pages[0].extract_tables()
        for table in first_page:
            for row in table:
                 if re.match(r'^\d+$', row[0].strip()):  # 只保留數字的分類編號
                    category[row[0].strip()] = row[1].strip().replace("\n", "") if row[1] else ''
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if len(row) >= 5:
                        # row[0] = 題號, row[1] = 正確答案, row[2] = 圖片, row[3] = 題目, row[4] = 分類編號
                        correct_ans = row[1].strip() if row[1] else ''
                        question = row[3].strip().replace("\n", "") if row[3] else ''
                        question_num = row[0].strip() if row[0] else ''# 題號
                        comment = f"選擇題第 {question_num} 題，分類{row[4]}|{category.get(row[4], '')}"
                        img_path = f".\src\sign-OX.files\image{question_num}.jpg"
                        # 只抓有內容的題目，不要抓到表頭欄位名，只要第 0 欄是數字就是題目
                        if row[0].isnumeric():
                            extracted_data.append([correct_ans, question ,comment, img_path])
    # 存成 CSV
    with open(f"./gen/{filename}.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["correct_ans", "question", "comment", "image_path"])  # 新增圖片欄位
        writer.writerows(extracted_data)

    print(f"✅ 含圖片的汽車法規題目 {filename}.pdf 已儲轉換到 {filename}.csv")
    return f"./gen/{filename}.csv"
if __name__=='__main__':
    no_img_pdf("car-rule-OX")
    no_img_pdf("car-rule-mc")
    pdf_with_images("sign-OX")
    pdf_with_images("sign-mc")
    create_anki_CSV("./gen/car-rule-mc.csv","汽車法規選擇.apkg")
    create_anki_CSV("./gen/car-rule-OX.csv","汽車法規是非.apkg")
    create_anki_CSV_IMG("./gen/sign-OX.csv","汽車號誌是非.apkg")
    create_anki_CSV_IMG("./gen/sign-mc.csv","汽車號誌選擇.apkg")