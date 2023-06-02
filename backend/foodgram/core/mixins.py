from django.conf import settings
from fpdf import FPDF
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class PDF(FPDF):
    """Класс назначает шапку и подвал PDF-файла."""

    width_a4 = 210
    height_a4 = 297

    def header(self):
        """Задаёт шапку."""
        header_text = 'ПРОЕКТ "ПРОДУКТОВЫЙ ПОМОЩНИК"'

        self.set_draw_color(*settings.COLOR_RECT)
        self.set_line_width(1)
        self.rect(10, settings.HEADER_HEIGNT + 1, 190,
                  self.height_a4 - settings.FOOTER_HEIGNT
                  - settings.HEADER_HEIGNT - 2, style='D')

        self.set_fill_color(*settings.COLOR_HEADER_FOOTER)
        self.rect(0, 0, self.width_a4, settings.HEADER_HEIGNT, 'F')
        self.add_font(settings.FONT, '',
                      f'{settings.BASE_DIR}/core/fonts/Cuprum-Bold.ttf',
                      uni=True)
        self.set_font(settings.FONT, '', settings.SIZE_FONT + 6)
        w = self.get_string_width(header_text) + 6
        self.set_x((self.width_a4 - w) / 2)
        self.cell(w, 9, header_text, ln=settings.LINE, align='C')
        self.ln(10)

    def footer(self):
        """Задаёт подвал."""
        self.set_y(-15)
        self.set_fill_color(*settings.COLOR_HEADER_FOOTER)
        self.rect(0, self.height_a4 - settings.FOOTER_HEIGNT,
                  self.width_a4, settings.FOOTER_HEIGNT, 'F')
        self.add_font(settings.FONT, '',
                      f'{settings.BASE_DIR}/core/fonts/Cuprum-Bold.ttf',
                      uni=True)
        self.set_font(settings.FONT, '', settings.SIZE_FONT)
        self.cell(settings.CELL_WIDTH, settings.CELL_HEIGNT,
                  'Стр. ' + str(self.page_no()), 0, 0, 'C')


class ListDestroyCreateModelViewSet(GenericViewSet, DestroyModelMixin,
                                    ListModelMixin, CreateModelMixin, ):
    """Набор представлений 'create()', 'destroy()' и 'list()' по умолчанию."""
    pass
