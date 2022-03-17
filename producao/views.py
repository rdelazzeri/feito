from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.forms import formset_factory
from io import BytesIO
from .rp_op import *
from .models import *
from .forms import *
from django.db import transaction
from django.utils.safestring import mark_safe


class ProdutoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('nome-autocomplete')
        if not self.request.user.is_authenticated:
            return Prod.objects.none()
        qs = Prod.objects.only('desc')
        if self.q:
            qs = qs.filter(desc__icontains=self.q)
        return qs

def op_delitem(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        id = request.POST.get('item_id')
        if source == 'CF':
            obj = OP_componente_fisico.objects.get(id=id).delete()
        elif source == 'SI':
            obj = OP_componente_servico_interno.objects.get(id=id).delete()
        elif source == 'SE':
            obj = OP_componente_servico_externo.objects.get(id=id).delete()
        return HttpResponse('Item Excluido')


@transaction.atomic
def op_comp_fis_add(request):
    if request.method == 'GET':
        op = OP.objects.get(id = int(request.GET.get('id')))
        prod = Prod.objects.get(id = int(request.GET.get('produto')))
        if prod.tipoProduto.cod == 'CO':
            it = OP_componente_fisico()
        elif prod.tipoProduto.cod == 'SI':
            it = OP_componente_servico_interno()
        elif prod.tipoProduto.cod == 'SE':
            it = OP_componente_servico_externo()
        it.op = op
        it.produto = prod
        it.qtd_programada = 1
        it.save()
        return HttpResponse('Produto adicionado')
    else:
        return HttpResponse('nao é post')


def op_new(request):
    print('op_new/00')
    if request.method == "POST":
        print('op_new/01')
        form = OP_detail_form(request.POST)
        if form.is_valid():
            print('op_new/02')
            fr = form.save(commit=False)
            fr.save()
            return redirect('producao:op_detail', fr.id) 
        else:
            print('op_new/03')
            return render(request, 'producao/op_detail.html', {'form': form})     
    else:
        print('op_new/ 10')
        form = OP_detail_form()
        return render(request, 'producao/op_detail.html', {'form': form})  



def formset_comp_fis(**kwargs):
    op_comp_fis_formset = formset_factory(OP_comp_fis_formset, OP_comp_fis_BaseFormSet, extra=0 )
    if kwargs.get('op'):
        op = kwargs.get('op')
        op_comp_fis = op.op_comp_fis.all() 
        op_comp_fis_initial = [{
            'item_id': l.id,
            'source': 'CF',
            'cod': l.produto.cod,
            'desc': l.produto.desc, 
            'unid': l.produto.unid.unid, 
            'qtd_programada': l.qtd_programada, 
            'qtd_utilizada': l.qtd_utilizada,
            'qtd_perda':l.qtd_perda,
            'custo_unit': l.custo_unitario, 
            'custo_tot':l.custo_total,
            'nivel':l.nivel,
            }for l in op_comp_fis] 
        formset = op_comp_fis_formset(initial = op_comp_fis_initial) 
        return formset
    if kwargs.get('request'):
        request = kwargs.get('request')
        formset = op_comp_fis_formset(request)
        if formset.is_valid():
            try:
                for it in formset:
                    if id:
                        item_id = it.cleaned_data.get('item_id')
                        itens_data = OP_componente_fisico.objects.get(pk=item_id)
                        itens_data.qtd_programada = it.cleaned_data.get('qtd_programada')
                        itens_data.qtd_utilizada = it.cleaned_data.get('qtd_utilizada')
                        itens_data.custo_unit = it.cleaned_data.get('custo_unit')
                        itens_data.nivel = it.cleaned_data.get('nivel')
                        itens_data.qtd_perda = it.cleaned_data.get('qtd_perda')
                        itens_data.save()
                return True
            except:
                raise
        else:
            return False
 
def formset_serv_int(**kwargs):
    op_serv_int_formset = formset_factory(OP_serv_int_formset, OP_serv_int_BaseFormSet, extra=0 )
    if kwargs.get('op'):
        op = kwargs.get('op')
        op_serv_int = op.op_serv_int.all() 
        op_serv_int_initial = [{
            'item_id': l.id,
            'source': 'SI',
            'cod': l.produto.cod,
            'desc': l.produto.desc, 
            'unid': l.produto.unid.unid, 
            'tempo_estimado': l.tempo_estimado,
            'tempo_realizado': l.tempo_realizado,
            'tempo_parada':l.tempo_parada,
            'custo_unit': l.custo_unitario, 
            'custo_tot':l.custo_total,
            'nivel':l.nivel,
            'operador':l.operador,
            }for l in op_serv_int] 
        formset = op_serv_int_formset(initial = op_serv_int_initial) 
        return formset
    if kwargs.get('request'):
        request = kwargs.get('request')
        formset = op_serv_int_formset(request)
        if formset.is_valid():
            try:
                for it in formset:
                    if id:
                        item_id = it.cleaned_data.get('item_id')
                        itens_data = OP_componente_servico_interno.objects.get(pk=item_id)
                        itens_data.tempo_estimado = it.cleaned_data.get('tempo_estimado')
                        itens_data.tempo_realizado = it.cleaned_data.get('tempo_realizado')
                        itens_data.custo_unit = it.cleaned_data.get('custo_unit')
                        itens_data.nivel = it.cleaned_data.get('nivel')
                        itens_data.tempo_parada = it.cleaned_data.get('tempo_parada')
                        itens_data.operador = it.cleaned_data.get('operador')
                        itens_data.save()
                return True
            except:
                raise
        else:
            return False

def formset_serv_ext(**kwargs):
    op_serv_ext_formset = formset_factory(OP_comp_fis_formset, OP_comp_fis_BaseFormSet, extra=0 )
    if kwargs.get('op'):
        op = kwargs.get('op')
        op_serv_ext = op.op_serv_ext.all() 
        op_serv_ext_initial = [{
            'item_id': l.id,
            'source': 'SE',
            'cod': l.produto.cod,
            'desc': l.produto.desc, 
            'unid': l.produto.unid.unid, 
            'tempo_estimado': l.tempo_estimado,
            'tempo_realizado': l.tempo_realizado,
            'tempo_parada':l.tempo_parada,
            'custo_unit': l.custo_unitario, 
            'custo_tot':l.custo_total,
            'nivel':l.nivel,
            'operador':l.operador,
            }for l in op_serv_ext] 
        formset = op_serv_ext_formset(initial = op_serv_ext_initial) 
        return formset
    if kwargs.get('request'):
        request = kwargs.get('request')
        formset = op_serv_ext_formset(request)
        if formset.is_valid():
            try:
                for it in formset:
                    if id:
                        item_id = it.cleaned_data.get('item_id')
                        itens_data = OP_componente_fisico.objects.get(pk=item_id)
                        itens_data.qtd_programada = it.cleaned_data.get('qtd_programada')
                        itens_data.qtd_utilizada = it.cleaned_data.get('qtd_utilizada')
                        itens_data.custo_unit = it.cleaned_data.get('custo_unit')
                        itens_data.nivel = it.cleaned_data.get('nivel')
                        itens_data.qtd_perda = it.cleaned_data.get('qtd_perda')
                        itens_data.save()
                return True
            except:
                raise
        else:
            return False

def form_op(**kwargs):
    if kwargs.get('request'):
        try:
            request = kwargs.get('request')
            op = kwargs.get('op')
            form = OP_detail_form(request.POST, instance = op)
            op = form.save(commit=False)
            op.save()
            return True
        except:
            raise
    else:
        if kwargs.get('op'):
            op = kwargs.get('op')
            form = OP_detail_form(instance  = op)
            return form



def op_detail(request, pk):
    op = get_object_or_404(OP, pk=pk)
    #op_comp_fis_formset = formset_factory(OP_comp_fis_formset, OP_comp_fis_BaseFormSet, extra=0 )
    #formset_serv_interno = formset_serv_int(op = op)

    if request.method == 'POST':
        try:
            if form_op(request = request, op = op):
                if formset_comp_fis(request = request.POST):
                    if formset_serv_int(request = request.POST):
                        if formset_serv_ext(request = request.POST):
                            return redirect('producao:op_detail', op.id)
        except:
            raise
            
    elif request.method == 'GET':
        data = {}
        data['form'] = OP_detail_form(instance  = op)
        data['formset'] = formset_comp_fis(op = op)
        data['formset_serv_int'] = formset_serv_int(op = op) 
        data['formset_serv_ext'] = formset_serv_ext(op = op)     
        data['id'] = op.id
        return render(request, 'producao/op_detail.html', data)

@transaction.atomic
def prod_save(request):
    if request.method == 'GET':
        op_id = request.GET.get('op_id')
        dt = request.GET.get('data')
        prod = Decimal(request.GET.get('qtd_produzida'))
        perd = Decimal(request.GET.get('qtd_perdida'))
        print(op_id)
        print(dt)
        print(prod)
        print(perd)
        result = producao_save(op_id, dt, prod, perd)

        if result:
            return HttpResponse('feito')
        else:
            return HttpResponse('não feito')


@transaction.atomic
def producao_save(op_id, data, qtd_produzida, qtd_perda):

    op = OP.objects.get(id=op_id)
    opcf = OP_componente_fisico.objects.filter(op=op_id)
    print(opcf)
    op.qtd_realizada += qtd_produzida
    op.qtd_perda += qtd_perda
    

    #adiciona produção no estoque
    
    mov = {}
    mov['data'] = data
    mov['desc'] = 'OP: %s Entrada produção' %(op.num)
    mov['produto'] = op.produto
    mov['qtd_entrada'] = qtd_produzida
    mov['qtd_saida'] = 0
    mov['valor'] = op.produto.cmv if op.produto.cmv != None else 0
    mov['tipo'] = 'OP_E'
    mov['chave'] = op_id        
    m = apps.get_model('estoque.Movimento')
    print(mov)
    m.objects.movimento_save(mov)
    #movimento_save(mov)

    print('passei pelo save mov')
    #baixa matérias primas do estoque

    for mp in opcf:
        print(mp)
        mov = {}
        mov['data'] = data
        mov['desc'] = 'OP: %s Baixa MP' %(op.num)
        mov['produto'] = mp.produto
        mov['qtd_entrada'] = 0
        mov['qtd_saida'] = mp.qtd_programada / op.qtd_programada * (qtd_produzida + qtd_perda)
        mov['valor'] = mp.produto.cmv if mp.produto.cmv != None else 0
        mov['tipo'] = 'OP_S'
        mov['chave'] = op_id        
        m = apps.get_model('estoque.Movimento')
        print(mov)
        m.objects.movimento_save(mov)

    op.save()
    return True




class MeuReport:
    #from django.http import FileResponse

    def __init__(self, *args, **kwargs):
        self.linhas = []
        self.response = HttpResponse(content_type='application/pdf')
        self.response['Content-Disposition'] = 'inline; filename="My Users.pdf"'
        self.buffer = BytesIO()
    
    def linha(self, linha):
        self.linhas.append(mark_safe(linha))

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
            self.linha('<span class="oi">' + self.campo(titulo, tamanho, 'c') + '</span>' )
            #self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('-', tamanho, 'f'))

    def show(self, buffer):
        print(self.linhas)
        meuKwarg = {}
        meuKwarg['titulo'] = 'meu titulo'
        meuKwarg['left_footer'] = 'meu footer'
        meuKwarg['dados'] = self.linhas
        report = MyReport(buffer, **meuKwarg)
        # I can now specify my custom foot  er in runtime!
        pdf = report.generateReport()
        #self.response.write(pdf)
        return pdf

























def pdf(request):
    from django.http import FileResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="My Users.pdf"'
    buffer = BytesIO()

    prods = Prod.objects.filter(cod__startswith = '10')

    r = MeuReport()

    l_prods = []
    for prod in prods:
        #l = str(prod.cod).ljust(15) + str(prod.desc).ljust(60) + str(prod.unid.unid).ljust(4)
        l = str(r.campo(prod.cod, 20, 'l')) +  r.campo(prod.desc, 80, 'l') +  r.campo(prod.unid.unid, 2, 'l')
        #print(l)
        l_prods.append(l)

    #print(prods)
    #report = MyPrint(buffer, 'A4', prods)
    #report.titulo = 'kfjldjsa'
    #report.setTitle('meu relatorio')
    #pdf = report.print_users()

    meuKwarg = {}
    meuKwarg['titulo'] = 'meu titulo'
    meuKwarg['left_footer'] = 'meu footer'
    meuKwarg['dados'] = l_prods


    report = MyReport(buffer, **meuKwarg)
    # I can now specify my custom foot  er in runtime!
    pdf = report.generateReport()


    response = r.linhas
    return response



def rpt_op(request):
    from django.utils.safestring import mark_safe, SafeData

    response = HttpResponse()
    buffer = BytesIO()
    id = request.GET.get('op_id')
    print(f'imprimindo op: {id}' )

    op = OP.objects.get(id=id)
    op_comp_fis = OP_componente_fisico.objects.filter(op = id).select_related()
    r = MeuReport()
    #rel = []
    #l = str(campo('Código', 15)) +  campo('Descrição', 60) +  campo('Quantidade', 10 + campo('Unid.', 4))
    r.sub_head('ORDEM DE PRODUÇÃO', 125)
    r.linha(r.campo('Número OP: ', 15, 'l') +  r.campo(op.num, 20, 'l') +  r.campo('Data emissão: ', 15, 'l') + r.campo(op.data_emissao, 4, 'l'))
    
    r.sub_head('PRODUTO', 125)
    r.linha(r.campo('Código', 15, 'l')
                + r.campo('Descrição', 60, 'l')
                + r.campo('Qtd.', 10, 'l')
                + r.campo('Unid.', 8, 'l')
                + r.campo('Qtd2', 8, 'l')
                + r.campo('Unid2', 8, 'l')
                )
    r.linha(r.campo(op.produto.cod, 15, 'l')
                + r.campo(op.produto.desc, 60, 'l')
                + r.campo(op.qtd_programada, 10, 'l')
                + r.campo(op.produto.unid, 8, 'l')
                + r.campo(op.produto.fatorUnid, 8, 'l')
                + r.campo(op.produto.unid2, 8, 'l')
                )

    
    r.sub_head('COMPOSIÇÃO', 125)
    r.linha(r.campo('Código', 15, 'l')
                + r.campo('Descrição', 60, 'l')
                + r.campo('Qtd.', 10, 'l')
                + r.campo('Unid.', 8, 'l')
                + r.campo('Qtd2', 8, 'l')
                + r.campo('Unid2', 8, 'l')
                )           

    for n in op.op_comp_fis.all():
        if n:
            linha = (r.campo(n.produto.cod, 15, 'l') 
                        + r.campo(n.produto.desc, 60, 'l') 
                        + r.campo(n.qtd_programada, 10, 'l'))
            
            linha = linha + r.campo(n.produto.unid, 8, 'l') if n.produto.unid else linha + r.campo('', 8, 'b')
            linha = linha + r.campo(n.produto.fatorUnid, 8, 'l') if n.produto.fatorUnid else linha + r.campo('', 8, 'b') 
            linha = linha + r.campo(n.produto.unid2, 8, 'l') if n.produto.unid2 else linha + r.campo('', 8, 'b')
                         
            r.linha(linha)


    #response.write(r.show(buffer))

    #meuKwarg = {}
    #meuKwarg['titulo'] = 'meu titulo'
    #meuKwarg['left_footer'] = 'meu footer'
    #meuKwarg['dados'] = r.linhas

    #rep = MyReport(buffer, **meuKwarg)
    #pdf = rep.generateReport()
   
    x = []
    for l in r.linhas:
        response.writelines(mark_safe(l))
        #x.append(mark_safe('EU NAO ENTENDO  \&nbsp; &nbsp; &nbsp; &nbsp;DE NOVO'))
        #print(l)

    

    return render(request, 'producao/rpt.html', {'data': r.linhas})
    #return response












def rpt_op_old(request, id):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="My Users.pdf"'
    buffer = BytesIO()

    op = OP.objects.get(id=id)
    r = MeuReport()
    #rel = []
    #l = str(campo('Código', 15)) +  campo('Descrição', 60) +  campo('Quantidade', 10 + campo('Unid.', 4))

    r.linha(r.campo('Número OP: ', 15, 'r') +  r.campo(op.num, 20, 'l') +  r.campo('Data emissão: ', 15, 'r') + r.campo(op.data_emissao, 4, 'l'))
    r.linha(r.campo('Código: ', 15, 'r') +  r.campo(op.produto.cod, 20, 'l') +  r.campo('Descrição: ', 15, 'r') + r.campo(op.produto.desc, 60, 'l'))
    r.linha(r.campo('Qtd. a produzir: ', 15, 'r') + r.campo(op.qtd_programada, 20, 'l') + r.campo('Unidade: ', 15, 'r') + r.campo(op.produto.unid.unid, 10, 'l')  )
    #r.linha(r.campo('Qtd. equivalente: ', 15, 'r') + r.campo(op.qtd_programada, 20, 'l') + r.campo('Unidade: ', 15, 'r') + r.campo(op.produto.unid2.unid, 10, 'l')  )
    r.linha(r.campo('.', 10, 'b'))
    r.linha(r.campo('-', 110, 'b'))
    r.linha(r.campo('.', 10, 'b'))
    r.linha(r.campo('COMPOSIÇÃO', 110, 'C'))
    r.linha(r.campo('.', 10, 'b'))
    r.linha(r.campo('-', 110, 'f'))
    r.linha(r.campo('Código', 15, 'c') +  r.campo('Descrição', 60, 'c') +  r.campo('Qtd.', 10, 'c') + r.campo('Unid.', 4, 'c'))
    r.sub_head('composição', 110)

    for n in op.op_comp_fis.all():
        #r.linha(r.campo(op.op_comp_fis.produto.cod, 15, 'l') +  r.campo(op.op_comp_fis.produto.desc, 60, 'l') +  r.campo('Qtd.', 10, 'l') + r.campo('Unid.', 4, 'l'))
        r.linha(r.campo(' ', 15 , 'f') + r.campo('Qtd2', 10, 'l') + r.campo('Unid2', 10, 'l')  )
        #r.linha(r.campo(op.op_comp_fis.produto), 40, 'l')

    #response.write(r.show(buffer))

    meuKwarg = {}
    meuKwarg['titulo'] = 'meu titulo'
    meuKwarg['left_footer'] = 'meu footer'
    meuKwarg['dados'] = r.linhas

    rep = MyReport(buffer, **meuKwarg)
    pdf = rep.generateReport()
   
    response.write(pdf)
    return response


'''

def rpt_op(request):
    # Set up response
    from django.http import FileResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="My Users.pdf"'
    # buffer
    buff = BytesIO()
    # Create the pdf object
    p = canvas.Canvas(buff, pagesize=A4)
    
    #print(A4)
    #print('larg: %s - alt: %s' ) % str(larg), str(alt)

    # Add some elements... then


    #conteudo(p)

    c = Rpt_op_class(p)
    c.relatorio()
    
    p.showPage()
    p.save()

    # Get the pdf from the buffer and return the response
    pdf = buff.getvalue()
    buff.close()
    response.write(pdf)
    return response'''


def conteudo(canvas):
    p = canvas
    larg, alt = A4
    #conteúdo
    ##dados da página
    titulo = 'Ordem de produção'
    tm = 10 * mm
    bm = 10 * mm
    lm = 10 * mm
    rm = 10 * mm
    empresa = 'Defer Indústria Metalúrgica'
    cnpj = '04.408.568/0001-05'
    relatorio = 'rpt_op'


    p.setFont('Helvetica', 8)
    p.setTitle(titulo)
    
    #header
    #grid
    hh = 15  * mm #altura do cabeçalho
    th = alt - tm
    bh = th - hh
    larg = larg - lm -rm
    alt = alt - tm - bm
    div1 = lm + 40 * mm
    div2 = lm + larg - 40 * mm
    p.line(lm, th, larg + lm, th )
    p.line(lm, bh, larg + lm, bh )
    p.line(div1, th, div1, bh )
    p.line(div2, th, div2, bh )
    #texto
    l1 = th - 11
    l2 = l1 - 10
    l3 = l2 - 10
    centro = larg / 2 + lm

    px = div2 + 5
    py = l3
    print(px)
    print(py)

    p.drawString(lm , l1, empresa)
    p.drawString(lm , l2, cnpj)
    p.drawString(lm , l3, relatorio)
    
    #div da data
    time = datetime.datetime.today()
    date = time.strftime("Data: %d/%m/%Y")
    hora = time.strftime("Hora: %H:%M:%S")
    p.drawString(div2 + 5, l1, date)
    p.drawString(div2 + 5, l2, hora)

    #div do titulo
    p.setFont('Helvetica', 14)
    p.drawString(div1 + 10, l2, 'Relatório de produtos')



def op_list(request):
    ops = OP.objects.all()
    #table = PedidosTable(orc)
    #table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'producao/op_list.html', {'lista': ops})