from django.shortcuts import render
import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime
from decimal import *
from .models import CC, Conta


def cx_list(request):
    pass


def import_conta():
    df = pd.read_csv (r'c:\dados2.csv', delimiter=';')

    ct_list = df['CONTA'].unique()
    for ct in ct_list:
        print(ct)
        conta = Conta()
        conta.conta = ct
        conta.save()

    #print(ct)
    #for index, row in df.iterrows():
    # print(row["DESC"])


def import_dados():
    df = pd.read_csv (r'c:\dados2.csv', delimiter=';')

    cc = CC.objects.all().delete()
    for index, row in df.iterrows():
        conta = Conta.objects.filter(conta=row['CONTA'])
        data  = datetime.strptime(row['DATA'], '%d/%m/%Y')
        credito = Decimal(row['CREDITO'].replace(',', '.'))
        debito = Decimal(row['DEBITO'].replace(',', '.'))
        cc = CC()
        cc.data = data
        cc.desc = row['DESC']
        cc.banco = row['BANCO']
        cc.conta = conta[0]
        cc.credito = credito
        cc.debito = debito
        cc.save()


def to_pandas():
    df = pd.DataFrame(list(CC.objects.all().values('conta__conta', 'banco', 'credito', 'debito' )))
    print(df)

    table = pd.pivot_table(df, index=['conta__conta'], aggfunc={'credito': np.sum, 'debito': np.sum})
    print(table)
    table.to_excel("c:\django\output4.xlsx") 
    #table.to_csv('c:\django\output.csv', sep=';') 



#import_conta()
#import_dados()
#to_pandas()
