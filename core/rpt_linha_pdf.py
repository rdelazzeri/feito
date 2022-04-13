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
        self.dados = kwargs['dados'] if 'dados' in kwargs else 'VAZIO'
        BASE_DIR = Path(__file__).resolve().parent.parent
        reportlab.rl_config.TTFSearchPath.append(str(BASE_DIR) + '/core/fonts')
        registerFont(TTFont('Lekton-Regular','Lekton-Regular.ttf'))
             
        self.doc = SimpleDocTemplate(self.buffer, pagesize=A4,
                                     topMargin = 2 * cm, bottomMargin = 1 * cm,
                                     leftMargin = 1 * cm, rightMargin = 1 * cm)
        
        self.titulo = 'Meu título'
      
        self.tm = 20 * mm
        self.bm = 20 * mm
        self.lm = 20 * mm
        self.rm = 20 * mm
        self.Story = []

    def onMyFirstPage(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        canvas.setTitle(self.titulo)
        canvas.restoreState()

    def onMyLaterPages(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        canvas.setTitle(self.titulo)
        canvas.restoreState()

    def onAllPages(self, canvas, doc):
        # If the left_footer attribute is not None, then add it to the page
        canvas.saveState()
        canvas.setTitle(self.titulo)
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
        styles.add(ParagraphStyle(name='st_normal', fontName='Lekton-Regular', fontSize = 8)) 
        #styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        #justify = styles['Justify']
        normal = styles['st_normal']
        dados = self.dados

        for linha in dados:
            self.Story.append(Paragraph(linha, normal))