import os

import pymupdf

font_path = "/Library/Fonts/PlemolJPConsoleNF-Regular.ttf"


if not os.path.exists(font_path):
    raise FileNotFoundError(f"フォントファイルが見つかりません: {font_path}")

# 元のPDFファイルを開く
input_pdf_path = "input.pdf"
output_pdf_path = "output.pdf"
doc = pymupdf.open(input_pdf_path)

# テキストを追加するページ番号（0始まり）
page_number = 0
page = doc[page_number]

# テキストを追加する位置（x, y座標）
x, y = 100, 100
text = "テスト"

# テキストを描画する
font_name = "PlemolJPConsoleNF-Regular"
pymupdf.Font(fontname=font_name, fontfile=font_path)
page.insert_text(
    (x, y),  # 位置
    text,  # テキスト
    fontsize=12,  # フォントサイズ
    fontname=font_name,
    fontfile=font_path,  # フォントファイル
    color=(0, 0, 0),  # テキストの色 (黒)
)

# 変更を保存
doc.save(output_pdf_path)
doc.close()

print(f"テキストを追加したPDFを保存しました: {output_pdf_path}")
