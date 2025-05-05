# 臺灣駕照題庫

本儲存庫從[中華民國交通部公路局網站](https://www.thb.gov.tw/cl.aspx?n=12)取得中華民國駕照筆試題目，使用 Python 轉換原始 PDF 為 CSV、 apkg 供大家使用。

## 為什麼有這個儲存庫
因為我要準備考駕照，我想把題目放進 Anki 這個軟體複習。然而，原始題庫是 PDF 格式，不太方便直接導入，因此我撰寫了轉換腳本，將它們轉為純文字的 CSV 格式，再自動生成 Anki 匯入檔案。你可以直接使用這些轉換好的 CSV，依需求修改後套用在其他學習工具上，或是直接使用我在 [release](https://github.com/iach526526/Drivers-License-Exam-TW/releases) 提供的 apkgs 匯入 Anki 中使用。
## 目前提供的題目
### 汽車題庫（中文）
- 汽車法規是非（car-rule-OX）
- 汽車法規選擇（car-rule-mc）
- 汽車號誌是非（sign-OX）
- 汽車號誌選擇（sign-mc）
## 公開版
如果沒有任何特殊需求，我建議直接下載 [releases](https://github.com/iach526526/Drivers-License-Exam-TW/releases)發布的 apkg 。有任何問題請發 issues 告訴我！

## 在本地執行
### 安裝套件
```
pip install -r requirements.txt
```

### 解壓縮圖片(可選)

解壓縮 src/sign-OX.files、src/sign-mc.files ，這是汽車號誌是非和選擇題使用的圖片檔。這是我把 PDF 放進 Word 另存成網頁產出的，我暫時沒有想到比這樣更快速的方法把圖片從 PDF 匯出。剛好檔案很單純，檔名就是題號，在 apkg 可以輕易的連結題目和圖片的關係。匯出後圖片就會在 apkg 裡面，只有在生成 apkg 需要注意路徑問題。如果你想更動 apkg 的題目顯示樣式，請參考[kerrickstaley:genanki](https://github.com/kerrickstaley/genanki)儲存庫查看套件呼叫邏輯。
