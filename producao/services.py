from decimal import Decimal
from comercial.models import Pedido
from prod.models import Prod, Prod_componente



class MRP:

    mrp_list = []

    def get_mrp_list(self):
        return self.mrp_list

    def clean_mrp_list(self):
        self.mrp_list.clear()

    def mrp_list_append(self, pedido, produto, necessidade, disponivel, produzir):
        nl = {}
        nl['ped_num'] = pedido.num
        nl['ped_id'] = pedido.id
        nl['prod_id'] = produto.id
        nl['prod_cod'] = produto.cod
        nl['prod_desc'] = produto.desc
        nl['necessario'] = float(f'{necessidade:.2f}')
        nl['disponivel'] = float(f'{disponivel:.2f}')
        nl['produzir'] = float(f'{produzir:.2f}')
        self.mrp_list.append(nl)

    def check_estoque_old(self, it):
        necessidade = Decimal(it.qtd_saldo) - Decimal(it.produto.qEstoque)
        return necessidade


    def check_estoque(self, produto):
        disponivel = Decimal(produto.qEstoque)
        return disponivel


    def qtd_produzir(self, produto, disponivel, necessidade):
        a_produzir =  necessidade - disponivel
        return a_produzir

    def controlado_mrp(self, produto):
        if 'SERVICO' in produto.grupo.desc or 'POLIMENTO' in produto.grupo.desc:
            print(produto.grupo.desc)
            return False
        else:
            print(produto.grupo.desc)
            return True

    def produzir(self, pedido, produto, quantidade):
        for componente in produto.codigoProd.filter(codProd = produto):
            if self.controlado_mrp(componente.codComp): 
                necessidade_bruta = Decimal(componente.qtd) * Decimal(quantidade)
                disponivel = self.check_estoque(componente.codComp)
                qtd_produzir = self.qtd_produzir(componente.codComp, disponivel, necessidade_bruta)
                if qtd_produzir > 0:
                    self.mrp_list_append(pedido, componente.codComp, necessidade_bruta, disponivel, qtd_produzir)
                    print(componente.codComp, ' - a produzir: ', qtd_produzir)
                    self.produzir(pedido, componente.codComp, qtd_produzir)
                else:
                    self.mrp_list_append(pedido, componente.codComp, necessidade_bruta, disponivel, 0)

    def mrp(self, pedidos):
        self.clean_mrp_list()
        for id in pedidos:
            pedido = Pedido.objects.get(id = id)
            print(f'pedido num: {pedido.num}')
            for it in pedido.itens.all():
                necessidade = it.qtd_saldo
                disponivel = self.check_estoque(it.produto)
                qtd_produzir = necessidade - disponivel
                print(f'Pedido: {pedido.num} item: {it.produto.cod} - necessidade: {necessidade} - disponivel: {disponivel} - a produzir: {qtd_produzir}')
                if qtd_produzir > 0:
                    self.mrp_list_append(pedido, it.produto, necessidade, disponivel, qtd_produzir)
                    self.produzir(it.pedido, it.produto, qtd_produzir)
                else:
                    self.mrp_list_append(pedido, it.produto, necessidade, disponivel, 0)
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