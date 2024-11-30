import os
from dataclasses import dataclass

import pymupdf
from pymupdf import Page


@dataclass
class InsertProperty:
    pos: tuple[int, int]
    text: str
    fontsize: int | None = None
    fontname: str | None = None
    fontfile: str | None = None
    color: tuple[int, int, int] | None = None
    label: str = ""

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]


class PdfWriter:
    def __init__(
        self,
        input_path: str = "input.pdf",
        output_path: str = "output.pdf",
        default_font_path: str = "/Library/Fonts/PlemolJPConsoleNF-Regular.ttf",
        default_font_size: int = 12,
    ):
        if not os.path.exists(input_path):
            msg = f"PDFファイルが見つかりません: {input_path}"
            raise FileNotFoundError(msg)
        self._input_path = input_path
        self._output_path = output_path
        self._default_font_path = default_font_path
        self._default_font_size = default_font_size
        if not os.path.exists(self._default_font_path):
            msg = f"フォントファイルが見つかりません: {self._default_font_path}"
            raise FileNotFoundError(msg)
        self._font_name = "DefaultFont"
        self._default_font_color = (0, 0, 0)

    def execute(self, properties: list[InsertProperty], page_num: int = 1):
        # フォントを登録
        pymupdf.Font(fontname=self._font_name, fontfile=self._default_font_path)

        # PDFファイルを開く
        doc = pymupdf.open(self._input_path)

        # ページを指定して、テキストを追加
        page = doc[page_num - 1]
        for p in properties:
            self._insert_text(page, p)

        # 変更を保存
        doc.save(self._output_path)
        doc.close()

    def _insert_text(self, page: Page, prop: InsertProperty) -> int:
        return page.insert_text(
            (prop.x, prop.y),
            prop.text,
            fontsize=prop.fontsize or self._default_font_size,
            fontname=prop.fontname or self._font_name,
            fontfile=prop.fontfile or self._default_font_path,
            color=prop.color or self._default_font_color,
        )
