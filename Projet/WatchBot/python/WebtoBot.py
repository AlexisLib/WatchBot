#!C:\Users\alexs\AppData\Local\Programs\Python\Python37\python.exe
import cgi, os, pymysql, datetime
os.environ['APPDATA']="C:/Users/alexs/AppData/Roaming"
os.environ['HOME'] = 'C:/Python'
from Watchbot_response import *

print('content-type:text/html\r\n\r\n')

# Get data from HTML
form=cgi.FieldStorage()
iduser=int(form.getvalue('iduser'))
text=str(form.getvalue('text')).replace("'", "&apos;")
gender=form.getvalue('gender')

#Redirect
print('<html>')
print('<head>')
print('<meta http-equiv="refresh" content="0;url=.."/>')
print('</head>')
print('</html>')

#PARAM HUMAN
if gender == "male":
	avatar="images/avatar.png"
else:
	avatar="images/female.png"
status="human"
date = datetime.now()
date = date.strftime("%H:%M, %d/%m/%y")

#Connect and insert to DB
conn = pymysql.connect(host="localhost", user="root", passwd="", db="watchbot", charset='utf8')
myCursor = conn.cursor()
myCursor.execute("INSERT INTO chat(id, avatar, iduser, text, img, status, date) VALUES(null, '%s', '%i', '%s', null, '%s', '%s');"% (avatar, iduser, text, status, date))
conn.commit()
conn.close()

textbot = nlp_watchbot(text,iduser).replace("'", "&apos;")

#PARAM BOT
avatar="images/bot.png"
status="bot"
date = datetime.now()
date = date.strftime("%H:%M, %d/%m/%y")

#Connect and insert to DB
if "IMG:" in textbot:
	img = "python/"+textbot.split(":",1)[1]
	conn = pymysql.connect(host="localhost", user="root", passwd="", db="watchbot")
	myCursor = conn.cursor()
	myCursor.execute("INSERT INTO chat(id, avatar, iduser, text, img, status, date) VALUES(null, '%s', '%i', '%s', '%s', '%s', '%s');"% (avatar, iduser, textbot, img, status, date))
	conn.commit()
	conn.close()
else:
	conn = pymysql.connect(host="localhost", user="root", passwd="", db="watchbot")
	myCursor = conn.cursor()
	myCursor.execute("INSERT INTO chat(id, avatar, iduser, text, img, status, date) VALUES(null, '%s', '%i', '%s', null, '%s', '%s');"% (avatar, iduser, textbot, status, date))
	conn.commit()
	conn.close()