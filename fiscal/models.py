from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey, OneToOneField

from comercial.models import Entrega

# Create your models here.

class Pre_nota_last_num(models.Model):
    num = models.IntegerField(default=0)

AMBIENTE_OPCOES = (
    ('1','PRODUCAO'),
    ('2','HOMOLOGACÃO'),
)

class NF_config(models.Model):
    last_num = models.IntegerField(default=0)
    ambiente = models.CharField(max_length=1, choices = AMBIENTE_OPCOES, default=2, null=True, blank=True)
    url_notificacao = models.CharField(max_length=80, null=True, blank=True)
    aliq_credito_simples = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    consumer_key = models.CharField(max_length=60, null=True, blank=True)
    consumer_secret = models.CharField(max_length=60, null=True, blank=True)
    access_token = models.CharField(max_length=60, null=True, blank=True)
    access_token_secret = models.CharField(max_length=60, null=True, blank=True)

class Pre_nota(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=CASCADE, related_name='nfe')
    num_nf = models.IntegerField(default=0)
    operacao = models.CharField(max_length=1, null=True, blank=True)
    natureza_operacao = models.CharField(max_length=60, null=True, blank=True)
    modelo = models.CharField(max_length=1, null=True, blank=True)
    finalidade = models.CharField(max_length=1, null=True, blank=True)
    ambiente = models.CharField(max_length=1, choices = AMBIENTE_OPCOES, default=1, null=True, blank=True)
    url_notificacao = models.CharField(max_length=80, null=True, blank=True)


class Pre_nota_cliente(models.Model):
    pre_nota = models.OneToOneField(Pre_nota, on_delete=CASCADE, related_name='cliente')
    cpf = models.CharField(max_length=11, null=True, blank=True)
    nome_completo = models.CharField(max_length=60, null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    razao_social = models.CharField(max_length=60, null=True, blank=True)
    ie = models.CharField(max_length=14, null=True, blank=True)
    suframa = models.CharField(max_length=9, null=True, blank=True)
    substituto_tributario = models.CharField(max_length=14, null=True, blank=True)
    consumidor_final = models.CharField(max_length=1, null=True, blank=True)
    contribuinte = models.CharField(max_length=1, null=True, blank=True)
    microcervejaria = models.BooleanField(default=False)
    endereco = models.CharField(max_length=60, null=True, blank=True)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.CharField(max_length=60, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    telefone = models.CharField(max_length=14, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)


class Pre_nota_produtos(models.Model):
    pre_nota = models.ForeignKey(Pre_nota, on_delete=CASCADE, related_name='produtos')
    produto_id = models.IntegerField(null=True, blank=True)
    item = models.IntegerField(null=True, blank=True)
    nome = models.CharField(max_length=120, null=True, blank=True)
    codigo = models.CharField(max_length=60, null=True, blank=True)
    ncm = models.CharField(max_length=8, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)
    quantidade_tributavel = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)
    unidade = models.CharField(max_length=6, null=True, blank=True)
    unidade_tributavel = models.CharField(max_length=4, null=True, blank=True)
    peso = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    origem = models.CharField(max_length=1, null=True, blank=True)
    desconto = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)
    subtotal_tributavel = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)
    total = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    classe_imposto = models.CharField(max_length=15, null=True, blank=True)
    cest = models.CharField(max_length=15, null=True, blank=True)
    beneficio_fiscal = models.CharField(max_length=8, null=True, blank=True)
    informacoes_adicionais = models.TextField(max_length=500, null=True, blank=True)
    gtin = models.CharField(max_length=14, null=True, blank=True)
    gtin_tributavel = models.CharField(max_length=14, null=True, blank=True)
    cod_barras = models.CharField(max_length=30, null=True, blank=True)
    cod_barras_tributavel = models.CharField(max_length=14, null=True, blank=True)
    nve = models.CharField(max_length=6, null=True, blank=True)
    nrecopi = models.CharField(max_length=20, null=True, blank=True)
    ativo_permanente = models.BooleanField(default=False)
    veiculo_usado = models.CharField(max_length=14, null=True, blank=True)
    ex_ipi = models.CharField(max_length=3, null=True, blank=True)
    classe_imposto = models.CharField(max_length=15, null=True, blank=True)

class Pre_nota_impostos(models.Model):
    Pre_nota_produtos = OneToOneField(Pre_nota_produtos, on_delete=CASCADE, related_name='impostos')

class Pre_nota_ICMS(models.Model):
    pre_nota_produtos = OneToOneField(Pre_nota_produtos, on_delete=CASCADE, related_name='icms')
    #ICMS para Simples Nacional
    aliquota = models.CharField(max_length=4, null=True, blank=True)
    codigo_cfop = models.CharField(max_length=4, null=True, blank=True)
    situacao_tributaria = models.CharField(max_length=3, null=True, blank=True)
    aliquota_importacao = models.CharField(max_length=4, null=True, blank=True)
    industria = models.CharField(max_length=1, null=True, blank=True)
    majoracao = models.CharField(max_length=13, null=True, blank=True)
    #ICMS101
    aliquota_credito = models.CharField(max_length=4, null=True, blank=True)

class Pre_nota_IPI(models.Model):
    pre_nota_produtos = OneToOneField(Pre_nota_produtos, on_delete=CASCADE, related_name='ipi')
    situacao_tributaria = models.CharField(max_length=3, null=True, blank=True)
    codigo_enquadramento = models.CharField(max_length=3, null=True, blank=True)
    aliquota = models.CharField(max_length=4, null=True, blank=True)

class Pre_nota_PIS(models.Model):
    pre_nota_produtos = OneToOneField(Pre_nota_produtos, on_delete=CASCADE, related_name='pis')
    situacao_tributaria = models.CharField(max_length=3, null=True, blank=True)
    aliquota = models.CharField(max_length=4, null=True, blank=True)

class Pre_nota_COFINS(models.Model):
    pre_nota_produtos = OneToOneField(Pre_nota_produtos, on_delete=CASCADE, related_name='cofins')
    situacao_tributaria = models.CharField(max_length=3, null=True, blank=True)
    aliquota = models.CharField(max_length=4, null=True, blank=True)

class Pre_nota_pedido(models.Model):
    pre_nota = models.OneToOneField(Pre_nota, on_delete=CASCADE, related_name='pedido')
    presenca = models.CharField(max_length=1, null=True, blank=True)
    intermediador = models.CharField(max_length=1, null=True, blank=True)
    cnpj_intermediador = models.CharField(max_length=14, null=True, blank=True)
    id_intermediador = models.CharField(max_length=60, null=True, blank=True)
    modalidade_frete = models.CharField(max_length=1, null=True, blank=True)
    frete = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    despesas_acessorias = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    despesas_aduaneiras = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    informacoes_fisco = models.TextField(max_length=2000, null=True, blank=True)
    informacoes_complementares = models.TextField(max_length=2000, null=True, blank=True)
    observacoes_contribuinte = models.TextField(max_length=2000, null=True, blank=True)
    #Informações de pagamento
    pagamento = models.CharField(max_length=1, null=True, blank=True)
    forma_pagamento = models.CharField(max_length=2, null=True, blank=True)
    desc_pagamento = models.CharField(max_length=40, null=True, blank=True)
    tipo_integracao = models.CharField(max_length=1, default=2)
    valor_pagamento = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cnpj_credenciadora = models.CharField(max_length=14, null=True, blank=True)
    bandeira = models.CharField(max_length=2, null=True, blank=True)
    autorizacao = models.CharField(max_length=20, null=True, blank=True)

class Pre_nota_transporte(models.Model):
    pre_nota = models.OneToOneField(Pre_nota, on_delete=CASCADE, related_name='transporte')
    volume = models.CharField(max_length=15, null=True, blank=True)
    peso_bruto = models.CharField(max_length=15, null=True, blank=True)
    peso_liquido = models.CharField(max_length=15, null=True, blank=True)
    marca = models.CharField(max_length=15, null=True, blank=True)
    numeracao = models.CharField(max_length=15, null=True, blank=True)
    lacres = models.CharField(max_length=15, null=True, blank=True)
    #Dados da transportadora
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    razao_social = models.CharField(max_length=60, blank=True, null=True)
    ie = models.CharField(max_length=14, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    nome_completo = models.CharField(max_length=60, blank=True, null=True)
    endereco = models.CharField(max_length=60, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cidade = models.CharField(max_length=60, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    placa = models.CharField(max_length=7, blank=True, null=True)
    uf_veiculo = models.CharField(max_length=2, blank=True, null=True)
    rntc = models.CharField(max_length=14, blank=True, null=True)
    seguro = models.CharField(max_length=14, blank=True, null=True)

class Pre_nota_entrega(models.Model):
    pre_nota = OneToOneField(Pre_nota, on_delete=CASCADE, related_name='local_entrega')
    cpf = models.CharField(max_length=11, null=True, blank=True)
    nome_completo = models.CharField(max_length=60, null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    razao_social = models.CharField(max_length=60, null=True, blank=True)
    ie = models.CharField(max_length=14, null=True, blank=True)
    endereco = models.CharField(max_length=60, null=True, blank=True)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.CharField(max_length=60, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    telefone = models.CharField(max_length=14, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)

class Pre_nota_fatura(models.Model):
    pre_nota = OneToOneField(Pre_nota, on_delete=CASCADE, related_name='fatura')
    numero = models.CharField(max_length=14, blank=True, null=True)
    valor = models.CharField(max_length=14, blank=True, null=True)
    desconto = models.CharField(max_length=14, blank=True, null=True)
    valor_liquido = models.CharField(max_length=14, blank=True, null=True)
 
class Pre_nota_parcelas(models.Model):
    pre_nota = ForeignKey(Pre_nota, on_delete=CASCADE, related_name='parcelas')
    vencimento = models.CharField(max_length=10, blank=True, null=True)
    valor = models.CharField(max_length=14, blank=True, null=True)


class NFe_transmissao(models.Model):
    #remessa
    pre_nota = ForeignKey(Pre_nota, on_delete=CASCADE, related_name='retorno')
    num_nf = models.PositiveIntegerField(default=0)
    nfe_json = models.TextField(max_length=50000, null=True, blank=True)
    #retorno
    error = models.CharField(max_length=300, null=True, blank=True)
    uuid = models.CharField(max_length=100, null=True, blank=True)
    nfe = models.CharField(max_length=20, null=True, blank=True)
    serie = models.CharField(max_length=3, null=True, blank=True)
    status = models.CharField(max_length=40, null=True, blank=True)
    motivo = models.CharField(max_length=60, null=True, blank=True)
    recibo = models.CharField(max_length=100, null=True, blank=True)
    chave = models.CharField(max_length=60, null=True, blank=True)
    modelo = models.CharField(max_length=4, null=True, blank=True)
    log = models.TextField(max_length=1000, null=True, blank=True)
    xml = models.URLField(max_length=300, null=True, blank=True)
    danfe = models.URLField(max_length=300, null=True, blank=True)
    danfe_simples = models.URLField(max_length=300, null=True, blank=True)
    

    def erro(self):
        if self.status == 'aprovado':
            return False
        else:
            return True
    








