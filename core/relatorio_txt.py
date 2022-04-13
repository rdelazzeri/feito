from django.utils.safestring import mark_safe


class MeuReport:

    def __init__(self, *args, **kwargs):
        self.linhas = []
        self.text = ''
    
    def linha(self, linha):
        self.linhas.append(mark_safe(linha))

    def rel(self):

        return self.linhas

    def campo(self, valor, tamanho, posicao):

        if valor is None:
            valor = ''
        if posicao == 'l':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = str1 + '&nbsp;' * l  
        elif posicao == 'r':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = '&nbsp;' * l + str1     
        elif posicao == 'c':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = '&nbsp;' * int(l/2) + str1 + '&nbsp;' * int(l/2) 
        elif posicao == 'b':
            campo = str('&nbsp; ' * tamanho )
        elif posicao == 'f':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = str1 + str1 * l
        else: 
            campo = 'erro'
        return str(campo)

    def sub_head(self, titulo, tamanho):
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('', tamanho, 'l'))
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo(titulo, tamanho, 'c'))
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('-', tamanho, 'f'))

class MeuReport2:

    def __init__(self, *args, **kwargs):
        self.linhas = []
        self.text = ''
    
    def linha(self, linha):
        #self.linhas.append(mark_safe(linha + '<br/>'))
        self.text += mark_safe(linha + '\r\n')
    
    def text_line(self, linha):
        self.text += mark_safe(linha + '<br/>')

    def rel(self):

        return self.text

    def campo(self, valor, tamanho, posicao):

        if valor is None:
            valor = ''
        if posicao == 'l':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = str1 + ' ' * l  
        elif posicao == 'r':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = ' ' * l + str1     
        elif posicao == 'c':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = ' ' * int(l/2) + str1 + ' ' * int(l/2) 
        elif posicao == 'b':
            campo = str(' ' * tamanho )
        elif posicao == 'f':
            str1 = str(valor)
            l = tamanho - len(str1)
            campo = str1 + str1 * l
        else: 
            campo = 'erro'
        return str(campo)

    def sub_head(self, titulo, tamanho):
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('', tamanho, 'l'))
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo(titulo, tamanho, 'c'))
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('-', tamanho, 'f'))

