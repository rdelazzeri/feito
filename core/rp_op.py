import pdb
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph,  Spacer
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
        self.setFont('Helvetica', 8)
        self.drawString(458.54, 782.45, 
                             'Página: %s / %s' % (self._pageNumber, page_count))
    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.drawPageNumber(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)



class MyReport:

    px = 10
    py = 10

    def __init__(self, buffer, *args, **kwargs):
        self.buffer = buffer
        self.filename = 'test.pdf'

        BASE_DIR = Path(__file__).resolve().parent.parent
        reportlab.rl_config.TTFSearchPath.append(str(BASE_DIR) + '/core/fonts')
        registerFont(TTFont('Lekton-Regular','Lekton-Regular.ttf'))
             
        self.doc = SimpleDocTemplate(self.buffer, pagesize=A4,
                                     topMargin = 2 * cm, bottomMargin = 1 * cm,
                                     leftMargin = 1 * cm, rightMargin = 1 * cm)
        
        self.left_footer = kwargs['left_footer'] if 'left_footer' in kwargs else ''
        self.titulo = kwargs['titulo'] if 'titulo' in kwargs else ''
        self.empresa = kwargs['empresa'] if 'empresa' in kwargs else 'Defer Indústria Metalúrgica'
        self.cnpj = kwargs['cnpj'] if 'cnpj' in kwargs else '04.408.568/0001-05'
        self.relatorio = kwargs['relatorio'] if 'relatorio' in kwargs else 'RPR-001/BVD'
        self.dados = kwargs['dados'] if 'dados' in kwargs else 'fazio'
        
        self.tm = 20 * mm
        self.bm = 20 * mm
        self.lm = 20 * mm
        self.rm = 20 * mm
        #self.px = 10
        #self.py = 10
        self.Story = []

    def onMyFirstPage(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        canvas.setTitle(self.titulo)
        if self.left_footer is not None:
            canvas.setFont('Helvetica', 8)
            canvas.drawString(1 * cm, 28 * cm, self.titulo)
            canvas.drawString(1 * cm, 1 * cm, self.left_footer)
        canvas.restoreState()

    def onMyLaterPages(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        canvas.setTitle(self.titulo)
        if self.left_footer is not None:
            canvas.setFont('Helvetica', 8)
            canvas.drawString(1 * cm, 28 * cm, self.titulo)
            canvas.drawString(1 * cm, 1 * cm, self.left_footer)
        canvas.restoreState()

    def onAllPages(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setTitle(self.titulo)
        
        #header
        #grid
        hh = 12 * mm #altura do cabeçalho
        th = self.bm + doc.height
        bh = th - hh
        div1 = doc.leftMargin + 40 * mm
        div2 = doc.leftMargin + doc.width - 40 * mm
        canvas.line(doc.leftMargin, th, doc.width + doc.leftMargin, th )
        canvas.line(doc.leftMargin, bh, doc.width + doc.leftMargin, bh )
        canvas.line(div1, th, div1, bh )
        canvas.line(div2, th, div2, bh )
        #texto
        l1 = th - 11
        l2 = l1 - 10
        l3 = l2 - 10
        centro = doc.width / 2 + doc.leftMargin

        self.px = div2 + 5
        self.py = l3
        print(self.px)
        print(self.py)

        canvas.drawString(doc.leftMargin + 5, l1, self.empresa)
        canvas.drawString(doc.leftMargin + 5, l2, self.cnpj)
        canvas.drawString(doc.leftMargin + 5, l3, self.relatorio)
        
        #div da data
        time = datetime.datetime.today()
        date = time.strftime("Data: %d/%m/%Y")
        hora = time.strftime("Hora: %H:%M:%S")
        canvas.drawString(div2 + 5, l1, date)
        canvas.drawString(div2 + 5, l2, hora)

        #div do titulo
        canvas.setFont('Helvetica', 14)
        canvas.drawString(div1 + 10, l2, 'Relatório de produtos')
        
        
        canvas.restoreState()
        

    def generateReport(self):
        self.reportContent()
        
        '''        
        self.doc.build(self.Story, canvasmaker=CustomCanvas, 
                       onFirstPage=self.onAllPages,
                       onLaterPages=self.onAllPages)'''
        self.doc.build(self.Story)

        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf    

    def reportContent(self):
        styles = getSampleStyleSheet()
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='st_normal', fontName='Lekton-Regular', fontSize = 10)) 
        #styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        #justify = styles['Justify']
        normal = styles['st_normal']
        dados = self.dados

        for linha in dados:
            self.Story.append(Paragraph(linha, normal))