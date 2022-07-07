from decimal import Decimal
from comercial.models import Pedido
from prod.models import Prod, Prod_componente



class MRP:

    mrp_list = []

    def get_mrp_list(self):
        return list(self.mrp_list)

    def mrp_list_append(self, pedido, produto, qtd_necessaria):
        nl = []
        nl.append(pedido)
        nl.append(produto)
        nl.append(Decimal(qtd_necessaria))
        self.mrp_list.append(nl)

    def check_estoque_old(self, it):
        necessidade = Decimal(it.qtd_saldo) - Decimal(it.produto.qEstoque)
        return necessidade

    def check_estoque(self, produto, quantidade):
        necessidade = quantidade - produto.qEstoque
        return necessidade

    def produzir(self, pedido, produto, quantidade):
        for componente in produto.codigoProd.filter(codProd = produto):
            necessidade_bruta = Decimal(componente.qtd) * Decimal(quantidade)
            necessidade_producao = self.check_estoque(componente.codComp, necessidade_bruta)
            if necessidade_producao > 0:
                self.mrp_list_append(pedido, componente.codComp, necessidade_producao)
                print(componente.codComp, ' - a produzir: ', necessidade_producao)
                self.produzir(pedido, componente.codComp, necessidade_producao)
            else:
                print(componente.codComp, ' - ', necessidade_producao)

    def mrp(self, pedidos):
        for id in pedidos:
            pedido = Pedido.objects.get(id = id)
            print(f'pedido num: {pedido.num}')
            for it in pedido.itens.all():
                print(f'Pedido: {pedido.num} item: {it.produto.cod} - qtd: {it.qtd_saldo} - estoque: {it.produto.qEstoque}')
                necessidade = self.check_estoque(it.produto, it.qtd_saldo)
                if necessidade > 0:
                    self.mrp_list_append(pedido, it.produto, necessidade)
                    self.produzir(it.pedido, it.produto, necessidade)
        return self.mrp_list


    '''
    def custo_composto(prod, custo, n=0):
        qr = ProdComp.objects.filter(codProd=prod)
        for it in qr:
            print('>', it.id, ' - ', it.codComp.desc, ' - ', it.codComp.cmv, ' - ', custo)
            qr2 = ProdComp.objects.filter(codProd=it.codComp)
            if qr2.count() > 0:
                for it2 in qr2:
                    print('>>', it2.codComp.id, ' - ',  it2.codComp.desc, ' - ', it2.codComp.cmv, ' - ', custo)
                    custo = custo_composto(it2.codComp, custo, n+1) * it2.qtd
                    print(n+1)
            else:
                cmv = it.codComp.cmv if it.codComp.cmv else 0
                custo += (cmv * it.qtd)
                print('>>>', it.id, ' - ', it.codComp.desc, ' - ', custo)
        return custo'''