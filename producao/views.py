from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.forms import formset_factory
from io import BytesIO
from .rp_op import *
from .models import *
from .forms import *
from django.db import transaction



def op_list(request):
    pass



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

class report:
    #from django.http import FileResponse

    def __init__(self, *args, **kwargs):
        self.linhas = ()
        self.response = HttpResponse(content_type='application/pdf')
        self.response['Content-Disposition'] = 'inline; filename="My Users.pdf"'
        self.buffer = BytesIO()
    
    def linha(self, linha):
        self.linhas.append(linha)

    def campo(self, valor, tamanho, posicao):

        if posicao == 'l':
            str = str(valor)
            l = tamanho - len(str)
            campo = str + '&nbsp;' * l 
        elif posicao == 'r':
            str = str(valor)
            l = tamanho - len(str)
            campo = '&nbsp;' * l + str    
        elif posicao == 'c':
            str = str(valor)
            l = tamanho - len(str)
            campo = '&nbsp;' * (l/2) + str + '&nbsp;' * (l/2) 
        elif posicao == 'b':
            campo = '&nbsp;' * valor 
        elif posicao == 'f':
            str = str(valor)
            l = tamanho - len(str)
            campo = str + str * l
        else: 
            campo = 'erro'
        #self.linhas.append(campo)
        return campo

    def sub_head(self, titulo, tamanho):
            str = str(titulo)
            l = tamanho - len(str)
            self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('-', 110, 'b'))
            self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo(titulo, 110, 'C'))
            self.linha(self.campo('', 1, 'b'))
            self.linha(self.campo('-', 110, 'f'))

    def show(self):
        meuKwarg = {}
        meuKwarg['titulo'] = 'meu titulo'
        meuKwarg['left_footer'] = 'meu footer'
        meuKwarg['dados'] = self.linhas
        report = MyReport(self.buffer, **meuKwarg)
        # I can now specify my custom foot  er in runtime!
        pdf = report.generateReport()
        self.response.write(pdf)
        return self.response

def pdf(request):
    from django.http import FileResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="My Users.pdf"'
    buffer = BytesIO()

     
    prods = Prod.objects.filter(cod__startswith = '10')

    r = report()

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


    response.write(pdf)
    return response


def print_op(id):
    op = OP.objects.get(id=id)
    r = report()
    #rel = []
    #l = str(campo('Código', 15)) +  campo('Descrição', 60) +  campo('Quantidade', 10 + campo('Unid.', 4))

    r.linha(r.campo('Número OP: ', 15, 'r') +  r.campo(op.num, 20, 'l') +  r.campo('Data emissão: ', 15, 'r') + r.campo(op.data_emi, 4, 'l'))
    r.linha(r.campo('Código: ', 15, 'r') +  r.campo(op.produto.cod, 20, 'l') +  r.campo('Descrição: ', 15, 'r') + r.campo(op.produto.desc, 60, 'l'))
    r.linha(r.campo('Qtd. a produzir: ', 15, 'r') + r.campo(op.qtd, 20, 'l') + r.campo('Unidade: ', 15, 'r') + r.campo(op.produto.unid.unid, 10, 'l')  )
    r.linha(r.campo('Qtd. equivalente: ', 15, 'r') + r.campo(op.qtd2, 20, 'l') + r.campo('Unidade: ', 15, 'r') + r.campo(op.produto.unid2.unid, 10, 'l')  )
    r.linha(r.campo('', 1, 'b'))
    r.linha(r.campo('-', 110, 'b'))
    r.linha(r.campo('', 1, 'b'))
    r.linha(r.campo('COMPOSIÇÃO', 110, 'C'))
    r.linha(r.campo('', 1, 'b'))
    r.linha(r.campo('-', 110, 'f'))
    r.linha(r.campo('Código', 15, 'c') +  r.campo('Descrição', 60, 'c') +  r.campo('Qtd.', 10, 'c') + r.campo('Unid.', 4, 'c'))
    r.sub_head('composição')

    for n in op.op_comp_fis.all():
        r.linha(r.campo(op.op_comp_fis.produto.cod, 15, 'l') +  r.campo(op.op_comp_fis.produto.desc, 60, 'l') +  r.campo('Qtd.', 10, 'l') + r.campo('Unid.', 4, 'l'))
        r.linha(r.campo(' ',15) + r.campo('Qtd2', 10) + r.campo('Unid2')  )

    return r.show()



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
    return response


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