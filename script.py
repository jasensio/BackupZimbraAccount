#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys
import os.path
import subprocess.Popen

def intro():
    print"""
    Utilidad de Importación/Exportación de cuentas en Zimbra.
    Opciones:
    1.- Exportar una cuenta.
    2.- Exportación masiva en función de tiempo de inactividad.
    3.- Importación de una cuenta.
    4.- Importaación masiva.
    5.- Salir
    """
    option = raw_input("Introduce Opción: ")
    try:
        option = int(option)
    except ValueError:
        print "No has introducido una opcón válida"
        sys.exit()
    if option < 1 or option > 5:
        print "Opción no válida"
        sys.exit()
    return option

def user_import(mailbox):
    if ( os.path.exists('backup_'+mailbox+'_.tgz') == "False" ):
        print "No se encuentra el backup de "+mailbox+" para su importación"
        sys.exit()
    cmd = 'zmaccts | grep '+ mailbox + ' | cut -d " " -f1'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.communicate()
    if out != mailbox:
        print "No existe el buzón, creándolo..."
        cmd = 'zmprov ca ' + mailbox + ' 1qasw2'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    else:
        print "El buzón a importar existe, se sobreescribirán los datos..."
        question = raw_input("CONTINUAR??  (SI)")
        if question != "SI":
            print "Cancelado"
            sys.exit()
    cmd = 'ls -lh backup_'+mailbox+'_.tgz | cut -d " " -f 5'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = p.communicate()
    print "Importando la cuenta "+mailbox+" con un tamaño de: "+out+" MB"
    cmd = 'zmmailbox -z -m '+mailbox+' postRestURL "//?fmt=tgz&resolve=reset"  backup'+mailbox+'_.tgz'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print "Cuenta Importada con éxito"
    sys.exit()

def user_export(mailbox):
    print "Iniciando el proceso de importación de la cuenta "+mailbox+"..."



print "Iniciando...."
option=intro()
print "La opción elegida es: " + str(option)
