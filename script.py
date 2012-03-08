#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys
import os.path
import subprocess

ibold="\033[31m""\n===> "
ebold="\033[00m"
COS = "250mb"

def intro():
    print"""
    \033[1m 
    Utilidad de Importación/Exportación de cuentas en Zimbra.
    Opciones:
    1.- Exportar una cuenta.
    2.- Exportación masiva en función de tiempo de inactividad.
    3.- Importación de una cuenta.
    4.- Importación masiva.
    5.- Salir
    \033[0m
    """
    option = raw_input("Introduce Opción: ")
    try:
        option = int(option)
    except ValueError:
        print "No has introducido una opción válida"
        sys.exit()
    if option < 1 or option > 5:
        print "Opción no válida"
        sys.exit()
    return option


def user_import(mailbox):
    if ( str(os.path.exists('backup_'+mailbox+'_.tgz')) == "False" ):
        print ibold + "No se encuentra el backup de " + mailbox + " para su importación" + ebold
        sys.exit()
    if ( str(os.path.exists(mailbox+'.txt')) == "False" ):
        print ibold + "No se encuentra el archivo con la información " + mailbox + " para su importación" + ebold
        sys.exit()
    cmd = 'zmaccts | grep '+ mailbox + ' | cut -d " " -f1'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    out = p.communicate()[0]
    out = out[:-1]
    if out != mailbox:
        f = open(mailbox + '.txt')
        params = f.readline()
        displayName = str(params)[:-1]
        params = f.readline()
        givenName = str(params)[:-1]
        params = f.readline()
        snName = str(params)[:-1]
        params = f.readline()
        initials = str(params)[:-1]
        print "No existe el buzón, creándolo..."
        cmd = 'zmprov ca ' + mailbox + ' 1qasw2' +  ' zimbraCOSid ' + COS + ' displayName "' + displayName + '" givenName "' + givenName + '" sn "' + snName + '" initials "' + initials + '"'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
    else:
        print "El buzón a importar existe, se sobreescribirán los datos..."
        question = raw_input(ibold + "CONTINUAR??  (SI) " + ebold)
        if question != "SI":
            print "Cancelado"
            sys.exit() 
    cmd = 'ls -lh backup_' + mailbox + '_.tgz | cut -d " " -f 5'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    out = p.communicate()[0]
    out = out[:-1]
    print "Importando la cuenta " + mailbox + " con un tamaño de: "+ out
    cmd = 'zmmailbox -z -m ' + mailbox + ' postRestURL "//?fmt=tgz&resolve=reset"  backup_' + mailbox + '_.tgz'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    print "Cuenta Importada con éxito"
    sys.exit()


def user_import_massive():
    print "Buscando cuentas para importar en el directorio actual..."
    print "Si continuas se crearán las cuentas que no existan y sobrescribiran las que existan!!"
    question = raw_input(ibold + "PROCEDEMOS??  (SI) " + ebold)
    if question != "SI":
        print "Cancelado"
        sys.exit()
    cmd = 'ls -1 backup*.tgz'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    for mailbox in p.stdout.readlines():
        mailbox = mailbox[:-1]
        mailbox = mailbox.split("_")[1]
        cmd = 'zmaccts | grep '+ mailbox + ' | cut -d " " -f1'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()[0]
        out = out[:-1]
        if out != mailbox:
            f = open(mailbox + '.txt')
            params = f.readline()
            displayName = str(params)[:-1]
            params = f.readline()
            givenName = str(params)[:-1]
            params = f.readline()
            snName = str(params)[:-1]
            params = f.readline()
            initials = str(params)[:-1]
            print "No existe el buzón, creándolo..."
            cmd = 'zmprov ca ' + mailbox + ' 1qasw2' + ' zimbraCOSid ' + COS + ' displayName "' + displayName + '" givenName "' + givenName + '" sn "' + snName + '" initials "' + initials + '"'
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            p.wait()
        cmd = 'ls -lh backup_'+ mailbox +'_.tgz | cut -d " " -f 5'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()[0]
        out = out[:-1]
        print "Importando la cuenta " + mailbox + " con un tamaño de: " + out
        cmd = 'zmmailbox -z -m ' + mailbox + ' postRestURL "//?fmt=tgz&resolve=reset"  backup_' + mailbox + '_.tgz'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        print "Cuenta Importada con éxito"
        
    
def user_export_massive():
    inactivity_days = raw_input("Introduce días de inactividad: ")
    try:
        inactivity_days = int(inactivity_days)
    except ValueError:
        print ibold + "No has introducido una número de días válida" + ebold
        sys.exit()
    print "Si continuas se procederá a la importación de cuentas inactivas de más de " + str(inactivity_days) + " días"
    question = raw_input(ibold + "PROCEDEMOS??  (SI) " + ebold)
    if question != "SI":
        print "Cancelado"
        sys.exit()
    inactivity_seconds = inactivity_days * 86400
    cmd = 'date "+%s"'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    actual_date = p.communicate()[0]
    reference_date = int(actual_date) - inactivity_seconds
    f=open('data.out','w')
    cmd = 'zmaccts | grep /'
    p = subprocess.Popen(cmd, shell=True, stdout=f)
    p.wait()
    f.close()
    for line in file('data.out'):
        line = line[:-1]
        if line == "\n": break
        tmp = line.split()
        mailbox = tmp[0]
        active = tmp[1]
        creation_date = tmp[2]
        last_activity_date = tmp[4]
        if "wiki" in mailbox  or "galsync" in mailbox  or "ham" in mailbox or "spam" in mailbox  or "virus" in mailbox:
            print "Cuenta de sistema no se exporta: " + mailbox
        else:
            if last_activity_date == "never":
                cmd = 'date -d ' + creation_date + ' "+%s"'
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                p.wait()
                creation_date_seconds = p.communicate()[0]
                if reference_date > int(creation_date_seconds):
                    
                    cmd = 'zmmailbox -z -m ' + mailbox + ' gms'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    out = out[:-1]
                    print "Exportando la cuenta: " + mailbox + "de tamaño: " + out
                    cmd = 'zmmailbox -z -m ' + mailbox + ' getRestURL "//?fmt=tgz" > backup_' + mailbox + '_.tgz'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    # Exportación de los datos del LDAP de la cuenta.
                    f = open (mailbox + ".txt","w")
                    
                    cmd = 'zmlocalconfig -s zimbra_ldap_password | cut -d " " -f3'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    zimbraLdapPassword = out[:-1]
                    
                    cmd = 'zmlocalconfig -s ldap_master_url | cut -d " " -f3'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    ldapMasterUrl = out[:-1]   
                    
                    cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" | grep displayName: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    displayName = out[:-1]
                    f.write(displayName+'\n')
                    
                    cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" |  grep givenName: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    givenName = out[:-1]
                    f.write(givenName+'\n')
         
                    cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" | grep sn: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    snName = out[:-1]
                    f.write(snName+'\n')
                    
                    cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" | grep initials: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    initials = out[:-1]
                    f.write(initials+'\n') 
                    
                    f.close()
                    print "Cuenta exportada con éxito"
                else:
                    print "No exportamos la cuenta: " + mailbox
            else:
                cmd = 'date -d ' + last_activity_date + ' "+%s"'
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                p.wait()
                last_activity_seconds = p.communicate()[0]
                if reference_date > int(last_activity_seconds):
                    cmd = 'zmmailbox -z -m ' + mailbox + ' gms'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    out = p.communicate()[0]
                    out = out[:-1]
                    print "Exportando la cuenta: " + mailbox + "de tamaño: " + out
                    cmd = 'zmmailbox -z -m ' + mailbox + ' getRestURL "//?fmt=tgz" > backup_' + mailbox + '_.tgz'
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    print "Cuenta exportada con éxito"
                else:
                    print "No exportamos la cuenta: " + mailbox

def user_export(mailbox):
    print "Iniciando el proceso de exportación de la cuenta "+mailbox+"..."
    question = raw_input(ibold + "CONTINUAR??  (SI) " + ebold)
    if question != "SI":
        print "Cancelado"
        sys.exit()
    cmd = 'zmaccts | grep ' + mailbox + ' | cut -d " " -f1'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    out = p.communicate()[0]
    out = out[:-1]
    if out != mailbox:
        print ibold + "No existe el buzón, saliendo..." + ebold
        sys.exit()
    else:
         cmd = 'zmmailbox -z -m ' + mailbox + ' gms'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         out = out[:-1]
         print "Exportando el buzón " + mailbox + " con un tamaño de " + out
         cmd = 'zmmailbox -z -m ' + mailbox + ' getRestURL "//?fmt=tgz" > backup_' + mailbox + '_.tgz'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         # Exportación de los datos del LDAP de la cuenta.
         f = open (mailbox + ".txt","w")
         
         cmd = 'zmlocalconfig -s zimbra_ldap_password | cut -d " " -f3'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         zimbraLdapPassword = out[:-1]
         
         cmd = 'zmlocalconfig -s ldap_master_url | cut -d " " -f3'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         ldapMasterUrl = out[:-1]   
        
         cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" | grep displayName: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         displayName = out[:-1]
         f.write(displayName+'\n')
         
         cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" |  grep givenName: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         givenName = out[:-1]
         f.write(givenName+'\n')
         
         cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" | grep sn: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         snName = out[:-1]
         f.write(snName+'\n')
         
         cmd = '/opt/zimbra/bin/ldapsearch -H' + ldapMasterUrl + ' -w ' + zimbraLdapPassword  + ' -D uid=zimbra,cn=admins,cn=zimbra -x "(&(objectClass=zimbraAccount)(mail=' + mailbox + '))" | grep initials: | cut -d ":" -f2 | sed "s/^ *//g" | sed "s/ *$//g"'
         p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
         p.wait()
         out = p.communicate()[0]
         initials = out[:-1]
         f.write(initials+'\n')
           
         f.close()
         print "Cuenta exportada con éxito"
         sys.exit()

def read_mailbox():
    mailbox = raw_input("Introduce el nombre de la cuenta: ")
    if mailbox.find("@") == -1:
        print ibold + "Nombre de cuenta nó válido. Cancelado" + ebold
        sys.exit()
    return mailbox

print "Iniciando...."
option=intro()
if option == 1:
    print " Se va a proceder a la EXPORTACIÓN. "
    mailbox = read_mailbox()
    user_export(mailbox)
elif option == 2:
    print " Se va a proceder a una EXPORTACIÓN masiva de cuentas. "
    user_export_massive()
elif option == 3:
    print " Se va a proceder a la IMPORTACIÓN. "
    mailbox = read_mailbox()
    user_import(mailbox)
elif option == 4:
    print " Se va a proceder a la IMPORTACIÓN masiva de cuentas. "
    user_import_massive()
elif option == 5:
    print " Cancelado a petición del usuario."
    sys.exit()
else:
    print "Opción incorrecta...Cancelado"
    sys.exit()

