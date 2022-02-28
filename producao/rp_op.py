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
        self.canvas = canvas.Canvas('oi.pdf')             
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
       
    def op_individual(self, linha):
                # If the left_footer attribute is not None, then add it to the page
        self.canvas.saveState()
        self.canvas.setFont('Helvetica', 8)
        self.canvas.setTitle(self.titulo)
        
        #header
        #grid
        hh = 100 * mm #altura do cabeçalho
        th = self.bm + self.doc.height
        bh = th - hh
        div1 = self.doc.leftMargin + 40 * mm
        div2 = self.doc.leftMargin + self.doc.width - 40 * mm
        self.canvas.line(self.doc.leftMargin, th, self.doc.width + self.doc.leftMargin, th )
        self.canvas.line(self.doc.leftMargin, bh, self.doc.width + self.doc.leftMargin, bh )
        self.canvas.line(div1, th, div1, bh )
        self.canvas.line(div2, th, div2, bh )
        #texto
        l1 = th - 11
        l2 = l1 - 10
        l3 = l2 - 10
        centro = self.doc.width / 2 + self.doc.leftMargin

        self.px = div2 + 5
        self.py = l3
        print(self.px)
        print(self.py)

        self.canvas.drawString(self.doc.leftMargin + 5, l1, self.empresa)
        self.canvas.drawString(self.doc.leftMargin + 5, l2, self.cnpj)
        self.canvas.drawString(self.doc.leftMargin + 5, l3, self.relatorio)
        
        #div da data
        time = datetime.datetime.today()
        date = time.strftime("Data: %d/%m/%Y")
        hora = time.strftime("Hora: %H:%M:%S")
        self.canvas.drawString(div2 + 5, l1, date)
        self.canvas.drawString(div2 + 5, l2, hora)

        #div do titulo
        self.canvas.setFont('Helvetica', 14)
        self.canvas.drawString(div1 + 10, l2, 'Relatório de produtos')
        
        
        self.canvas.restoreState()

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
            self.op_individual(linha)



class Rpt_op_class():
    def __init__(self, canvas, *args, **kwargs):
        self.p = canvas
        self.larg, self.alt = A4
        self.titulo = 'Ordem de produção'
        self.tm = 10 * mm
        self.bm = 10 * mm
        self.lm = 10 * mm
        self.rm = 10 * mm
        self.empresa = 'Defer Indústria Metalúrgica'
        self.cnpj = '04.408.568/0001-05'
        self.tit_relatorio = 'Ordem de produção'
        self.p.setFont('Helvetica', 8)
        self.p.setTitle(self.titulo)
        self.hh = 15  * mm #altura do cabeçalho
        self.th = self.alt - self.tm #topo do cabeçalho
        self.bh = self.th - self.hh #base do cabeçalho
        self.larg_u = self.larg - self.lm -self.rm #largura util
        self.alt_u = self.alt - self.tm - self.bm #altura util
        self.rMax = self.larg - self.rm
        self.lMax = self.lm
        self.div1 = self.lm + 40 * mm
        self.div2 = self.lm + self.larg_u - 40 * mm
        self.pos = self.alt

    def header(self):
        p = self.p
        larg = self.larg
        alt = self.alt
        pos = self.pos
        

        #conteúdo
        ##dados da página

        p.line(self.lm, self.th, self.larg + self.lm, self.th )
        p.line(self.lm, self.bh, self.larg + self.lm, self.bh )
        p.line(self.div1, self.th, self.div1, self.bh )
        p.line(self.div2, self.th, self.div2, self.bh )
        #texto
        l1 = self.alt - self.tm - 11
        l2 = l1 - 10
        l3 = l2 - 10
        centro = self.larg / 2 + self.lm

        px = self.div2 + 5
        py = l3
        print(px)
        print(py)

        p.drawString(self.lm , l1, self.empresa)
        p.drawString(self.lm , l2, self.cnpj)
        p.drawString(self.lm , l3, self.tit_relatorio)
        
        #div da data
        time = datetime.datetime.today()
        date = time.strftime("Data: %d/%m/%Y")
        hora = time.strftime("Hora: %H:%M:%S")
        p.drawString(self.div2 + 5, l1, date)
        p.drawString(self.div2 + 5, l2, hora)

        #div do titulo
        p.setFont('Helvetica', 14)
        p.drawString(self.div1 + 10, l2, 'self.tit_relatorio')
    
    def corpo(self):
        p = self.p
        p.line(self.lMax, self.alt - 140 * mm, self.rMax, self.alt - 140 * mm )

    
    def relatorio(self):
        for reg in range(2):
            pass
            self.header()
            self.corpo()
            self.pos = self.pos - 150 * mm
        #return self.p
