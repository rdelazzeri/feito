import fdb
conn = fdb.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey')
cur = conn.cursor()
cur.execute("select DESCRICAO from ACEC1101")
print(cur)
for c in cur:
    print(c[0])
conn.close()
