#!C:\Users\alexs\AppData\Local\Programs\Python\Python37\python.exe
#!/usr/bin/env python
import cgi, os, sys
os.environ['APPDATA']="C:/Users/alexs/AppData/Roaming"

iduser = str(sys.argv[1])

file = open("memory"+iduser+".json","r+")
file.truncate(0)
file.write('{"type": "", "nb_reponse": 0, "type_demande": "", "periode": ""}')
file.close()