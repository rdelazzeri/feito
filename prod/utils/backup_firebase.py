
'''
C:\Program Files (x86)\Firebird\Firebird_1_5\bin\gbak
c:\dadosadm.fbk
c:\django.fdb

gbak –user SYSDBA –pas masterkey –r –p 4096 -o c:\dadosadm.fbk c:\dados.fdb

restore que funcionou:
gbak -user SYSDBA -pas masterkey -r -o c:\dadosadm.fbk localhost:c:\dados.fdb

verificaçao de erros
gfix -v -f localhost:c:\dados.fdb -user sysdba -pass masterkey

corrigir a base
gfix -m -i localhost:c:\dados.fdb -user sysdba -pass masterkey

'''
