import firebirdsql
conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
cur = conn.cursor()
cur.execute("select DESCRICAO from ACEC1101")
print(cur)
n=0
for c in cur:
    n = n + 1
    print(c[0] + ' - ' + str(n))
conn.close()







