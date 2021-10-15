#!/usr/bin/env python
# coding: utf-8

# ### Imports du code

# In[163]:


#!C:\Users\alexs\AppData\Local\Programs\Python\Python37\python.exe
import os
os.environ['APPDATA']="C:/Users/alexs/AppData/Roaming"

import numpy as np
import pandas as pd
import math
from math import *
import boto3
import io
import os
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# ### Fonctions d'IMC

# In[164]:


def IMC(dataframe,id_user):
        
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight']}
    df_IMC = pd.DataFrame(columns)
    df_user = df_IMC[(df_IMC['id_user'] == id_user)]
    line_imc = df_IMC.tail(1)
    h= line_imc['Height'].values
    w= line_imc['Weight'].values
    taille = h[0]
    poids = w[0]
    imc_formula = poids / (taille*0.01)**2
    if (imc_formula < 18.5):
        return "Votre IMC est de "+str(round(imc_formula,2))+" Vous êtes en insuffisance pondérale (maigreur)";
    elif (imc_formula > 18.5 or imc_formula < 25):
        return "Votre IMC est de "+str(round(imc_formula,2))+" Vous êtes en corpulence normale, félicitations.";
    elif (imc_formula > 25 or imc_formula < 30):
        return "Votre IMC est de "+str(round(imc_formula,2))+" Vous êtes en surpoids, ne vous en faites pas, c'est assez courant. Continuez vos efforts";
    elif (imc_formula > 30 or imc_formula < 35):
        return "Votre IMC est de "+str(round(imc_formula,2))+" Vous êtes en obésité modérée. Faites attention à votre sport quotidien.";
    elif (imc_formula > 35 or imc_formula < 40):
        return "Votre IMC est de "+str(round(imc_formula,2))+" Vous êtes en obésité. Votre santé a besoin que vous fassiez plus d'efforts physiques.";
    elif (imc_formula < 40):
        return "Votre IMC est de "+str(round(imc_formula,2))+" Vous êtes en obésité morbide ou massive. Votre santé est en grand danger, veuillez consulter un médecin.";


# In[165]:


def average_IMC(dataframe,id_user):
    
    now = datetime.now()
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight'],"Date": dataframe['date']}
    df_IMC = pd.DataFrame(columns)
    df_user = df_IMC[(df_IMC['id_user'] == id_user)]
    imcs= []
    for i in df_user.itertuples():
        imc_formula = i.Weight / (i.Height*0.01)**2
        imcs.append(imc_formula)
    
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight'],"Date": dataframe['date'],"IMC":imcs}
    df_IMC_2 = pd.DataFrame(columns)
    result_average_imc = df_IMC_2["IMC"].mean()
    if (result_average_imc < 18.5):
        return "Votre IMC moyen est de "+str(round(result_average_imc,2))+" Vous êtes en insuffisance pondérale (maigreur)";
    elif (result_average_imc > 18.5 or result_average_imc < 25):
        return "Votre IMC moyen est de "+str(round(result_average_imc,2))+" Vous êtes en corpulence normale, félicitations.";
    elif (result_average_imc > 25 or result_average_imc < 30):
        return "Votre IMC moyen est de "+str(round(result_average_imc,2))+" Vous êtes en surpoids, ne vous en faites pas, c'est assez courant. Continuez vos efforts";
    elif (result_average_imc > 30 or result_average_imc < 35):
        return "Votre IMC moyen est de "+str(round(result_average_imc,2))+" Vous êtes en obésité modérée. Faites attention à votre sport quotidien.";
    elif (result_average_imc > 35 or result_average_imc < 40):
        return "Votre IMC moyen est de "+str(round(result_average_imc,2))+" Vous êtes en obésité. Votre santé a besoin que vous fassiez plus d'efforts physiques.";
    elif (result_average_imc < 40):
        return "Votre IMC moyen est de "+str(round(result_average_imc,2))+" Vous êtes en obésité morbide ou massive. Votre santé est en grand danger, veuillez consulter un médecin.";


# In[166]:


def evolution_number_IMC(dataframe,id_user):
    
    now = datetime.now()
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight'],"Date": dataframe['date']}
    df_IMC = pd.DataFrame(columns)
    df_user = df_IMC[(df_IMC['id_user'] == id_user)]
    imcs= []
    for i in df_user.itertuples():
        imc_formula = i.Weight / (i.Height*0.01)**2
        imcs.append(imc_formula)
    
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight'],"Date": dataframe['date'],"IMC":imcs}
    df_IMC_2 = pd.DataFrame(columns)
    df_group = df_IMC_2.groupby(df_IMC_2["Date"]).agg("max")
    
    ############################# Sorting Date ###############################################
        
    dataframe_values = np.array(df_group["IMC"])
    dataframe_index = np.array(df_group.index)
        
    # Create sorted values by date in a zip
    zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
    sorted_zip = sorted(zip_iterator)
        
    date = []
    columns_values = []
    my_xticks = []
    for i in range(len(sorted_zip)):
        date.append(str(sorted_zip[i][0]).split(" ")[0])
        columns_values.append(float(sorted_zip[i][1]))
        d = str(sorted_zip[i][0]).split(" ")[0]
        my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))
        
    ############################################################################
    
    fig = plt.figure()
    x=np.array(date)
    y=np.array(columns_values)
    ax = fig.add_subplot()
    ax.set_xticklabels(my_xticks,rotation=50)
    
    plt.axhspan(10, 18.5, color='grey', alpha=0.5, lw=0,label = "Maigreur")
    plt.axhspan(18.6, 25, color='green', alpha=0.5, lw=0,label = "Normale")
    plt.axhspan(25.1,30, color='yellow', alpha=0.5, lw=0,label = "Surpoids")
    plt.axhspan(30.1, 35, color='orange', alpha=0.5, lw=0,label = "Obésité")
    plt.axhspan(35.1, 40, color='red', alpha=0.5, lw=0,label = "Obésité modérée")
    plt.axhspan(40, 45, color='black', alpha=0.5, lw=0,label = "Obésité massive")

    plt.plot(x,y,marker="o",label = "IMC par jour")
    img_title = " Evolution de L'IMC par jour"
    
    plt.legend()
    
    plt.gcf().set_size_inches(len(date)+5,9)
    img_code = "graph_evolution_number_IMC"+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
    fig.suptitle(img_title, fontsize=16)
    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
    fig.savefig(path)
    plt.close()
    
    return str("IMG:"+ path)


# In[167]:


def evolution_average_IMC(dataframe,id_user):
    
    #now = datetime.datetime.now()
    now = datetime.now()
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight'],"Date": dataframe['date']}
    df_IMC = pd.DataFrame(columns)
    df_user = df_IMC[(df_IMC['id_user'] == id_user)]
    imcs= []
    for i in df_user.itertuples():
        imc_formula = i.Weight / (i.Height*0.01)**2
        imcs.append(imc_formula)
    
    columns = {'id_user': dataframe['iduser'],'Height': dataframe['height'],'Weight': dataframe['weight'],"Date": dataframe['date'],"IMC":imcs}
    df_IMC_2 = pd.DataFrame(columns)
    df_group = df_IMC_2.groupby(df_IMC_2["Date"]).mean()
    
    ############################# Sorting Date ###############################################
        
    dataframe_values = np.array(df_group["IMC"])
    dataframe_index = np.array(df_group.index)
        
    # Create sorted values by date in a zip
    zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
    sorted_zip = sorted(zip_iterator)
        
    date = []
    columns_values = []
    my_xticks = []
    for i in range(len(sorted_zip)):
        date.append(str(sorted_zip[i][0]).split(" ")[0])
        columns_values.append(float(sorted_zip[i][1]))
        d = str(sorted_zip[i][0]).split(" ")[0]
        my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))
    ############################################################################
    

    fig = plt.figure()
    x=np.array(date)
    y=np.array(columns_values)
    ax = fig.add_subplot()
    ax.set_xticklabels(my_xticks,rotation=50)

    plt.axhspan(10, 18.5, color='grey', alpha=0.5, lw=0,label = "Maigreur")
    plt.axhspan(18.6, 25, color='green', alpha=0.5, lw=0,label = "Normale")
    plt.axhspan(25.1,30, color='yellow', alpha=0.5, lw=0,label = "Surpoids")
    plt.axhspan(30.1, 35, color='orange', alpha=0.5, lw=0,label = "Obésité")
    plt.axhspan(35.1, 40, color='red', alpha=0.5, lw=0,label = "Obésité modérée")
    plt.axhspan(40.1, 45, color='black', alpha=0.5, lw=0,label = "Obésité massive")
    img_title = " Evolution moyenne de l'IMC par jours"

    plt.plot(x,y,marker="o")
    
    plt.legend()
    plt.gcf().set_size_inches(len(date)+5,9)
    img_code = "graph_evolution_average_IMC"+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
    fig.suptitle(img_title, fontsize=16)
    #path = "Graphes/user_"+str(id_user)+"/"+img_code
    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
    fig.savefig(path)
    plt.close()

    return str("IMG:"+ path)


# ### Fonctions VMA

# In[168]:


def VMA(dataframe,debut,fin,id_user):
    #print("VMA CALCULATION")
    debut_date = debut.split(" ")[0]
    debut_hour = debut.split(" ")[1]
    fin_date = fin.split(" ")[0]
    fin_hour = fin.split(" ")[1]
    
    columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'], 'Hour': dataframe['hour']}
    df_steps = pd.DataFrame(columns)
    df_user = df_steps[(df_steps['id_user'] == id_user)]
    
    dataframe_values= df_user.values
    
    list_steps=[]
    cpt = 0 
    steps = 0 
    
    for i in dataframe_values:
        cpt += 1
        steps += i[1]
        #print(i)
        if cpt % 6 == 0:
            list_steps.append(steps)
            #print(steps)
            cpt =  0
            steps = 0

    
    max_steps_on_six_minutes = max(list_steps)
    stepstometer=max_steps_on_six_minutes /2
    vma_formula = stepstometer/100
    result = "Votre VMA maximale est de "+ str(vma_formula)
    return result


# In[169]:


def evolution_number_VMA(dataframe,id_user):
    #print("VMA CALCULATION")
    now = datetime.now()
    columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'], 'Hour': dataframe['hour']}
    df_steps = pd.DataFrame(columns)
    df_user = df_steps[(df_steps['id_user'] == id_user)]
    dates = df_user["Date"].unique()
    list_vma_by_day = []
    for date in dates:
        dataframe_by_day = df_user[(df_user["Date"] == str(date))]
        dataframe_values= dataframe_by_day.values
        list_steps=[]
        cpt = 0 
        steps = 0 
        
        for i in dataframe_values:
            cpt += 1
            steps += i[1]
            #print(i)
            if cpt % 6 == 0:
                list_steps.append(steps)
                #print(steps)
                cpt =  0
                steps = 0

    
        max_steps_on_six_minutes = max(list_steps)
        stepstometer=max_steps_on_six_minutes /2
        vma_formula = stepstometer/100
        list_vma_by_day.append(vma_formula)
        
    
    ############################# Sorting Date ###############################################
        
    dataframe_values = np.array(list_vma_by_day)
    dataframe_index = np.array(dates)
        
    # Create sorted values by date in a zip
    zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
    sorted_zip = sorted(zip_iterator)
        
    date = []
    columns_values = []
    my_xticks = []
    for i in range(len(sorted_zip)):
        date.append(str(sorted_zip[i][0]).split(" ")[0])
        columns_values.append(float(sorted_zip[i][1]))
        d = str(sorted_zip[i][0]).split(" ")[0]
        my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))
    ############################################################################
    
    fig = plt.figure()
    x=np.array(date)
    y=np.array(columns_values)
    ax = fig.add_subplot()
    ax.set_xticklabels(my_xticks,rotation=50)
    
    plt.plot(x,y,marker="o",label = "VMA par jours")
    img_title = " Evolution de la VMA par jours"
    
    plt.legend()
    
    plt.gcf().set_size_inches(len(date)+5,9)
    img_code = "graph_evolution_number_VMA"+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
    fig.suptitle(img_title, fontsize=16)
    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
    fig.savefig(path)
    plt.close()
    
    return str("IMG:"+ path)


# In[170]:


def evolution_average_VMA(dataframe,id_user):
    #print("Etant donné que votre demande a aucun sens , nous vous présentons le graphique d'evolution de la VMA par jour")
    return evolution_number_VMA(dataframe,id_user)


# ### Fonctions de valeurs fixes ( moyennes et nombre totale à l'écrit )

# In[171]:


def average(dataframe,col,debut,fin,id_user):
      
    now = datetime.now()
    debut_date = debut.split(" ")[0]
    debut_hour = debut.split(" ")[1]
    fin_date = fin.split(" ")[0]
    fin_hour = fin.split(" ")[1]

    fmt = '%d-%m-%Y %H:%M'
    tstamp1 = datetime.strptime(debut, fmt)
    tstamp2 = datetime.strptime(fin, fmt)
    date_difference = tstamp2-tstamp1
    age = dataframe['age'].iloc[0]
    card_m = str(220 - int(age))
    s = dataframe['gender'].iloc[0]
    if s == "f":
        cons_cal = "1800 - 2000 kcal"
        sexe = "une femme"
    else:
        cons_cal = "2100 - 2700 kcal"
        sexe = "un homme"
    #print(date_difference.days)

    if (col == 'calories'):
        
        if(date_difference.days == 0):
            
            heure_difference = int(str(date_difference / 60).split(":")[1])
         
            columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Hour': dataframe['hour'],'Weight': dataframe['weight']}
            df_calories = pd.DataFrame(columns)
            df_user = df_calories[(df_calories['id_user'] == id_user)]
            w = df_user['Weight'].tail(1)
            just_hour = []
            for i in df_user["Hour"]:
                just_hour.append(i.split(":")[0])
                
            columns_2 = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'],'Date': dataframe['date'],'Hour': dataframe['hour'],'Weight': dataframe['weight'],"Heure": just_hour}
            df_calories_h = pd.DataFrame(columns_2)
            
            # Sommes des calories par heure pour faire la moyenne
            somme_per_date = df_calories_h.groupby(df_calories_h["Heure"]).sum()
        
            list_calories = []
            for i in somme_per_date.itertuples():
                list_calories.append(ceil(((i.Steps*0.7)*w*1.036))/100)
                                     #list_calories.append(ceil(((i.Steps*0.7) * Poids_user * 1.036))/100)

            columns_3 = {'id_user': somme_per_date['id_user'],'Steps': somme_per_date['Steps'], 'CaloriesByHour': list_calories}
            df_average_calories = pd.DataFrame(columns_3)
            
            somme_calorie_totale = df_average_calories["CaloriesByHour"].sum()
           
            average_calories = ceil(somme_calorie_totale/(heure_difference))
            return "En moyenne par heures, vous avez perdu environ "+ str(average_calories) + " kcal dans la période sélectionnée. La moyenne de consommation calorique par jour pour "+sexe+" est de "+cons_cal+". Toutefois, les efforts physiques ne sont qu'une partie de cette consommation quotidienne."
            
        else:
            columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Weight': dataframe['weight'],'Hour': dataframe['hour']}
            df_calories = pd.DataFrame(columns)
            df_user = df_calories[(df_calories['id_user'] == id_user)]
            w = df_user['Weight'].tail(1)
            # Sommes des calories par jour pour faire la moyenne
            somme_per_date = df_user.groupby(df_user["Date"]).sum()
            df_values = somme_per_date.values
            
            list_calories = []
            for i in somme_per_date.itertuples():
                list_calories.append(ceil(((i.Steps*0.7)*w*1.036))/100)

            columns_2 = {'id_user': somme_per_date['id_user'],'Steps': somme_per_date['Steps'], 'CaloriesByDay': list_calories}
            df_average_calories = pd.DataFrame(columns_2)
            
            somme_calorie_totale = df_average_calories["CaloriesByDay"].sum()
            
            average_calories = ceil(somme_calorie_totale/(date_difference.days+1))

            return "En moyenne par jours, vous avez perdu environ "+ str(average_calories) + " kcal dans la période sélectionnée. La moyenne de consommation calorique par jour pour "+sexe+" est de "+cons_cal+". Toutefois, les efforts physiques ne sont qu'une partie de cette consommation quotidienne. "

    if (col == "blood_pressure"):
                  
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]
        systolic = []
        diastolic = []
        for i in df_user[col]:
            systolic.append(float(i.split("/")[0]))
            diastolic.append(float(i.split("/")[1]))

        columns_2 = {'id_user': dataframe['iduser'],col: dataframe[col],"Systolic_value":systolic,"Diastolic_value":diastolic, 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_blood_pressure = pd.DataFrame(columns_2)
        somme_sys_value_date = df_blood_pressure["Systolic_value"].groupby(df_blood_pressure["Date"]).sum()
        somme_dias_value_date = df_blood_pressure["Diastolic_value"].groupby(df_blood_pressure["Date"]).sum()
        df_count_sys = df_blood_pressure["Systolic_value"].groupby(df_blood_pressure["Date"]).count()
        df_count_dias = df_blood_pressure["Diastolic_value"].groupby(df_blood_pressure["Date"]).count()
        sum_sys_value = sum(somme_sys_value_date)
        sum_dias_value = sum(somme_dias_value_date)
        sum_count_sys = sum(df_count_sys)
        sum_count_dias = sum(df_count_dias)

        moyenne_sys_day = sum_sys_value/sum_count_sys
        moyenne_dias_day = sum_dias_value/sum_count_dias

        return "La moyenne par jours de pressions sanguines systoliques/diastoliques sur la période sélectionnée est de: "+ str(round(moyenne_sys_day,1))+"/"+str(round(moyenne_dias_day,1))

    if (col == "temperature"):
                         
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]

        df_col_by_day1 = df_user.groupby(df_user["Date"]).sum()# Sommes des température par jour de la semaine
        df_count = df_user.groupby(df_user["Date"]).count()# nombre de valeurs par date

        sum_temp_value = sum(df_col_by_day1["temperature"])
        sum_temp_count= sum(df_count["temperature"])

        moyenne_temp = sum_temp_value/sum_temp_count

        return "La moyenne par jours de temperature sur la période séléctionnée est de: "+ str(round(float(moyenne_temp),1))

    if (col == "heartbeat"):
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]

        df_col_by_day1 = df_user.groupby(df_user["Date"]).sum()# Sommes des température par jour de la semaine
        df_count = df_user.groupby(df_user["Date"]).count()# nombre de valeurs par date

        sum_temp_value = sum(df_col_by_day1["heartbeat"])
        sum_temp_count= sum(df_count["heartbeat"])

        moyenne_temp = sum_temp_value/sum_temp_count
        return "La moyenne de battements de coeur par minutes sur la période séléctionnée est de: "+str(round(moyenne_temp,1))+". Pour un adulte, le battement moyen au repos se situe entre 55 et 85. Et à l'effort il devrait se situer aux alentours de "+card_m+" pour vous."

    else:    
        if(date_difference.days == 0):

            heure_difference = int(str(date_difference / 60).split(":")[1])
            
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_average = pd.DataFrame(columns)
            df_user = df_average[(df_average['id_user'] == id_user)]
            just_hour = []
            for i in df_user["Hour"]:
                just_hour.append(i.split(":")[0])
                
            columns_2 = {'id_user': dataframe['iduser'],col: dataframe[col],'Date': dataframe['date'],'Hour': dataframe['hour'],"Heure": just_hour}
            df_mean = pd.DataFrame(columns_2)
            somme = df_mean[col].groupby(df_mean["Heure"]).sum()
            
            somme_totale = somme.sum()
            moyenne = somme_totale/(heure_difference)

            return "La moyenne de "+col+" sur la période séléctionnée est de: "+str(round(moyenne,1))
        else:
            
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_average = pd.DataFrame(columns)
           
            df_user = df_average[(df_average['id_user'] == id_user)]
            #somme de pas par jour
            somme = df_user[col].groupby(df_user["Date"]).sum()
            somme_totale = somme.sum()
            moyenne = somme_totale/(date_difference.days+1)
            

            return "La moyenne par jours de "+col+" sur la période séléctionnée est de: "+str(round(moyenne,1))


# In[172]:


def number(dataframe,col,debut,fin,id_user):
    
    debut_date = debut.split(" ")[0]
    debut_hour = debut.split(" ")[1]
    fin_date = fin.split(" ")[0]
    fin_hour = fin.split(" ")[1]
    s = dataframe['gender'].iloc[0]
    if s == "f":
        cons_cal = "1800 - 2000 kcal"
        sexe = "une femme"
    else:
        cons_cal = "2100 - 2700 kcal"
        sexe = "un homme"
    
    if (col == "calories"):
        
        columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Hour': dataframe['hour'],'Weight':dataframe['weight']}
        df_nb_calories = pd.DataFrame(columns)
        df_user = df_nb_calories[(df_nb_calories['id_user'] == id_user)]
        #df_steps = df_user['Steps'].sum()
        
        #display(df_steps)
        #for i in df_user['Steps']:
            #print(i)
        
        #list_calories = []
        result = 0 
        for i in df_user.itertuples():
            result+=ceil(((i.Steps*0.7)*i.Weight*1.036))/100
        
            
        #ceil(((i.Steps*0.7)*i.Weight*1.036))/100
        return "Vous avez perdu environ "+ str(round(result,1)) + " kcals dans la période séléctionnée. La moyenne de consommation calorique par jour pour "+sexe+" est de "+cons_cal+". Toutefois, les efforts physiques ne sont qu'une partie de cette consommation quotidienne. "
    
    if (col == "temperature"):
        
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]
        max_df = df_user[col].max(axis = 0)
        min_df = df_user[col].min(axis = 0)
        return "La valeur maximale de température durant la période sélectionnée est de :"+ str(max_df)+". La valeur minimale de température durant la période sélectionnée est de :"+ str(min_df)
    
    if (col == "heartbeat"):
        
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]
        max_df = df_user[col].max(axis = 0)
        min_df = df_user[col].min(axis = 0)
        return "La valeur maximale de battements du coeur par minutes durant la période séléctionnée est de: "+ str(max_df)+". La valeur minimale de battements du coeur par minutes durant la période séléctionnée est de :"+ str(min_df)+". En général, des battements minimum de 55, et des battements maximum de 220 sont possibles. Tout dépend de l'effort en question et de votre état de santé. En cas de doute, n'hésitez pas à en parler avec votre médecin."
    
    
    if (col == "blood_pressure"):
        
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]
        systolic = []
        diastolic = []
        for i in df_user[col]:
            systolic.append(i.split("/")[0])
            diastolic.append(i.split("/")[1])
            
        columns_2 = {'id_user': dataframe['iduser'],col: dataframe[col],"Systolic_value":systolic,"Diastolic_value":diastolic, 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_blood_pressure = pd.DataFrame(columns_2)
        max_sys_value = df_blood_pressure["Systolic_value"].max(axis = 0)
        max_dias_value = df_blood_pressure["Diastolic_value"].max(axis = 0)
        min_sys_value = df_blood_pressure["Systolic_value"].min(axis = 0)
        min_dias_value = df_blood_pressure["Diastolic_value"].min(axis = 0)
        
        return "La valeur maximale de pression sanguine systolique durant la période séléctionnée est de : "+ str(max_sys_value+"/"+max_dias_value)+". La valeur minimale de pression sanguine durant la période séléctionnée est de : "+ str(min_sys_value+"/"+min_dias_value)
    
    else:  
            
        columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
        df_number = pd.DataFrame(columns)
        df_user = df_number[(df_number['id_user'] == id_user)]
        #max_df = df_user[col].max(axis = 0)
        #min_df = df_user[col].min(axis = 0)
        somme = df_user[col].sum()
        
        if(col =="steps"):
            return "La somme du nombre de pas sur la période sélectionnée est de: "+ str(round(somme,1))
        else:
            return "La somme de "+ col +" sur la période séléctionnée est de: "+ str(round(somme,1))


# ### Fonctions générations de graphiques ( moyennes et nombre totale )

# In[200]:


def evolution_average(dataframe,col,debut,fin,id_user):
    
    now = datetime.now()

    fmt = '%d-%m-%Y %H:%M'
    tstamp1 = datetime.strptime(debut, fmt)
    tstamp2 = datetime.strptime(fin, fmt)
    date_difference = tstamp2-tstamp1
    #print(date_difference.days)
    hours_difference = date_difference.days * 24 + date_difference.seconds // 3600
    minutes_for_hour_difference = (date_difference.seconds % 3600) // 60
    
    if (col == "calories"):
        
        if(date_difference.days >8):
            
            
            columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Hour': dataframe['hour'],'Weight': dataframe['weight']}
            df_nb_calories = pd.DataFrame(columns)
            df_user = df_nb_calories[(df_nb_calories['id_user'] == id_user)]
            w = df_user['Weight'].tail(1)
            #display(df_user)
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                
                
            columns_2 = {'id_user': df_user['id_user'],'Steps': df_user['Steps'], 'Date': df_user['Date'],'Hour': df_user['Hour'],'Weight': df_user['Weight'],"DayoftheWeek":dayoftheweek}
            df_calories_by_day = pd.DataFrame(columns_2)
            #display(df_calories_by_day)
            
            df_cal_by_day1 = df_calories_by_day.groupby(df_calories_by_day["DayoftheWeek"]).sum()# Sommes des steps par jour de la semaine
            df_cal_by_day = df_cal_by_day1.sort_index()
            only_for_index = df_calories_by_day.groupby(df_calories_by_day["Date"]).sum()
            #display(df_cal_by_day)
            
            #diviser par le nombre de jour par semaine
            dates = only_for_index.index
            #print(dates)
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 0
            
            for i in dates:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    Monday += 1
                if (temp.day_name() == 'Tuesday'):
                    Tuesday += 1
                if (temp.day_name() == 'Wednesday'):
                    Wednesday += 1
                if (temp.day_name() == 'Thursday'):
                    Thursday += 1
                if (temp.day_name() == 'Friday'):
                    Friday += 1
                if (temp.day_name() == 'Saturday'):
                    Saturday += 1
                if (temp.day_name() == 'Sunday'):
                    Sunday += 1
            
                
            #display(df_cal_by_day)
            list_mean_calories = []
            for i in df_cal_by_day.itertuples():
                
                somme_calories = ceil(((i.Steps*0.7)*w*1.036))/100
                #print("la somme de calories est de ",somme_calories)
                if (i.Index == '1'):
                    
                    moyenne = somme_calories / Monday
                    list_mean_calories.append(ceil(moyenne))
                if (i.Index =='2'):
                   
                    moyenne = somme_calories / Tuesday
                    list_mean_calories.append(ceil(moyenne))
                if (i.Index == '3'):
                    
                    moyenne = somme_calories / Wednesday
                    list_mean_calories.append(ceil(moyenne))
                if (i.Index == '4'):
                    
                    moyenne = somme_calories / Thursday
                    list_mean_calories.append(ceil(moyenne))
                if (i.Index == '5'):
                    
                    moyenne = somme_calories / Friday
                    list_mean_calories.append(ceil(moyenne))
                if (i.Index == '6'):
                    
                    moyenne = somme_calories / Saturday
                    list_mean_calories.append(ceil(moyenne))
                if (i.Index == '7'):
                    
                    moyenne = somme_calories / Sunday
                    list_mean_calories.append(ceil(moyenne))
            
            
            # Moyenne des calories par heure pour faire la moyenne

            columns_mean_values = pd.to_numeric(list_mean_calories)
            day_of_week = df_cal_by_day.index
                           

            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y=np.array(columns_mean_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            plt.plot(x,y,marker="o",label = "Moyenne_Calories_par_jour")
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_title = "Evolution de la moyenne calorique en kcal"
            img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
            
        else:
            if(date_difference.days == 0):
                
                if(hours_difference<=23):
                    
                    
                    columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Weight':dataframe['weight'],'Hour': dataframe['hour']}
                    df_nb_calories = pd.DataFrame(columns)
                    df_user = df_nb_calories[(df_nb_calories['id_user'] == id_user)]
                    w = df_user['Weight'].tail(1)
                    #print(w)
                    #display(df_user)
                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)


                    columns_2 = {'id_user': df_user['id_user'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Hour': dataframe['hour'],'Weight':dataframe['weight'],"Heure":heure}
                    df_calories_by_day = pd.DataFrame(columns_2)
                    #display(df_calories_by_day)

                    df_cal_by_day1 = df_calories_by_day.groupby(df_calories_by_day["Heure"]).mean()# somme des calories par heure
                    df_cal_by_day = df_cal_by_day1.sort_index()
                    df_quantity_values_by_dates = df_calories_by_day.groupby(df_calories_by_day["Heure"]).count()# somme des calories par heure
                    only_for_index = df_calories_by_day.groupby(df_calories_by_day["Heure"]).sum()
                    
                    #display(df_cal_by_day)
                    list_mean_calories = []
                    for i in df_cal_by_day.itertuples():
                        moyenne_calories = ceil(((i.Steps*0.7)*w*1.036))/100
                        list_mean_calories.append(moyenne_calories)


                    # Moyenne des calories par heure pour faire la moyenne

                    columns_mean_values = pd.to_numeric(list_mean_calories)
                    day_of_week = df_cal_by_day.index


                    fig = plt.figure()
                    ax = fig.add_subplot()
                    x=np.array(day_of_week)
                    y=np.array(columns_mean_values)

                    #my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                    #ax.set_xticklabels(my_xticks,rotation=50)
                    plt.plot(x,y,marker="o",label = "Moyenne_Calories_perdues_par_minutes")
                    plt.legend()
                    plt.gcf().set_size_inches(len(day_of_week)+5,9)
                    img_title = "Evolution de la moyenne calorique en kcal par minutes"
                    img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)

                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    #return "moyenne by day"
                    return str("IMG:"+ path)
                    
                else:
                    pass
            
            else:
            
                columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Weight': dataframe['weight'],'Hour': dataframe['hour']}
                df_nb_calories = pd.DataFrame(columns)
                df_user = df_nb_calories[(df_nb_calories['id_user'] == id_user)]
                w = df_user['Weight'].tail(1)
                # Sommes des calories par jour pour faire la moyenne
                df_cal_bydate = df_user.groupby(df_user["Date"]).sum()       

                list_calories = []
                for i in df_cal_bydate.itertuples():
                    list_calories.append(ceil(((i.Steps*0.7)*w*1.036))/100)

                list_mean_calories=[]
                for j in list_calories:
                    list_mean_calories.append(j/24)

                columns_2 = {'id_user': df_cal_bydate['id_user'],'MeanCaloriesByDay': list_mean_calories}
                df_average_calories = pd.DataFrame(columns_2)
                #display(df_average_calories)


                ############################# Sorting Date ###############################################

                dataframe_values = np.array(df_average_calories["MeanCaloriesByDay"].values)
                dataframe_index = np.array(df_average_calories.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_values.append(float(sorted_zip[i][1]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))


                ############################################################################


                fig = plt.figure()
                x=np.array(date)
                y=np.array(columns_values)
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=50)
                if(col == "calories"):
                    plt.plot(x,y,marker="o",label = "Moyenne_Calories_par_heure")
                    img_title = "Evolution de la moyenne calorique (kcal)"
                else:
                    plt.plot(x,y,marker="o",label = "Nombre de"+str(col)+" par heure")
                    img_title = " Evolution du nombre de"+str(col)+" par heure"

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()

                return str("IMG:"+ path)
            
    
    if (col == "blood_pressure"):
        
        if(date_difference.days >8):
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
            
            systolic = []
            diastolic = []
            for i in df_user[col]:
                systolic.append(float(i.split("/")[0]))
                diastolic.append(float(i.split("/")[1]))
                
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                    
            columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"Systolic_value":systolic,"Diastolic_value":diastolic,"DayoftheWeek":dayoftheweek}
            df_m = pd.DataFrame(columns_2)
            
            df_col_by_day1 = df_m.groupby(df_m["DayoftheWeek"]).mean()# Sommes des steps par jour de la semaine
            df_col_by_day = df_m.sort_index()
            only_for_date_index = df_m.groupby(df_m["Date"]).sum()
            
            columns_mean_sys_values = pd.to_numeric(df_col_by_day1["Systolic_value"])
            columns_mean_dias_values = pd.to_numeric(df_col_by_day1["Diastolic_value"])
            day_of_week = df_col_by_day1.index
                           
            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y_sys=np.array(columns_mean_sys_values)
            y_dias = np.array(columns_mean_dias_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "blood_pressure"):
                plt.plot(x,y_sys,marker="o",label = "moyenne PS systolique par jour")
                plt.plot(x,y_dias,marker="o",label = "moyenne PS diastolique par jour")
                img_title = " Evolution de la moyenne de la pression artérielle par jour"
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
        
        
        else:
            if(date_difference.days == 0):
                if(hours_difference<=23):
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]

                    systolic = []
                    diastolic = []
                    for i in df_user[col]:
                        systolic.append(float(i.split("/")[0]))
                        diastolic.append(float(i.split("/")[1]))

                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"Systolic_value":systolic,"Diastolic_value":diastolic,"Heure":heure}
                    df_m = pd.DataFrame(columns_2)
                    

                    df_col_by_day1 = df_m.groupby(df_m["Heure"]).mean()# Sommes des steps par jour de la semaine
                    df_col_by_day = df_m.sort_index()
                    only_for_date_index = df_m.groupby(df_m["Date"]).sum()
                    

                    columns_mean_sys_values = pd.to_numeric(df_col_by_day1["Systolic_value"])
                    columns_mean_dias_values = pd.to_numeric(df_col_by_day1["Diastolic_value"])
                    hours_of_the_day = df_col_by_day1.index

                    fig = plt.figure()
                    ax = fig.add_subplot()
                    x=np.array(hours_of_the_day)
                    y_sys=np.array(columns_mean_sys_values)
                    y_dias = np.array(columns_mean_dias_values)

                    if(col == "blood_pressure"):
                        plt.plot(x,y_sys,marker="o",label = "moyenne PS systolique par heure")
                        plt.plot(x,y_dias,marker="o",label = "moyenne PS diastolique par heure")
                        img_title = " Evolution de la moyenne de la température par heure"
                    plt.legend()
                    plt.gcf().set_size_inches(len(hours_of_the_day)+5,9)
                    img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    #return "moyenne by day"
                    return str("IMG:"+ path)

                else:
                    pass
            else:
                
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]
                systolic = []
                diastolic = []
                for i in df_user[col]:
                    systolic.append(float(i.split("/")[0]))
                    diastolic.append(float(i.split("/")[1]))

                columns_2 = {'id_user': dataframe['iduser'],col: dataframe[col],"Systolic_value":systolic,"Diastolic_value":diastolic, 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_blood_pressure = pd.DataFrame(columns_2)
                df_sum = df_blood_pressure.groupby(df_blood_pressure["Date"]).sum()
                df_count = df_blood_pressure.groupby(df_blood_pressure["Date"]).count()

                sys = df_sum["Systolic_value"]
                dias = df_sum["Diastolic_value"]
                number_of_values_in_a_day = df_count["id_user"]

                list_mean_sys = []
                for i in range(len(sys)):
                    list_mean_sys.append(ceil(sys[i]/number_of_values_in_a_day[i]))
                list_mean_dias = []
                for i in range(len(dias)):
                    list_mean_dias.append(ceil(dias[i]/number_of_values_in_a_day[i]))

                ############################# Sorting Date ###############################################

                dataframe_sys_values = np.array(list_mean_sys)
                dataframe_dias_values = np.array(list_mean_dias)
                dataframe_index = np.array(df_sum.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_sys_values,dataframe_dias_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_sys_values = []
                columns_dias_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_sys_values.append(float(sorted_zip[i][1]))
                    columns_dias_values.append(float(sorted_zip[i][2]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                ax = fig.add_subplot()
                x_mean_sys=np.array(date)
                y_mean_sys=np.array(columns_sys_values)
                x_mean_dias=np.array(date)
                y_mean_dias=np.array(columns_dias_values)

                if(col == "blood_pressure"):
                    ax.set_xticklabels(my_xticks,rotation=50)
                    plt.plot(x_mean_sys, y_mean_sys, label = "moyenne PS systolique")
                    plt.plot(x_mean_dias, y_mean_dias, label = "moyenne PS diastolique")
                    img_title = " Evolution de la moyenne de la pression artérielle "

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()
                return str("IMG:"+ path)

    if (col == "temperature"):
        
        if(date_difference.days >8):
            
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
                
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                    
            columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"DayoftheWeek":dayoftheweek}
            df_m = pd.DataFrame(columns_2)
            #display(df_m)
            
            df_col_by_day1 = df_m.groupby(df_m["DayoftheWeek"]).mean()# Sommes des steps par jour de la semaine
            df_col_by_day = df_m.sort_index()
            only_for_date_index = df_m.groupby(df_m["Date"]).sum()
            #display(df_col_by_day1)
                       
            columns_mean_values = pd.to_numeric(df_col_by_day1[col])
            day_of_week = df_col_by_day1.index
                           
            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y=np.array(columns_mean_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "temperature"):
                plt.plot(x,y,marker="o",label = "Moyennes de la température par jour")
                img_title = " Evolution de la moyenne de la température par jour"
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
        
        else:
            if(date_difference.days == 0):
                if(hours_difference<=23):
                    
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]

                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"Heure":heure}
                    df_m = pd.DataFrame(columns_2)
                    

                    df_col_by_day1 = df_m.groupby(df_m["Heure"]).mean()# Sommes des steps par jour de la semaine
                    df_col_by_day = df_m.sort_index()
                    only_for_date_index = df_m.groupby(df_m["Date"]).sum()
                    
                    columns_mean_values = pd.to_numeric(df_col_by_day1[col])
                    hours_of_the_day = df_col_by_day1.index

                    fig = plt.figure()
                    x=np.array(hours_of_the_day)
                    y=np.array(columns_mean_values)

                    if(col == "temperature"):
                        plt.plot(x,y,marker="o",label = "Moyennes température par heure")
                        img_title = " Evolution de la moyenne de la température par heure"
                    plt.legend()
                    plt.gcf().set_size_inches(len(hours_of_the_day)+5,9)
                    img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    #return "moyenne by day"
                    return str("IMG:"+ path)
                else:
                    pass
            else:
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]

                df_col_by_day1 = df_user.groupby(df_user["Date"]).sum()# Sommes des température par jour de la semaine
                df_count = df_user.groupby(df_user["Date"]).count()# nombre de valeurs par date
                df_col_by_day =  df_col_by_day1[col]
                number_of_values_in_a_day = df_count["id_user"]

                list_mean_temperature = []
                for i in range(len(df_col_by_day)):
                    list_mean_temperature.append(ceil(df_col_by_day[i]/number_of_values_in_a_day[i]))

                ############################# Sorting Date ###############################################

                dataframe_values = np.array(list_mean_temperature)
                dataframe_index = np.array(df_col_by_day1.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_values.append(float(sorted_zip[i][1]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                ax = fig.add_subplot()
                x=np.array(date)
                y=np.array(columns_values)
                ax.set_xticklabels(my_xticks,rotation=50)
                if(col == "temperature"):
                    plt.plot(x,y,marker="o",label = "Moyenne de la température par jour")
                    img_title = " Evolution moyenne de la température "

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()
                return str("IMG:"+ path)

    if (col == "heartbeat"):
        
        if(date_difference.days >8):
            
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
                
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                    
            columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"DayoftheWeek":dayoftheweek}
            df_m = pd.DataFrame(columns_2)
                        
            df_col_by_day1 = df_m.groupby(df_m["DayoftheWeek"]).mean()# Moyennes des heartbeat par jour de la semaine
            df_col_by_day = df_m.sort_index()
            
            columns_mean_values = pd.to_numeric(df_col_by_day1[col])
            day_of_week = df_col_by_day1.index
                           
            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y=np.array(columns_mean_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "heartbeat"):
                plt.plot(x,y,marker="o",label = "Moyennes de battements par minutes par jour")
                img_title = " Evolution de la moyenne de battements par minutes par jour"
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
            
        
        else:
            if(date_difference.days == 0):
                if(hours_difference<=23):
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]

                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"Heure":heure}
                    df_m = pd.DataFrame(columns_2)
                    

                    df_col_by_day1 = df_m.groupby(df_m["Heure"]).mean()# Sommes des steps par jour de la semaine
                    df_col_by_day = df_m.sort_index()
                    only_for_date_index = df_m.groupby(df_m["Date"]).sum()

                    
                    columns_mean_values = pd.to_numeric(df_col_by_day1[col])
                    hours_of_the_day = df_col_by_day1.index

                    fig = plt.figure()
                    x=np.array(hours_of_the_day)
                    y=np.array(columns_mean_values)

                    if(col == "heartbeat"):
                        plt.plot(x,y,marker="o",label = "moyenne de battements par minutes par heure")
                        img_title = " Evolution de la moyenne de battements par minutes par heure"
                    plt.legend()
                    plt.gcf().set_size_inches(len(hours_of_the_day)+5,9)
                    img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    #return "moyenne by day"
                    return str("IMG:"+ path)
                else:
                    pass
            else:
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]

                df_col_by_day1 = df_user.groupby(df_user["Date"]).sum()# Sommes des steps par jour de la semaine
                df_count = df_user.groupby(df_user["Date"]).count()# nombre de valeurs par date
                df_col_by_day =  df_col_by_day1[col]
                number_of_values_in_a_day = df_count["id_user"]
                #display(df_col_by_day1)

                list_mean_heartbeat = []
                for i in range(len(df_col_by_day)):
                    list_mean_heartbeat.append(ceil(df_col_by_day[i]/number_of_values_in_a_day[i]))

                ############################# Sorting Date ###############################################

                dataframe_values = np.array(list_mean_heartbeat)
                dataframe_index = np.array(df_col_by_day1.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_values.append(float(sorted_zip[i][1]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                ax = fig.add_subplot()
                x=np.array(date)
                y=np.array(columns_values)
                ax.set_xticklabels(my_xticks,rotation=50)
                if(col == "heartbeat"):
                    plt.plot(x,y,marker="o",label = "Moyenne de battement par minute par jour")
                    img_title = " Evolution de la moyenne de battement par minute par jour"

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()
                return str("IMG:"+ path)

    else:
        
        if(date_difference.days >8):
            
            
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
                
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                    
            columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"DayoftheWeek":dayoftheweek}
            df_m = pd.DataFrame(columns_2)
            #display(df_m)
            
            df_col_by_day1 = df_m.groupby(df_m["DayoftheWeek"]).sum()# Sommes des steps par jour de la semaine
            df_col_by_day = df_m.sort_index()
            only_for_index = df_m.groupby(df_m["Date"]).sum()
            #display(df_col_by_day1)
            
            #diviser par le nombre de jour par semaine
            dates = only_for_index.index
            
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 0
            
            for i in dates:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    Monday += 1
                if (temp.day_name() == 'Tuesday'):
                    Tuesday += 1
                if (temp.day_name() == 'Wednesday'):
                    Wednesday += 1
                if (temp.day_name() == 'Thursday'):
                    Thursday += 1
                if (temp.day_name() == 'Friday'):
                    Friday += 1
                if (temp.day_name() == 'Saturday'):
                    Saturday += 1
                if (temp.day_name() == 'Sunday'):
                    Sunday += 1
            
            list_days = [Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday]
            
            list_mean_calories = []
            
            for i in range(len(list_days)):
                moyenne = ceil(df_col_by_day1[col][i]/list_days[i])
                list_mean_calories.append(moyenne)
            
            columns_mean_values = pd.to_numeric(list_mean_calories)
            day_of_week = df_col_by_day1.index
                           
            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y=np.array(columns_mean_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "steps"):
                plt.plot(x,y,marker="o",label = "Nombre de pas par jour")
                img_title = " Evolution de la moyenne du nombre de pas par jour"
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
       
        else:
            if(date_difference.days == 0):
                if(hours_difference<=23):
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]

                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour'],"Heure":heure}
                    df_m = pd.DataFrame(columns_2)
                    

                    df_col_by_day1 = df_m.groupby(df_m["Heure"]).mean()# Sommes des steps par jour de la semaine
                    df_col_by_day = df_m.sort_index()
                    only_for_date_index = df_m.groupby(df_m["Date"]).sum()
                   

                    columns_mean_values = pd.to_numeric(df_col_by_day1[col])
                    hours_of_the_day = df_col_by_day1.index

                    fig = plt.figure()
                    x=np.array(hours_of_the_day)
                    y=np.array(columns_mean_values)

                    if(col == "steps"):
                        plt.plot(x,y,marker="o",label = "moyennes de pas par heure")
                        img_title = " Evolution de la moyenne de pas par heure"
                    plt.legend()
                    plt.gcf().set_size_inches(len(hours_of_the_day)+5,9)
                    img_code = "graph_evolution_average"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    #return "moyenne by day"
                    return str("IMG:"+ path)

                else:
                    pass
            else:
        
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]
                df_group = df_user.groupby(df_user["Date"]).sum()
                #display(df_group)

                list_mean_col = []
                for j in df_group[col].values:
                    list_mean_col.append(j/24)

                df_group.sort_index(ascending=False)
                #columns_values_by_dates = pd.to_numeric(df_group[col].values)
                #dates = df_group.index


                ############################# Sorting Date ###############################################

                dataframe_values = np.array(list_mean_col)
                dataframe_index = np.array(df_group.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_values.append(float(sorted_zip[i][1]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=50)

                x=np.array(date)
                y=np.array(columns_values)

                if(col == "steps"):
                    plt.plot(x,y,marker="o",label = "Nombre de pas par heure")
                    img_title = " Evolution du nombre de pas par heure"

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code= "graph_evolution_average_"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()
                
                return str("IMG:"+ path)
            


# In[204]:


def evolution_number(dataframe,col,debut,fin,id_user):
    
    now = datetime.now()
    fmt = '%d-%m-%Y %H:%M'
    tstamp1 = datetime.strptime(debut, fmt)
    tstamp2 = datetime.strptime(fin, fmt)
    date_difference = tstamp2-tstamp1
    #print(date_difference.days)
    hours_difference = date_difference.days * 24 + date_difference.seconds // 3600
    minutes_for_hour_difference = (date_difference.seconds % 3600) // 60
    
    if (col == "calories"):
        
        if(date_difference.days >8):
            
            columns = {'id_user': dataframe['iduser'],'Steps': dataframe["steps"], 'Date': dataframe['date'],'Hour': dataframe['hour'],'Weight':dataframe['weight']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
            w = df_user['Weight'].tail(1)
                
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                    
            columns_2 = {'id_user': df_user['id_user'],'Steps': df_user["Steps"], 'Date': df_user['Date'],'Hour': df_user['Hour'],"DayoftheWeek":dayoftheweek}
            df_m = pd.DataFrame(columns_2)
            #display(df_m)
            
            df_col_by_day1 = df_m.groupby(df_m["DayoftheWeek"]).sum()# Sommes des steps par jour de la semaine
            
            list_total_calories = []
            for i in df_col_by_day1.itertuples():
                list_total_calories.append(ceil(((i.Steps*0.7)*w*1.036))/100)
                
            
            columns_values = pd.to_numeric(list_total_calories)
            day_of_week = df_col_by_day1.index
                           
            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y=np.array(columns_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "calories"):
                plt.plot(x,y,marker="o",label = "Nombre de calories perdues par jour")
                img_title = " Evolution du nombre de calories perdues par jour"
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_code = "graph_evolution_number_calories"+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
    
        else:
            if(date_difference.days == 0):
                
                
                if(hours_difference<=23):
                    

                    columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Weight': dataframe['weight'],'Hour': dataframe['hour']}
                    df_nb_calories = pd.DataFrame(columns)
                    df_user = df_nb_calories[(df_nb_calories['id_user'] == id_user)]
                    w = df_user['Weight'].tail(1)

                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],'Steps': df_user['Steps'], 'Date': df_user['Date'],'Weight': df_user['Weight'],'Hour': df_user['Hour'],"Heure":heure}
                    df_sum = pd.DataFrame(columns_2)

                    # Sommes des calories par jour pour faire la moyenne
                    df_cal_bydate = df_sum.groupby(df_sum["Heure"]).sum()
                    df_values = df_cal_bydate.values

                    list_calories = []
                    for i in df_cal_bydate.itertuples():
                        list_calories.append(ceil(((i.Steps*0.7)*w*1.036))/100)

                    columns_3 = {'id_user': df_cal_bydate['id_user'],'CaloriesByDay': list_calories}
                    df_number_calories = pd.DataFrame(columns_3)


                    columns_mean_values = pd.to_numeric(list_calories)
                    hours_of_the_day = df_cal_bydate.index

                    fig = plt.figure()
                    x=np.array(hours_of_the_day)
                    y=np.array(columns_mean_values)

                    if(col == "calories"):
                        plt.plot(x,y,marker="o",label = "nombre de calories perdues par heures")
                        img_title = " Evolution du nombre de calories perdues par heures"

                    plt.legend()
                    plt.gcf().set_size_inches(len(hours_of_the_day)+5,9)
                    img_code = "graph_evolution_number"+"calories"+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    #return "moyenne by day"
                    return str("IMG:"+ path)

                else:
                    pass
            
        
            else:
                columns = {'id_user': dataframe['iduser'],'Steps': dataframe['steps'], 'Date': dataframe['date'],'Weight': dataframe['weight'],'Hour': dataframe['hour']}
                df_nb_calories = pd.DataFrame(columns)
                df_user = df_nb_calories[(df_nb_calories['id_user'] == id_user)]
                w = df_user['Weight'].tail(1)

                # Sommes des calories par jour pour faire la moyenne
                df_cal_bydate = df_user.groupby(df_user["Date"]).sum()
                df_values = df_cal_bydate.values

                list_calories = []
                for i in df_cal_bydate.itertuples():
                    list_calories.append(ceil(((i.Steps*0.7)*w*1.036))/100)

                columns_2 = {'id_user': df_cal_bydate['id_user'],'CaloriesByDay': list_calories}
                df_average_calories = pd.DataFrame(columns_2)

                ############################# Sorting Date ###############################################


                dataframe_values = np.array(df_average_calories["CaloriesByDay"])
                dataframe_index = np.array(df_average_calories["CaloriesByDay"].index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_values.append(float(sorted_zip[i][1]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################
                columns_values_by_dates = pd.to_numeric(columns_values)
                dates = date

                fig = plt.figure()
                x=np.array(dates)
                y=np.array(columns_values_by_dates)
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=50)
                if(col == "calories"):
                    plt.plot(x,y,marker="o",label = "Nombre de Calories_par_jour")
                    img_title = " Evolution du nombre de calories perdues par jours"
                else:
                    plt.plot(x,y,marker="o",label = "Nombre de Calories_par_jour")
                    img_title = " Evolution du nombre de"+str(col)+" par jours"


                plt.legend()
                plt.gcf().set_size_inches(len(x)+5,9)
                img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_title
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()

                return str("IMG:"+ path)

    
    if (col == "temperature"):
        
        if(date_difference.days>8):
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
            
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                    
            columns_2 = {'id_user': df_user['id_user'],col: df_user[col], 'Date': df_user['date'],'Hour': df_user['hour'],"DayoftheWeek":dayoftheweek}
            df_m = pd.DataFrame(columns_2)
            display(df_m)
            
            df_min_max_agg = df_m.groupby(df_m["DayoftheWeek"]).agg(['min', 'max'])
            df_temp = df_min_max_agg["temperature"]
            display(df_temp)
            
            dataframe_min_values = np.array(df_temp["min"])
            dataframe_max_values = np.array(df_temp["max"])
            
            fig = plt.figure()
            x_max=np.array(df_temp.index)
            y_max=np.array(dataframe_max_values)
            x_min=np.array(df_temp.index)
            y_min=np.array(dataframe_min_values)
            ax = fig.add_subplot()
            
            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "temperature"):
                plt.plot(x_max, y_max, label = "C° maximales par heure ")
                plt.plot(x_min, y_min, label = "C° minimales par heure ")
                img_title = " Evolution de la temperature par heure"

            else:
                plt.plot(x_max, y_max, label = "C° maximales par heure ")
                plt.plot(x_min, y_min, label = "C° minimales par heure ")
                img_title = " Evolution du nombre de"+str(col)+" par heure"

            plt.legend()
            plt.gcf().set_size_inches(len(df_temp.index)+5,9)
            img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()

            return str("IMG:"+ path)

        else:
            if(date_difference.days == 0):
                if(hours_difference <= 23):
                    
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]
                    
                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: df_user[col], 'Date': df_user['Date'],'Hour': df_user['Hour'],"Heure":heure}
                    df_sum = pd.DataFrame(columns_2)
                    
                    df_min_max_agg = df_sum.groupby(df_sum["Heure"]).agg(['min', 'max'])
                    df_temp = df_min_max_agg["temperature"]
                    
                    #display(df_temp)
                    
                    dataframe_min_values = np.array(df_temp["min"])
                    dataframe_max_values = np.array(df_temp["max"])
                    
                    fig = plt.figure()
                    x_max=np.array(df_temp.index)
                    y_max=np.array(dataframe_max_values)
                    x_min=np.array(df_temp.index)
                    y_min=np.array(dataframe_min_values)
                    ax = fig.add_subplot()
                    
                    if(col == "temperature"):
                        plt.plot(x_max, y_max, label = "C° maximales par heure ")
                        plt.plot(x_min, y_min, label = "C° minimales par heure ")
                        img_title = " Evolution de la température par heures"

                    else:
                        plt.plot(x_max, y_max, label = "C° maximales par heure ")
                        plt.plot(x_min, y_min, label = "C° minimales par heure ")
                        img_title = " Evolution du nombre de"+str(col)+" par heures"

                    plt.legend()
                    plt.gcf().set_size_inches(len(df_temp.index)+5,9)
                    img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()

                    return str("IMG:"+ path)
                    
                    
                else:
                    pass
            else:
        
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]
                df_min_max_agg = df_user.groupby(df_user["Date"]).agg(['min', 'max'])
                df_temp = df_min_max_agg["temperature"]
                

                ############################# Sorting Date ###############################################

                dataframe_min_values = np.array(df_temp["min"])
                dataframe_max_values = np.array(df_temp["max"])
                dataframe_index = np.array(df_temp.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_min_values, dataframe_max_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_min_values = []
                columns_max_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_min_values.append(float(sorted_zip[i][1]))
                    columns_max_values.append(float(sorted_zip[i][2]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                x_max=np.array(date)
                y_max=np.array(columns_max_values)
                x_min=np.array(date)
                y_min=np.array(columns_min_values)
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=50)
                if(col == "temperature"):
                    plt.plot(x_max, y_max, label = "C° maximales par jour ")
                    plt.plot(x_min, y_min, label = "C° minimales par jour ")
                    img_title = " Evolution de la température par jours"

                else:
                    plt.plot(x_max, y_max, label = "C° maximales par jour ")
                    plt.plot(x_min, y_min, label = "C° minimales par jour ")
                    img_title = " Evolution du nombre de"+str(col)+" par jours"

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_title
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()

                return str("IMG:"+ path)
    
    if (col == "blood_pressure"):
        
        if(date_difference.days>8):
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
                    
            systolic = []
            diastolic = []
            for i in df_user[col]:
                systolic.append(i.split("/")[0])
                diastolic.append(i.split("/")[1]) 
            
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                        
            columns_2 = {'id_user': df_user['id_user'],col: df_user[col],"Systolic_value":systolic,"Diastolic_value":diastolic, 'Date': df_user['Date'],'Hour': df_user['Hour'],"DayOfTheWeek": dayoftheweek}
            df_blood_pressure = pd.DataFrame(columns_2)
            df_min_max_agg = df_blood_pressure.groupby(df_blood_pressure["DayOfTheWeek"]).agg(['min', 'max'])
            sys = df_min_max_agg["Systolic_value"]
            dias = df_min_max_agg["Diastolic_value"]
            
            ############################# Sorting Date ###############################################

            dataframe_sys_min_values = np.array(sys["min"])
            dataframe_sys_max_values = np.array(sys["max"])
            dataframe_dias_min_values = np.array(dias["min"])
            dataframe_dias_max_values = np.array(dias["max"])
            dataframe_index = np.array(sys.index)

            # Create sorted values by date in a zip
            zip_iterator = zip(dataframe_index, dataframe_sys_min_values, dataframe_sys_max_values,dataframe_dias_min_values,dataframe_dias_max_values)
            sorted_zip = sorted(zip_iterator)

            hour = []
            columns_sys_min_values = []
            columns_sys_max_values = []
            columns_dias_min_values = []
            columns_dias_max_values = []
            my_xticks = []
            for i in range(len(sorted_zip)):
                hour.append(str(sorted_zip[i][0]).split(" ")[0])
                columns_sys_min_values.append(float(sorted_zip[i][1]))
                columns_sys_max_values.append(float(sorted_zip[i][2]))
                columns_dias_min_values.append(float(sorted_zip[i][3]))
                columns_dias_max_values.append(float(sorted_zip[i][4]))
                d = str(sorted_zip[i][0]).split(" ")[0]

           ############################################################################
            fig = plt.figure()
            x_max_min_sys_dias=np.array(hour)
            y_max_sys=np.array(columns_sys_max_values)
            y_min_sys=np.array(columns_sys_min_values)
            y_max_dias=np.array(columns_dias_max_values)
            y_min_dias=np.array(columns_dias_min_values)
            ax = fig.add_subplot()
            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)

            if(col == "blood_pressure"):
                plt.plot(x_max_min_sys_dias, y_max_dias, label = "max PS diastolique  par jours")
                plt.plot(x_max_min_sys_dias, y_min_dias, label = "min PS diastolique  par jours")
                plt.plot(x_max_min_sys_dias, y_min_sys, label = "min PS systolique  par jours")  
                plt.plot(x_max_min_sys_dias, y_max_sys, label = "max PS systolique par jours")
                img_title = " Evolution de la pression artérielle par jours"

            else:
                plt.plot(x_max_min_sys_dias, y_max_dias, label = "max PS diastolique  par jours")
                plt.plot(x_max_min_sys_dias, y_min_dias, label = "min PS diastolique  par jours")
                plt.plot(x_max_min_sys_dias, y_min_sys, label = "min PS systolique  par jours")  
                plt.plot(x_max_min_sys_dias, y_max_sys, label = "max PS systolique par jours")
                img_title = " Evolution du nombre de"+str(col)+" par jours"

            plt.legend()
            plt.gcf().set_size_inches(len(df_min_max_agg.index)+5,9)
            img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_code
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            return str("IMG:"+ path) 
            
        else:
            if(date_difference.days==0):
                if(hours_difference <= 23):
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]
                    
                    systolic = []
                    diastolic = []
                    for i in df_user[col]:
                        systolic.append(i.split("/")[0])
                        diastolic.append(i.split("/")[1])
                    heure = []
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)
                        
                    columns_2 = {'id_user': df_user['id_user'],col: df_user[col],"Systolic_value":systolic,"Diastolic_value":diastolic, 'Date': df_user['Date'],'Hour': df_user['Hour'],"Heure": heure}
                    df_blood_pressure = pd.DataFrame(columns_2)
                    df_min_max_agg = df_blood_pressure.groupby(df_blood_pressure["Heure"]).agg(['min', 'max'])
                    sys = df_min_max_agg["Systolic_value"]
                    dias = df_min_max_agg["Diastolic_value"]
                    
                    ############################# Sorting Date ###############################################

                    dataframe_sys_min_values = np.array(sys["min"])
                    dataframe_sys_max_values = np.array(sys["max"])
                    dataframe_dias_min_values = np.array(dias["min"])
                    dataframe_dias_max_values = np.array(dias["max"])
                    dataframe_index = np.array(sys.index)

                    # Create sorted values by date in a zip
                    zip_iterator = zip(dataframe_index, dataframe_sys_min_values, dataframe_sys_max_values,dataframe_dias_min_values,dataframe_dias_max_values)
                    sorted_zip = sorted(zip_iterator)

                    hour = []
                    columns_sys_min_values = []
                    columns_sys_max_values = []
                    columns_dias_min_values = []
                    columns_dias_max_values = []
                    my_xticks = []
                    for i in range(len(sorted_zip)):
                        hour.append(str(sorted_zip[i][0]).split(" ")[0])
                        columns_sys_min_values.append(float(sorted_zip[i][1]))
                        columns_sys_max_values.append(float(sorted_zip[i][2]))
                        columns_dias_min_values.append(float(sorted_zip[i][3]))
                        columns_dias_max_values.append(float(sorted_zip[i][4]))
                        d = str(sorted_zip[i][0]).split(" ")[0]

                    ############################################################################
                    
                    
                    fig = plt.figure()
                    x_max_min_sys_dias=np.array(hour)
                    y_max_sys=np.array(columns_sys_max_values)
                    y_min_sys=np.array(columns_sys_min_values)
                    y_max_dias=np.array(columns_dias_max_values)
                    y_min_dias=np.array(columns_dias_min_values)
                    ax = fig.add_subplot()
                    #ax.set_xticklabels(my_xticks,rotation=50)

                    if(col == "blood_pressure"):
                        plt.plot(x_max_min_sys_dias, y_max_dias, label = "max PS diastolique  par jours")
                        plt.plot(x_max_min_sys_dias, y_min_dias, label = "min PS diastolique  par jours")
                        plt.plot(x_max_min_sys_dias, y_min_sys, label = "min PS systolique  par jours")  
                        plt.plot(x_max_min_sys_dias, y_max_sys, label = "max PS systolique par jours")
                        img_title = " Evolution de la pression artérielle par jour"

                    else:
                        plt.plot(x_max_min_sys_dias, y_max_dias, label = "max PS diastolique  par jours")
                        plt.plot(x_max_min_sys_dias, y_min_dias, label = "min PS diastolique  par jours")
                        plt.plot(x_max_min_sys_dias, y_min_sys, label = "min PS systolique  par jours")  
                        plt.plot(x_max_min_sys_dias, y_max_sys, label = "max PS systolique par jours")
                        img_title = " Evolution du nombre de"+str(col)+" par jour"

                    plt.legend()
                    plt.gcf().set_size_inches(len(df_min_max_agg.index)+5,9)
                    img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_code
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()
                    return str("IMG:"+ path)
                
                
                else:
                    pass
            else:
                      
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]
                systolic = []
                diastolic = []
                for i in df_user[col]:
                    systolic.append(i.split("/")[0])
                    diastolic.append(i.split("/")[1])
                columns_2 = {'id_user': df_user['id_user'],col: df_user[col],"Systolic_value":systolic,"Diastolic_value":diastolic, 'Date': df_user['Date'],'Hour': df_user['Hour']}
                df_blood_pressure = pd.DataFrame(columns_2)
                df_min_max_agg = df_blood_pressure.groupby(df_blood_pressure["Date"]).agg(['min', 'max'])
                sys = df_min_max_agg["Systolic_value"]
                dias = df_min_max_agg["Diastolic_value"]

                ############################# Sorting Date ###############################################

                dataframe_sys_min_values = np.array(sys["min"])
                dataframe_sys_max_values = np.array(sys["max"])
                dataframe_dias_min_values = np.array(dias["min"])
                dataframe_dias_max_values = np.array(dias["max"])
                dataframe_index = np.array(sys.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_sys_min_values, dataframe_sys_max_values,dataframe_dias_min_values,dataframe_dias_max_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_sys_min_values = []
                columns_sys_max_values = []
                columns_dias_min_values = []
                columns_dias_max_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_sys_min_values.append(float(sorted_zip[i][1]))
                    columns_sys_max_values.append(float(sorted_zip[i][2]))
                    columns_dias_min_values.append(float(sorted_zip[i][3]))
                    columns_dias_max_values.append(float(sorted_zip[i][4]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                x_max_min_sys_dias=np.array(date)
                y_max_sys=np.array(columns_sys_max_values)
                y_min_sys=np.array(columns_sys_min_values)
                y_max_dias=np.array(columns_dias_max_values)
                y_min_dias=np.array(columns_dias_min_values)
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=50)

                if(col == "blood_pressure"):
                    plt.plot(x_max_min_sys_dias, y_max_dias, label = "max PS diastolique  par jours")
                    plt.plot(x_max_min_sys_dias, y_min_dias, label = "min PS diastolique  par jours")
                    plt.plot(x_max_min_sys_dias, y_min_sys, label = "min PS systolique  par jours")  
                    plt.plot(x_max_min_sys_dias, y_max_sys, label = "max PS systolique par jours")
                    img_title = " Evolution de la pression artérielle par jours"

                else:
                    plt.plot(x_max_min_sys_dias, y_max_dias, label = "max PS diastolique  par jours")
                    plt.plot(x_max_min_sys_dias, y_min_dias, label = "min PS diastolique  par jours")
                    plt.plot(x_max_min_sys_dias, y_min_sys, label = "min PS systolique  par jours")  
                    plt.plot(x_max_min_sys_dias, y_max_sys, label = "max PS systolique par jours")
                    img_title = " Evolution du nombre de"+str(col)+" par jours"

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()
                return str("IMG:"+ path)
    
    if (col == "heartbeat"):
        
        if(date_difference.days>8):
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
            
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                        
            columns_2 = {'id_user': df_user['id_user'],col: dataframe[col],'Date': df_user['Date'],'Hour': df_user['Hour'],"DayOfTheWeek": dayoftheweek}
            df_heartbeat = pd.DataFrame(columns_2)
            df_min_max_agg = df_heartbeat.groupby(df_heartbeat["DayOfTheWeek"]).agg(['min', 'max'])
            heart = df_min_max_agg[col]
            ############################# Sorting Date ###############################################

            dataframe_heartbeat_min_values = np.array(heart["min"])
            dataframe_heartbeat_max_values = np.array(heart["max"])

            dataframe_index = np.array(heart.index)

            # Create sorted values by date in a zip
            zip_iterator = zip(dataframe_index, dataframe_heartbeat_min_values, dataframe_heartbeat_max_values)
            sorted_zip = sorted(zip_iterator)

            date = []
            columns_min_values = []
            columns_max_values = []
            my_xticks = []
            
            for i in range(len(sorted_zip)):
                date.append(str(sorted_zip[i][0]).split(" ")[0])
                columns_min_values.append(float(sorted_zip[i][1]))
                columns_max_values.append(float(sorted_zip[i][2]))
                d = str(sorted_zip[i][0]).split(" ")[0]

           ############################################################################
            fig = plt.figure()
            x_max_min=np.array(date)
            y_max=np.array(columns_min_values)
            y_min=np.array(columns_max_values)

            ax = fig.add_subplot()
            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)

            if(col == "heartbeat"):
                plt.plot(x_max_min, y_max, label = "Nombre de battements par minutes maximums par jours")
                plt.plot(x_max_min, y_min, label = "Nombre de battements par minutes minimums par jours")
                
                img_title = " Evolution du nombre de battements par minute par jour de la semaine"

            else:
                plt.plot(x_max_min, y_max, label = "Nombre de battements par minutes maximums par jours")
                plt.plot(x_max_min, y_min, label = "Nombre de battements par minutes minimums par jours")

                img_title = " Evolution du nombre de"+str(col)+" par jour"

            plt.legend()
            plt.gcf().set_size_inches(len(date)+5,9)
            img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_code
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            return str("IMG:"+ path) 
            
            pass
        else:
            if(date_difference.days==0):
                if(hours_difference <= 23):
                   
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]
                    
                    heure=[]
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: df_user[col], 'Date': df_user['Date'],'Hour': df_user['Hour'],"Heure":heure}
                    df_sum = pd.DataFrame(columns_2)
                    
                    df_min_max_agg = df_sum.groupby(df_sum["Heure"]).agg(['min', 'max'])
                    df_heart = df_min_max_agg[col]
                    
                    ############################# Sorting Date ###############################################

                    dataframe_min_values = np.array(df_heart["min"])
                    dataframe_max_values = np.array(df_heart["max"])
                    dataframe_index = np.array(df_heart.index)

                    # Create sorted values by date in a zip
                    zip_iterator = zip(dataframe_index, dataframe_min_values, dataframe_max_values)
                    sorted_zip = sorted(zip_iterator)

                    hour = []
                    columns_min_values = []
                    columns_max_values = []
                    my_xticks = []
                    for i in range(len(sorted_zip)):
                        hour.append(str(sorted_zip[i][0]).split(" ")[0])
                        columns_min_values.append(float(sorted_zip[i][1]))
                        columns_max_values.append(float(sorted_zip[i][2]))
                        d = str(sorted_zip[i][0]).split(" ")[0]
                        #my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                    ############################################################################
                    
                    fig = plt.figure()
                    x_max=np.array(hour)
                    y_max=np.array(columns_max_values)
                    x_min=np.array(hour)
                    y_min=np.array(columns_min_values)
                    ax = fig.add_subplot()
                    
                    if(col == "heartbeat"):
                        plt.plot(x_max, y_max, label = "Nombre maximum battements par minutes/ par heures ")
                        plt.plot(x_min, y_min, label = "Nombre minimum battements par minutes/ par heures ")
                        img_title = " Evolution des battements par minutes par heures"

                    else:
                        plt.plot(x_max, y_max, label = "Nombre maximum battements par minutes/ par heures ")
                        plt.plot(x_min, y_min, label = "Nombre minimum battements par minutes/ par heures ")
                        img_title = " Evolution du nombre de"+str(col)+" par heures"

                    plt.legend()
                    plt.gcf().set_size_inches(len(hour)+5,9)
                    img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()

                    return str("IMG:"+ path)

                else:
                    print(hours_difference)
                    pass
            else:
        
                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]
                df_min_max_agg = df_user.groupby(df_user["Date"]).agg(['min', 'max'])
                df_temp = df_min_max_agg[col]

                ############################# Sorting Date ###############################################

                dataframe_min_values = np.array(df_temp["min"])
                dataframe_max_values = np.array(df_temp["max"])
                dataframe_index = np.array(df_temp.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_min_values, dataframe_max_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_min_values = []
                columns_max_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_min_values.append(float(sorted_zip[i][1]))
                    columns_max_values.append(float(sorted_zip[i][2]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                x_max=np.array(date)
                y_max=np.array(columns_max_values)
                x_min=np.array(date)
                y_min=np.array(columns_min_values)
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=60)

                if(col == "heartbeat"):
                    plt.plot(x_max, y_max, label = "valeurs maximales par jours ")
                    plt.plot(x_min, y_min, label = "valeurs minimales par jours ")
                    img_title = " Evolution du nombre de battements par minutes par jours"
                else:
                    plt.plot(x_max, y_max, label = "valeurs maximales par jours ")
                    plt.plot(x_min, y_min, label = "valeurs minimales par jours ")
                    img_title = " Evolution du nombre de"+str(col)+" par jours"

                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()

                return str("IMG:"+ path)
        
    else:
        if(date_difference.days>8):
            
            columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
            df_number = pd.DataFrame(columns)
            df_user = df_number[(df_number['id_user'] == id_user)]
                
            dayoftheweek = []
            for i in df_user["Date"]:
                temp = pd.Timestamp(i)
                if (temp.day_name() == 'Monday'):
                    dayoftheweek.append('1')
                if (temp.day_name() == 'Tuesday'):
                    dayoftheweek.append('2')
                if (temp.day_name() == 'Wednesday'):
                    dayoftheweek.append('3')
                if (temp.day_name() == 'Thursday'):
                    dayoftheweek.append('4')
                if (temp.day_name() == 'Friday'):
                    dayoftheweek.append('5')
                if (temp.day_name() == 'Saturday'):
                    dayoftheweek.append('6')
                if (temp.day_name() == 'Sunday'):
                    dayoftheweek.append('7')
                        
            columns_2 = {'id_user': df_user['id_user'],col: df_user[col],'Date': df_user['Date'],'Hour': df_user['Hour'],"DayOfTheWeek": dayoftheweek}
            df_heartbeat = pd.DataFrame(columns_2)
            
            df_group = df_heartbeat.groupby(df_heartbeat["DayOfTheWeek"]).sum()
            
            columns_values = pd.to_numeric(df_group[col].values)
            day_of_week = df_group.index
                           
            fig = plt.figure()
            ax = fig.add_subplot()
            x=np.array(day_of_week)
            y=np.array(columns_values)

            my_xticks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            ax.set_xticklabels(my_xticks,rotation=50)
            if(col == "steps"):
                plt.plot(x,y,marker="o",label = "Nombre de pas par jours")
                img_title = " Evolution du nombre de pas par jours"
            plt.legend()
            plt.gcf().set_size_inches(len(day_of_week)+5,9)
            img_code = "graph_evolution_number_calories"+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
            fig.suptitle(img_title, fontsize=16)
            #path = "Graphes/user_"+str(id_user)+"/"+img_title
            path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
            fig.savefig(path)
            plt.close()
            #return "moyenne by day"
            return str("IMG:"+ path)
            
        else:
            if(date_difference.days==0):
                if(hours_difference <= 23):
                    
                    columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                    df_number = pd.DataFrame(columns)
                    df_user = df_number[(df_number['id_user'] == id_user)]
                    
                    heure=[]
                    for i in df_user["Hour"]:
                        h = i.split(':')[0]
                        heure.append(h)

                    columns_2 = {'id_user': df_user['id_user'],col: df_user[col], 'Date': df_user['Date'],'Hour': df_user['Hour'],"Heure":heure}
                    df_sum = pd.DataFrame(columns_2)
                    
                    df_sum = df_sum.groupby(df_sum["Heure"]).sum()
                    df_steps = df_sum[col]
                    
                    ############################# Sorting Date ###############################################

                    dataframe_values = np.array(df_steps.values)
                    dataframe_index = np.array(df_sum.index)

                    # Create sorted values by date in a zip
                    zip_iterator = zip(dataframe_index, dataframe_values)
                    sorted_zip = sorted(zip_iterator)

                    hour = []
                    columns_values = []
                    my_xticks = []
                    for i in range(len(sorted_zip)):
                        hour.append(str(sorted_zip[i][0]).split(" ")[0])
                        columns_values.append(float(sorted_zip[i][1]))
                        
                        d = str(sorted_zip[i][0]).split(" ")[0]
                        #my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                    ############################################################################
                    
                    fig = plt.figure()
                    x=np.array(hour)
                    y=np.array(columns_values)
                    ax = fig.add_subplot()
                    
                    if(col == "steps"):
                        plt.plot(x,y,marker="o",label = "Nombre de pas par heures")
                        img_title = " Evolution du nombre de pas par heures"
                    else:
                        plt.plot(x,y,marker="o",label = "Nombre de"+str(col)+" par heures")
                        img_title = " Evolution du nombre de"+str(col)+" par heures"

                    plt.legend()
                    plt.gcf().set_size_inches(len(hour)+5,9)
                    img_code = "graph_evolution_number"+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                    fig.suptitle(img_title, fontsize=16)
                    #path = "Graphes/user_"+str(id_user)+"/"+img_title
                    path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                    fig.savefig(path)
                    plt.close()

                    return str("IMG:"+ path)
                else:
                    pass

            else:

                columns = {'id_user': dataframe['iduser'],col: dataframe[col], 'Date': dataframe['date'],'Hour': dataframe['hour']}
                df_number = pd.DataFrame(columns)
                df_user = df_number[(df_number['id_user'] == id_user)]
                df_group = df_user.groupby(df_user["Date"]).sum()
                df_group.sort_index(ascending=False)
                columns_values_by_dates = pd.to_numeric(df_group[col].values)
                dates = df_group.index

                 ############################# Sorting Date ###############################################

                dataframe_values = np.array(df_group[col])
                dataframe_index = np.array(df_group.index)

                # Create sorted values by date in a zip
                zip_iterator = zip(pd.to_datetime(dataframe_index,format = '%d-%m-%Y'), dataframe_values)
                sorted_zip = sorted(zip_iterator)

                date = []
                columns_values = []
                my_xticks = []
                for i in range(len(sorted_zip)):
                    date.append(str(sorted_zip[i][0]).split(" ")[0])
                    columns_values.append(float(sorted_zip[i][1]))
                    d = str(sorted_zip[i][0]).split(" ")[0]
                    my_xticks.append(datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y"))

                ############################################################################

                fig = plt.figure()
                x=np.array(date)
                y=np.array(columns_values)
                ax = fig.add_subplot()
                ax.set_xticklabels(my_xticks,rotation=50)
                if(col == "steps"):
                    plt.plot(x,y,marker="o",label = "Nombre de pas par jours")
                    img_title = " Evolution du nombre de pas par jours"
                else:
                    plt.plot(x,y,marker="o",label = "Nombre de"+str(col)+" par jours")
                    img_title = " Evolution du nombre de"+str(col)+" par jours"
                plt.legend()
                plt.gcf().set_size_inches(len(date)+5,9)
                img_code = "graph_evolution_number "+str(col)+"_"+str(now.strftime("%d-%m-%Y_%H%M%S"))+".png"
                fig.suptitle(img_title, fontsize=16)
                #path = "Graphes/user_"+str(id_user)+"/"+img_code
                path = "Traitement_Data/Graphes/user_"+str(id_user)+"/"+img_code
                fig.savefig(path)
                plt.close()

                return str("IMG:"+ path)


# # Fonction principale retournant les résultats souhaités pour chaque utilisateurs

# In[205]:


def actions(analyse,colonnes,debut,fin,id_user):
    
    s3 = boto3.client('s3', aws_access_key_id='AKIAXENTS6UZG2MIL4GG',aws_secret_access_key='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', region_name='eu-west-3')
    d1 = debut.split(" ")[0]
    d2 = fin.split(" ")[0]
    h1 = debut.split(" ")[1]
    h2 = fin.split(" ")[1]
    
    #day,month,year d1
    day1 = int(d1.split("-")[0])
    month1 = int(d1.split("-")[1])
    year1 = int(d1.split("-")[2])

    #day,month,year d2
    day2 = int(d2.split("-")[0])
    month2 = int(d2.split("-")[1])
    year2 = int(d2.split("-")[2])

    sdate = date(year1, month1, day1)   # start date
    edate = date(year2, month2, day2)   # end date

    delta = edate - sdate       # as timedelta
    #print(delta)
    list_dates = []
    # Récuperation des dates de la periode donnée en paramètre
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        list_dates.append(str(day.strftime("%d-%m-%Y")))

    liste = []

    # Récuperation des données datant de la periode sélectionné
    for i in list_dates:
        s3_file_key = str(id_user)+'/health/'+i+'/health_data.csv'
        bucket = 's3fakewatch'
        #print(s3_file_key)
        obj = s3.get_object(Bucket=bucket, Key=s3_file_key)
        initial_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        liste.append(initial_df)

    frame = pd.concat(liste, axis=0, ignore_index=True)
    frame.to_csv (r'health_data_finale.csv', index = False, header=True)
    
    # Récuperation des données datant de l'heure périodique sélectionné
    first_position = 0
    for i in frame.itertuples():
        if (i.date == d1 and i.hour == h1):
            #print(i,first_position)
            break;
        first_position = first_position + 1
        
    last_position = 0
    for i in frame.itertuples():
        if (i.date == d2 and i.hour == h2):
            #print(i,last_position)
            break;
        last_position = last_position + 1 
    
    final_dataframe = frame.loc[first_position:last_position]
    #display(final_dataframe)
    
    if not os.path.exists("Traitement_Data/Graphes/user_"+str(id_user)):
        os.makedirs("Traitement_Data/Graphes/user_"+str(id_user),exist_ok = True)        
    else:
        pass
        
    if analyse =='average':
        if colonnes in ['heartbeat','calories','steps','temperature','blood_pressure'] :
            return average(final_dataframe,colonnes,debut,fin,id_user)
        if colonnes == "IMC":
            return average_IMC(final_dataframe,id_user)
        else: 
            return "Colonnes de données non existantes"
    if analyse =='number':
        if colonnes in ['heartbeat','calories','steps','temperature','blood_pressure']  :
            return number(final_dataframe,colonnes,debut,fin,id_user)
        if colonnes == "VMA":
            return VMA(final_dataframe,debut,fin,id_user)
        if colonnes == "IMC":
            return IMC(final_dataframe,id_user)
        else: 
            return "Colonnes de données non existantes"
    if analyse =='evolution_average':
        if colonnes in ['heartbeat','calories','steps','temperature','blood_pressure'] :
            return evolution_average(final_dataframe,colonnes,debut,fin,id_user)
        if (colonnes == 'IMC'):
            return evolution_average_IMC(final_dataframe,id_user)
        if (colonnes == 'VMA'):
            return evolution_average_VMA(final_dataframe,id_user)
        else: 
            return "Colonnes de données non existantes"
    if analyse =='evolution_number':
        if colonnes in ['heartbeat','calories','steps','temperature','blood_pressure'] :
            return evolution_number(final_dataframe,colonnes,debut,fin,id_user)
        if (colonnes == 'IMC'):
            return evolution_number_IMC(final_dataframe,id_user)
        if (colonnes == 'VMA'):
            return evolution_number_VMA(final_dataframe,id_user)
        else: 
            return "Colonnes de données non existantes"
    """if analyse =='':
        if colonnes == "Dataframe":
            return final_dataframe"""



