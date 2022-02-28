from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

import reportlab
from django.conf import settings
reportlab.rl_config.TTFSearchPath.append(str(BASE_DIR) + '/core/fonts')
#pdfmetrics.registerFont(TTFont('Copperplate', 'Copperplate-Gothic-Bold.ttf'))

pdfmetrics.registerFont(TTFont('Lekton-Regular','Lekton-Regular.ttf'))


canvas = canvas.Canvas("form2.pdf", pagesize=letter)
canvas.setLineWidth(.3)
canvas.setFont('Lekton-Regular', 12)

canvas.drawString(30,750,'OFFICIAL COMMUNIQUE')
canvas.drawString(30,735,'OF ACME INDUSTRIES')
canvas.drawString(500,750,"12/12/2010")
canvas.line(480,747,580,747)

canvas.drawString(275,725,'AMOUNT OWED:')
canvas.drawString(500,725,"$1,000.00")
canvas.line(378,723,580,723)

canvas.drawString(30,703,'RECEIVED BY:')
canvas.line(120,700,580,700)
canvas.drawString(120,703,"JOHN DOE")

canvas.save()