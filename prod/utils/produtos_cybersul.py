import firebirdsql
conn = firebirdsql.connect(
    dsn='localhost:/cybersul/banco/dadosadm.fdb', 
    user='sysdba', 
    password='masterkey',
    dialect='1'
    )
cur = conn.cursor()
cur.execute("select CODIGO_CLIENTE from AUGC0301")
print(cur)
n=0
for c in cur.fetchall():
    n= n+1
    #print(c + ' - ' + str(n))
    print (n) 

conn.close()



