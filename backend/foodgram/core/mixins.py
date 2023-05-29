from django.conf import settings
from fpdf import FPDF
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class PDF(FPDF):
    """Класс назначает шапку и подвал PDF-файла."""

    header_height = 25
    footer_height = 20
    width_a4 = 210
    height_a4 = 297
    color_header_footer = (159, 43, 104, )
    color_rect = (140, 43, 104, )

    def header(self):
        """Задаёт шапку."""
        header_text = 'ПРОЕКТ "ПРОДУКТОВЫЙ ПОМОЩНИК"'

        self.set_draw_color(*self.color_rect)
        self.set_line_width(1)
        self.rect(10, self.header_height + 1, 190,
                  self.height_a4 - self.footer_height
                  - self.header_height - 2, style='D')

        self.set_fill_color(*self.color_header_footer)
        self.rect(0, 0, self.width_a4, self.header_height, 'F')
        self.add_font('CuprumRU', '',
                      f'{settings.BASE_DIR}/static/fonts/Cuprum-Bold.ttf',
                      uni=True)
        self.set_font('CuprumRU', '', 20)
        w = self.get_string_width(header_text) + 6
        self.set_x((self.width_a4 - w) / 2)
        self.cell(w, 9, header_text, ln=1, align='C')
        self.ln(10)

    def footer(self):
        """Задаёт подвал."""
        self.set_y(-15)
        self.set_fill_color(*self.color_header_footer)
        self.rect(0, self.height_a4 - self.footer_height,
                  self.width_a4, self.footer_height, 'F')
        self.add_font('CuprumRU', '',
                      f'{settings.BASE_DIR}/static/fonts/Cuprum-Bold.ttf',
                      uni=True)
        self.set_font('CuprumRU', '', 14)
        self.cell(0, 10, 'Стр. ' + str(self.page_no()), 0, 0, 'C')


class ListDestroyCreateModelViewSet(GenericViewSet, DestroyModelMixin,
                                    ListModelMixin, CreateModelMixin, ):
    """Набор представлений 'create()', 'destroy()' и 'list()' по умолчанию."""
    pass
