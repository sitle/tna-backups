from fabric.api import *

env.hosts = ['srv1.tna.pf']

def filebackup():
    sudo('cd /var/backups/fabric/files && tar -cvzf www.tna.pf.tar.gz /var/www/www.tna.pf')
    sudo('cd /var/backups/fabric/files && tar -cvzf doc.tna.pf.tar.gz /var/www/doc.tna.pf')

def mysqldump(user, password, database):
    sudo('mysqldump -u %s -p%s %s > %s.sql' %(user, password, database, database))

def dbdump(user,password):
    with cd('/var/backups/fabric/db'):
        mysqldump(user, password, 'wwwtnapf')
        mysqldump(user, password, 'mediawiki')
        mysqldump(user, password, 'mumble')
        mysqldump(user, password, 'archivetnapf')

def slapdump():
    sudo ('cd /var/backups/fabric/db && slapcat > annuaire.ldif')

def dbbackup(password):
    dbdump(password)
    slapdump()
    filebackup()
    sudo ('cd /var/backups/fabric/db && rm *.bz2 && bzip2 *')
    get('/var/backups/fabric/db/*', 'databases/')
    get('/var/backups/fabric/files/*', 'files/')
