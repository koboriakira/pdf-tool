import os
from dataclasses import dataclass

import pymupdf


@dataclass
class InsertProperty:
    pos: tuple[int, int]
    text: str
    fontsize: int | None = None
    fontname: str | None = None
    fontfile: str | None = None
    color: tuple[int, int, int] | None = None
    label: str = ""


class PdfWriter:
    def __init__(
        self,
        input_path: str = "input.pdf",
        output_path: str = "output.pdf",
        default_font_path: str = "/Library/Fonts/PlemolJPConsoleNF-Regular.ttf",
        default_font_size: int = 12,
    ):
        self._input_path = input_path
        self._output_path = output_path
        self._default_font_path = default_font_path
        self._default_font_size = default_font_size
        if not os.path.exists(self._default_font_path):
            msg = f"フォントファイルが見つかりません: {self._default_font_path}"
            raise FileNotFoundError(msg)
        self._font_name = "DefaultFont"
        self._default_font_color = (0, 0, 0)

    def execute(self, properties: list[InsertProperty]):
        pymupdf.Font(fontname=self._font_name, fontfile=self._default_font_path)

        # 元のPDFファイルを開く
        doc = pymupdf.open(self._input_path)

        # テキストを追加するページ番号（0始まり）
        page_number = 0
        page = doc[page_number]

        # テキストを追加する位置（x, y座標）
        for p in properties:
            page.insert_text(
                (p.pos[0], p.pos[1]),  # 位置
                p.text,  # テキスト
                fontsize=p.fontsize or self._default_font_size,  # フォントサイズ
                fontname=p.fontname or self._font_name,
                fontfile=p.fontfile or self._default_font_path,  # フォントファイル
                color=p.color or self._default_font_color,  # テキストの色
            )

        # 変更を保存
        doc.save(self._output_path)
        doc.close()

        print(f"テキストを追加したPDFを保存しました: {self._output_path}")
