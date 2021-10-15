#!C:\Users\alexs\AppData\Local\Programs\Python\Python37\python.exe
import os
os.environ['APPDATA']="C:/Users/alexs/AppData/Roaming"

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import re
from tensorflow import keras
#from keras.models import load_model
model = keras.models.load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.txt').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
from Traitement_Data import generate_stats

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    nb = 0
    for s in sentence_words:
        for i,word in enumerate(words):
            word = lemmatizer.lemmatize(word.lower())
            if word == s: 
                nb +=1
                bag[i] = 1
    if nb == 0:
        return "Error"
    return(np.array(bag))


def predict_class(sentence,nb_user):
    return_list = []
    p = bag_of_words(sentence, words)
    
    # If anyone word is recognize :
    if p == "Error":
        return_list.append("erreur")
        return return_list
       
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.2
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # Meilleur probabilité
    results.sort(key=lambda x: x[1], reverse=True)
    liste_process = ['VMA','heartbeat','temperature','steps',"blood_pressure","calories","IMC"]
    for r in results:
        if classes[r[0]] in liste_process :
            details = {"type":classes[r[0]],"nb_reponse":0,"type_demande":[],"periode":[]}
            with open("memory"+str(nb_user)+".json", 'w') as json_file:
                json.dump(details, json_file)
            return 0
        return_list.append(classes[r[0]])
    return return_list


def getResponse(tag, intents_json, nb_rep = -1):
    list_of_intents = intents_json['intents']
    if type(tag) == list:
        tag = tag[0]
    for i in list_of_intents:
        if(i['tag'] == tag):
            if nb_rep > -1:
                try :
                    result = i['responses'][nb_rep]
                    break
                except :
                    result = "END"
                    break
            result = random.choice(i['responses'])
            break
    return result

import re
from datetime import datetime

def clear_text(x):
    x = x.lower()
    x = x.replace('_','')
    x = x.replace(" ","")
    mois = {'janvier':'01','février':'02','fevrier':'02','mars':'03','avril':'04','mai':'05','juin':'06',
            'juillet':'07','août':'08','aout':'08','septembre':'09','octobre':'10','novembre':'11',
            'décembre':'12'}
    
    for m,nb in mois.items():
        x = x.replace(m,"-"+nb)
    # Aujourd'hui 
    auj = ["aujourd'hui","date du jour","maintenant"]
    now = datetime.now()
    date_now = now.strftime("%d/%m/%Y %H:%M")
    
    for ex in auj:
        x = x.replace(ex,date_now)
    return x

def verif_date(date):    
    if len(date) == 5:
        date = date[0:5] + "-2021"
    else:
        pos = date.rfind("-")+3
        date = date[0:pos]+"-"+date[pos:]
        if len(date) == 8:
            date = date[0:6] + "20" + date[6:8]

    return date

def verif_horaire(h):
    if len(h) == 3:
        h = h+"00"
    return h
    
def recup_date(text):
    if text == "END" :
        return text
    try:
        text = clear_text(text)
        # Récupération Horaire
        horaire = re.findall("\d{1,2}[:h]\d{0,2}",text)
        if len(horaire) !=2:
            return 0
        
        horaire1 = horaire[0].replace("h",":")
        horaire2 = horaire[1].replace("h",":")
        horaire1 = verif_horaire(horaire1)
        horaire2 = verif_horaire(horaire2)
        
        # On supprime l'horaire du texte pour éviter les erreurs de mélange
        for h in horaire:
            text = text.replace(h,"")
        
        # Récupération date
        date = re.findall("\d{2}[-/]\d{2}\d{0,4}",text)
        
        if len(date) < 2:
            date2 = re.findall("\d{1}[-/]\d{2}\d{0,4}",text)
            for i in range(len(date2)):
                date2[i] = date2[i].replace(" ","")
                date2[i] = "0"+date2[i]
                date.append(date2[i])
            date = [d.replace(" ","") for d in date]
            date = sorted(date, key=lambda x: datetime.strptime(x, '%d-%m'))   
            if len(date) !=2:
                return 0
        date1 = date[0].replace("/","-")
        date2 = date[1].replace("/","-")
        date1 = verif_date(date1)
        date2 = verif_date(date2)
        
        
        
        date_finale = date1+" "+horaire1+"_"+date2+" "+horaire2

        if len(date_finale) == 33:
            return date_finale
    except: return 0
    else:
        return 0

def recup_type(text,demande_preli = 0):
    text = text.lower()
    fixe = ["fixe"]
    moyenne = ["moyenne"]
    evolution_moy = ["moyenne","evolution","évolution","graphique","graphe","moyens"]
    evolution_fixe = ['fixe',"evolution","évolution","graphique","graphe"]
    scores = {"number": 0,"average": 0, "evolution_average" : 0,"evolution_number": 0}
    if fixe[0] in text: scores['number'] = 1
    if moyenne[0] in text : scores['average'] = 1
    for elem in evolution_moy:
        if elem in text:
            if elem == 'moyenne': scores['evolution_average'] +=0.5
            else: scores['evolution_average'] +=1
    for elem in evolution_fixe:
        if elem in text:
            if elem == 'fixe': scores['evolution_number'] +=0.5
            else : scores['evolution_number'] +=1
    
    types = []
    best_score = max([ scores[s] for s in scores])
    for s in scores:
        if scores[s] == best_score:
            types.append(s)
    if(len(types) > 0):
        if demande_preli == 1:
            if len(types) > 2:
                return 0
        return types
    else : return 0
    
    
def nlp_watchbot(msg,nb_user):
    tag = 1
    if msg != '':
        with open("memory"+str(nb_user)+".json") as json_data:
            details = json.load(json_data)
        
        try:
            # Si aucune demande n'est en cours
            if details["type"] == "":
                tag = predict_class(msg,nb_user)
                # Si on détecte une demande
                if tag == 0:
                    with open("memory"+str(nb_user)+".json") as json_data:
                        details = json.load(json_data)

                    res = getResponse(details['type'],intents,details['nb_reponse'])
                    details['nb_reponse'] +=1
                    
                    # On vérifie qu'une date n'est pas déjà présente
                    date = recup_date(msg)
                    if date != 0:
                        details['periode'].append(date)
                        res = getResponse(details['type'],intents,details['nb_reponse'])
                        
                        
                    # On vérifie qu'un type de demande n'a pas déjà été fait
                    type_demande = recup_type(msg,1)
                    if (len(details['type_demande']) == 0) and (type_demande != 0):
                        details['type_demande'].append(type_demande)
                        res = getResponse(details['type'],intents,0)
                      
                    with open("memory"+str(nb_user)+".json", 'w') as json_file:
                        json.dump(details, json_file)
                    
                    # Si toutes les informations sont directement données sans le demander, on traite la demande
                    if (len(details['type_demande']) > 0) and (len(details['periode']) > 0):
                        periode = details['periode'][0].split("_")
                        type_demande = details['type_demande'][0]
                        start = periode[0]
                        end = periode[1]
                        # APPEL FONCTION AMRTA --- Modifier l'appel ici, et afficher le résultat
                        res = ""
                        for t in type_demande:
                            if res != "":
                                res = res + "_AND_"
                            try:
                                result = generate_stats.actions(t,details['type'],start,end,nb_user)
                                res = res + result
                            except:
                                res = res +"Je n'ai pas de résulats pour la période du "+start+" au "+end+", au sujet de la demande : "+t
                        details['type'] = ""
                        details['nb_reponse'] = 0
                        details['type_demande'] = ""
                        details['periode'] = ""

                        with open("memory"+str(nb_user)+".json", 'w') as json_file:
                            json.dump(details, json_file)
                        

                else:
                    res = getResponse(tag, intents)

            # Si une demande est en cours
            else :
                if len(details['periode']) == 0:
                    txt_erreur = "Le format indiqué n'est pas correct, veuillez me donner un format de date correct."
                    res = getResponse(details['type'],intents,details['nb_reponse'])
                    date = recup_date(msg)
                    # Si le message de l'utilisateur est incorrect
                    if date == 0:
                        res = txt_erreur
                    else:
                        details['periode'].append(date)
                # Sinon on passe au traitement de la demande
                else:
                    if len(details['type_demande']) == 0:
                        details['nb_reponse'] = 2
                        txt_erreur = "Je n'ai pas compris le type de demande que vous souhaitez. Veuillez me l'indiquer plus clairement"
                        res = getResponse(details['type'],intents,details['nb_reponse'])
                        type_demande = recup_type(msg)
                        if type_demande == 0:
                            res = txt_erreur
                        else:
                            details['type_demande'].append(type_demande)
                            
                
                if (len(details['type_demande']) > 0) and (len(details['periode']) > 0):
                    res = "END"
                    
                if res != txt_erreur :        
                    if res == "END":
                        periode = details['periode'][0].split("_")
                        type_demande = details['type_demande'][0]
                        start = periode[0]
                        end = periode[1]
                        # APPEL FONCTION AMRTA --- Modifier l'appel ici, et afficher le résultat
                        res = ""
                        for t in type_demande:
                            if res != "":
                                res = res + "_AND_"
                            try:
                                result = generate_stats.actions(t,details['type'],start,end,nb_user)
                                res = res + result
                            except:
                                res = res +"Je n'ai pas de résulats pour la période du "+start+" au "+end+", au sujet de la demande : "+t
                        details['type'] = ""
                        details['nb_reponse'] = 0
                        details['type_demande'] = ""
                        details['periode'] = ""

                        with open("memory"+str(nb_user)+".json", 'w') as json_file:
                            json.dump(details, json_file)
                    else :
                        details['nb_reponse'] +=1
                        with open("memory"+str(nb_user)+".json", 'w') as json_file:
                            json.dump(details, json_file)
        except:
            details['type'] = ""
            details['nb_reponse'] = 0
            details['type_demande'] = ""
            details['periode'] = "" 
            with open("memory"+str(nb_user)+".json", 'w') as json_file:
                json.dump(details, json_file)
            res = "ERROR"
        
    return res
    