import pdb
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph,  Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
import os, reportlab
from pathlib import Path
from decimal import Decimal
import datetime
from textwrap import wrap

def p_mm(p):
    return p / mm

def mm_p(p):
    return p * mm

class CustomCanvas(canvas.Canvas):
    """
    Adapted from http://code.activestate.com/recipes/576832/
    """
    meux = 10
    meuy = 10

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def setPagePoint(self, x, y):
        self.x = x
        self.y = y

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def drawPageNumber(self, page_count):
        self.setFont('Helvetica-Bold', 14)
        self.drawCentredString(5, 70 * mm, 'DEFER INDÚSTRIA METALÚRGICA')
        self.drawCentredString(100 * mm /2, 60, 'DESTINATÁRIO')
        self.drawCentredString(5, 50 * mm, 'DESTINATÁRIO: HERVAL MOVEIS')
        self.drawCentredString(5, 40 * mm, 'NF: 15888')
        self.drawCentredString(5, 30 * mm, 'Volume: %s / %s' % (self._pageNumber, page_count))
    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            
            self.__dict__.update(state)
            self.setPageSize((100 * mm , 80 * mm ))
            self.drawPageNumber(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)




class Label_volumes:

    def __init__(self, buffer, *args, **kwargs):
        self.buffer = buffer
        self.filename = 'test.pdf'
        self.lbl_width = kwargs['width'] * mm
        self.lbl_height = kwargs['height'] * mm
        self.lbl_emissor = kwargs['emissor'] 
        self.lbl_destinatario = kwargs['destinatario']
        self.lbl_nf = kwargs['nf']
        self.lbl_volumes = kwargs['volumes']
        self.lbl_num_ped = kwargs['num_ped']
        self.lbl_num_oc = kwargs['num_oc']
        self.lbl_center = self.lbl_width / 2
        self.lh = 7 * mm

    def show(self):
        my_canvas = canvas.Canvas(self.buffer)

        lc = self.lbl_center #ponto central
        lh = self.lh # altura da linha
        lbht = self.lbl_height #altura da etiqueta
        lblt = self.lbl_width #largura da etiqueta

        print(self.lbl_destinatario)

        for v in range(self.lbl_volumes):
            volume = v + 1
            pv = lbht - lh * 0.8
            my_canvas.setPageSize((self.lbl_width , self.lbl_height ))
            my_canvas.setFont('Helvetica-Bold', 14)
            my_canvas.drawCentredString(lc, pv, self.lbl_emissor)
            pv -= lh
            my_canvas.setFont('Helvetica-Bold', 10)
            my_canvas.drawCentredString(lc, pv, 'Destinatário:')
            #dest = my_canvas.beginText(10, lt - 3 * lh)
            dest = "\n".join(wrap(self.lbl_destinatario, 31 )) # 80 is line width
            dest_list = dest.splitlines()
            ln = 3
            my_canvas.setFont('Helvetica-Bold', 14)
            for line in dest_list:
                pv -= lh * 0.85
                my_canvas.drawCentredString(lc, pv, line)
            
            pv -= lh
            l= 'NF: %s   -   Volume: %s de: %s' % (self.lbl_nf, volume, self.lbl_volumes)
            my_canvas.drawCentredString(lc, pv, l)
            pv -= lh/2
            x1 = lblt * 0.1
            x2 = lblt * 0.9
            my_canvas.line(x1, pv, x2, pv)
            my_canvas.setFont('Helvetica-Bold', 10)
            pv -= lh/2
            l2= 'Nº Pedido: %s   -   Nº OC Cliente: %s ' % (self.lbl_num_ped, self.lbl_num_oc)
            my_canvas.drawCentredString(lc, pv, l2)
            #my_canvas.drawCentredString(lc, lblh - ln * lh, 'NF: %s' % (self.lbl_nf))
            #my_canvas.drawCentredString(lc, lblh - (ln + 1) * lh, 'Volume: %s / %s' % (volume, self.lbl_volumes))
            my_canvas.showPage()

        my_canvas.save()
        pdf = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf
