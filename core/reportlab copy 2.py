import pdb
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph,  Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
import os, reportlab
from pathlib import Path

    
def p_mm(p):
    return p / mm

def mm_p(p):
    return p * mm


class MyPrint:

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='st_normal', fontName='Lekton-Regular')) 

    def __init__(self, buffer, pagesize, data):
        self.buffer = buffer
        self.data = data
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        ##Registro da Fonte
        BASE_DIR = Path(__file__).resolve().parent.parent
        reportlab.rl_config.TTFSearchPath.append(str(BASE_DIR) + '/core/fonts')
        registerFont(TTFont('Lekton-Regular','Lekton-Regular.ttf'))

        ##variáveis de inicialização
        self.titulo = ''
        self.autor = 'Feito engenharia e sistemas'
        self.assunto = ''
        self.topMargin = 20
        self.bottomMargin = 20
        self.leftMargin = 20
        self.rightMargin = 20
        self.docHeight = 0
        self.linhas = []


    def print_users(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin = self.rightMargin * mm,
                                leftMargin = self.leftMargin * mm,
                                topMargin = self.topMargin * mm,
                                bottomMargin = self.bottomMargin * mm,
                                pagesize=self.pagesize)
 
        self.docHeight = doc.height
        elements = []
        styles = self.styles

        elements.append(Spacer(1, 3 * mm))
        elements.append(Paragraph('Lista de produtos', styles['Heading1']))
        elements.append(Spacer(1, 3 * mm))

        for i, row in enumerate(self.data):
            line = '{}  -  {}  -  {}'.format(row['cod'], row['desc'], row['unidCyber'])
            elements.append(Paragraph(line, styles['Normal']))
 
        doc.build(elements, canvasmaker=NumberedCanvas)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

class NumberedCanvas(canvas.Canvas):


    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = []

     def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            #pdb.set_trace()
            self.setFont('Lekton-Regular', 8)
            self.draw_page_number(num_pages)
            self.meuHeader()
            self.meuFooter(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)
 
    def meuHeader(self):
        headerHeight = 15
        #pv = self.height + self.bottomMargin
        self.setLineWidth(0.3)
        self.setFont('Lekton-Regular', 10, 2)
        self.line(self.leftMargin, 300, self.width + self.leftMargin, 300 )
        self.drawString(self.leftMargin, pv, 'Defer Indústria Metalúrgica Ltda ')
        self.drawRightString(self.leftMargin + self.width, pv, '14/02/2022')
        self.line(self.leftMargin, pv-3, self.width + self.leftMargin, pv-3 )
        self.setAuthor("Feito engenharia e sistemas")
        #self.setTitle(tit)
        self.setSubject("Lista de produtos")

    def meuFooter(self, page_count):
        pass
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString( 700, 30, "Page %d of %d" % (self._pageNumber, page_count))

