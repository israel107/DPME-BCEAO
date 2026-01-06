import pandas as pd
import panel as pn
pn.extension('tabulator')
from io import BytesIO
import concurrent.futures

import io
# Importation des librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import panel as pn
from io import BytesIO
import holoviews as hv
import hvplot.pandas
import io

# Extension Panel
pn.extension('tabulator')

hv.extension('bokeh')
pn.extension()


from datetime import datetime
import datetime as dt



#initialisation à 0
pme_type = []
dates_list = []


# Etape 0 : Listes ne dépendant pas de df
# La liste des pays est supposée constante avec UEMOA
country_list = ['Benin', 'Burkina', "Côte d'Ivoire", 'Guinée Bissau', 'Mali', 'Niger', 'Sénégal', 'Togo', 'UEMOA']
# La liste des formes à affichier dans le graphique de la page 1 a été choisie manuellement
liste_forme_g =sorted(['Crédits nets','Crédits à long terme', 'Crédits à court terme','Crédits à moyen terme','Crédit de location-financement',
                'Affacturage'])


# Etape 1 : Gestion des widgets 
##############################################################################################################################
#--------------------------------------- GESTION DES WIDGETS-----------------------------------------------------------------#
##############################################################################################################################





# Choix du pays
select_country = pn.widgets.Select(name='Selectionner un pays', options= country_list,styles={'font-size': '18px'})
# Choix de la date du financement global

select_type = pn.widgets.Select(name="Sélectionner le type de financement PME", options=pme_type,styles={'font-size': '18px'})
# Sélection de la forme de l'encours ( dans libelle poste) générale
date_select = pn.widgets.Select(name="Sélectionner une date", options=dates_list,styles={'font-size': '18px'})
# Sélection du type de pme financée
forme_g_select = pn.widgets.Select(name = "Choix de la forme de l'Encours Global ", options = liste_forme_g)
#Icone de chargement de la page !
loading_spinner = pn.indicators.LoadingSpinner(value=True, width=100, height=100)
#Icone chargement du graphe 2 !
graph_spinner = pn.widgets.LoadingSpinner(value=True, width=30, height=50)

credit_display = pn.pane.HTML("", width=350)
aft_display = pn.pane.HTML("", width=350)
cb_display = pn.pane.HTML("", width=350)
csb_display = pn.pane.HTML("", width=350)
taux_degradation_display = pn.pane.HTML("", width=350)
titres_display = pn.pane.HTML("", width=350)
total_titres_display = pn.pane.HTML("", width=350)
lt_display = pn.pane.HTML("",width=350)
mt_display= pn.pane.HTML("",width=350)
ct_display= pn.pane.HTML("",width=350)
prop_aff_display = pn.pane.HTML("",width=375)
prop_cb_display = pn.pane.HTML("",width = 375)

taux_credit_pme_display = pn.pane.HTML("",width =350)
prop_aff_pme_display = pn.pane.HTML("", width=350)
prop_cb_pme_display = pn.pane.HTML("",width =350)
credit_pme_display = pn.pane.HTML("", width=350)
aft_pme_display = pn.pane.HTML("", width=350)
cb_pme_display = pn.pane.HTML("", width=350)
csb_pme_display = pn.pane.HTML("", width=350)
lt_pme_display = pn.pane.HTML("", width=350)
mt_pme_display = pn.pane.HTML("", width=350)
taux_degra_pme_display =  pn.pane.HTML("",width = 375)


##################---------------------- WIDGETS POUR LA PAGE 1 ------------------------------------####################################
credit_var = pn.widgets.MultiChoice(name='Choix des indicateurs Globaux', value=['Encours Global Crédit'],styles={'font-size': '16px'},
                                    options=['Encours Global Crédit','Encours Global Aft','Encours Global Crédit-Bail','Encours Global Créance en souffrance','Encours Global Crédit Long Terme','Encours Global Crédit Moyen Terme','Encours Global Crédit Court Terme'])


periodicity = pn.widgets.Select(name='Periodicity', options=['Mensuelle', 'Trimestrielle', 'Annuelle'],styles={'font-size': '16px'})
start_date_picker = pn.widgets.DatePicker(name='Date de Début', value=pd.to_datetime('2018-01-31'),styles={'font-size': '16px'})
end_date_picker = pn.widgets.DatePicker(name='Date de Fin', value=pd.to_datetime('2024-03-31'),styles={'font-size': '16px'})

var_pme =pn.widgets.MultiChoice(name='Choix des indicateurs PME', value=['Encours Crédit PME'],styles={'font-size': '16px'},
                                    options=['Encours Crédit PME','Encours Aft PME','Encours Crédit-Bail PME','Encours Créance en Souffrance PME','Encours Crédit Long Terme PME','Encours Crédit Moyen Terme PME'])




# Etape 2 : Ecrire toutes les fonctions ne dépendant pas de df 



def encours_poste(dfu,pays,date):
    try:
        df_pays=dfu[dfu['Libelle Pays']==pays]
        date_selected =pd.to_datetime(date)
        #df_pays_lastdate trouve la ligne avec la date la plus proche qui est <= à celle choisie
        df_pays_lastdate = df_pays[df_pays['Arrete']<=date_selected]
        if not df_pays_lastdate.empty:
            max_date =df_pays_lastdate['Arrete'].max()
            somme_encours= df_pays_lastdate[df_pays_lastdate['Arrete']== max_date]['Valeurn'].sum()
            return somme_encours
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans encours_poste: {e}")
        return 0
#Fonction pour calculer l'encours total des crédits
def rapport (titre1,titre2,titre3, denominateur) :
    try :
        total_titres = titre1+titre2+titre3
        if denominateur >0 :
            return (total_titres/denominateur)*100
        else :
            return 0
    except AssertionError as e :
        print(f"Problème dans la fonction rappor : {e}")
        return 0
def total_titres_affiche(titre1,titre2,titre3) :
    try :
        return titre1+titre2+titre3
    except AssertionError as e :
        print(f"Problème dans la fonction d'affichage du total des titres : {e}")
        return 0

def percent_encours(num,deno1, deno2):
    try:
        total = deno1 + deno2
        if total > 0:  # Évite la division par zéro
            return (num / total) * 100
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans percent_encours: {e}")
        return 0

def encours_uemoa (dfu,date) :
    try:
        date_selected = pd.to_datetime(date)
        df_last_date = dfu[dfu['Arrete'] <= date_selected]
        if not df_last_date.empty :
            max_date = df_last_date['Arrete'].max()
            somme_uemoa_encours= df_last_date[df_last_date['Arrete']== max_date]['Valeurn'].sum()
            return somme_uemoa_encours
        else : 
            return 0
    except AssertionError as e : 
        print(f"Erreur dans encours_uemoa: {e}")
        return 0

############################----------------------- REPARTITION GLOBALE DU CREDIT LT-MT-CT---------------------#########################
#encours_g_lt_uemoa
def encours_g_lt_fpays(df_g_lt,pays,date):
    try:
        date_selected = pd.to_datetime(date)
        df_filtered=df_g_lt[(df_g_lt['Libelle Pays']==pays) & (df_g_lt['Arrete'] == date_selected )]        
        if not df_filtered.empty:
            result = df_filtered['Valeurn'].sum()
            return result
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans Credit LT Global: {e}")
        return 0
#encours_g_lt_filtrable par pays
def encours_g_lt_pays(df_g_lt,date):
    try:
        date_selected = pd.to_datetime(date)
        df_filtered=df_g_lt[ (df_g_lt['Arrete'] == date_selected )]        
        if not df_filtered.empty:
            result = df_filtered['Valeurn'].sum()
            return result
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans Credit LT Global: {e}")
        return 0
###################################################################-----MOYEN TERME------------############################
def encours_g_mt_fpays(df_g_mt,pays,date):
    try:
        date_selected = pd.to_datetime(date)
        df_filtered=df_g_mt[(df_g_mt['Libelle Pays']==pays) & (df_g_mt['Arrete'] == date_selected )]        
        if not df_filtered.empty:
            result = df_filtered['Valeurn'].sum()
            return result
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans Credit LT Global: {e}")
        return 0

def encours_g_mt_pays(df_g_mt,date):
    try:
        date_selected = pd.to_datetime(date)
        df_filtered=df_g_mt[(df_g_mt['Arrete'] == date_selected )]        
        if not df_filtered.empty:
            result = df_filtered['Valeurn'].sum()
            return result
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans Credit LT Global: {e}")
        return 0

#####################################------------------------Court TERME------------------------######################
def encours_g_ct_fpays(df_g_ct,pays,date):
    try:
        date_selected = pd.to_datetime(date)
        df_filtered=df_g_ct[(df_g_ct['Libelle Pays']==pays) & (df_g_ct['Arrete'] == date_selected )]        
        if not df_filtered.empty:
            result = df_filtered['Valeurn'].sum()
            return result
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans Credit LT Global: {e}")
        return 0

def encours_g_ct_pays(df_g_ct,date):
    try:
        date_selected = pd.to_datetime(date)
        df_filtered=df_g_ct[(df_g_ct['Arrete'] == date_selected )]        
        if not df_filtered.empty:
            result = df_filtered['Valeurn'].sum()
            return result
        else :
            return 0

    except AssertionError as e : 
        print(f"Erreur dans Credit LT Global: {e}")
        return 0
# --------------------------------------------------------------DATAFRAME PME---------------------------------------------------------------------- 
##################################----------------------- CREDIT NET-----------------------------------##########################################
#Filtré par pays et Filtré par type
def encours_pme_credit_fpays_ftype(df_pme_credit, pays, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_credit[
            (df_pme_credit['Libelle Pays'] == pays) &
            (df_pme_credit['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_credit['Libelle Colonne'] == type_financement)
        ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
#Financement Global mais filtré par pays
def encours_pme_credit_fpays_type(df_pme_credit, pays, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_credit[
            (df_pme_credit['Libelle Pays'] == pays) &
            (df_pme_credit['Arrete'] <= pd.to_datetime(date)) ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
#Uemoa mais filtré par type
def encours_pme_credit_pays_ftype(df_pme_credit, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_credit[
            (df_pme_credit['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_credit['Libelle Colonne'] == type_financement)]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
# UEMOA + Financement Global
def encours_pme_credit_pays_type(df_pme_credit, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_credit[
            (df_pme_credit['Arrete'] <= pd.to_datetime(date)) ]
       
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
 
        return 0
##################################----------------------- AFFACTURAGE-----------------------------------##########################################
# Filtré par pays et par Type de financement
def encours_pme_aft_fpays_ftype(df_pme_aft, pays, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_aft[
            (df_pme_aft['Libelle Pays'] == pays) &
            (df_pme_aft['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_aft['Libelle Colonne'] == type_financement)
        ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
#Financement Global mais filtré par pays
def encours_pme_aft_fpays_type(df_pme_aft, pays, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_aft[
            (df_pme_aft['Libelle Pays'] == pays) &
            (df_pme_aft['Arrete'] <= pd.to_datetime(date)) ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
#Uemoa mais filtré par type
def encours_pme_aft_pays_ftype(df_pme_aft, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_aft[
            (df_pme_aft['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_aft['Libelle Colonne'] == type_financement)]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
# UEMOA + Financement Global
def encours_pme_aft_pays_type(df_pme_aft, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_aft[
            (df_pme_aft['Arrete'] <= pd.to_datetime(date)) ]
       
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
 
        return 0

##################################----------------------- CREDIT-BAIL-----------------------------------##########################################
# Filtré par pays et par Type de financement
def encours_pme_cb_fpays_ftype(df_pme_cb, pays, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_cb[
            (df_pme_cb['Libelle Pays'] == pays) &
            (df_pme_cb['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_cb['Libelle Colonne'] == type_financement)
        ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
#Financement Global mais filtré par pays
def encours_pme_cb_fpays_type(df_pme_cb, pays, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_cb[
            (df_pme_cb['Libelle Pays'] == pays) &
            (df_pme_cb['Arrete'] <= pd.to_datetime(date)) ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0

#Uemoa mais filtré par type
def encours_pme_cb_pays_ftype(df_pme_cb, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_cb[
            (df_pme_cb['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_cb['Libelle Colonne'] == type_financement)]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
# UEMOA + Financement Global
def encours_pme_cb_pays_type(df_pme_cb, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_cb[
            (df_pme_cb['Arrete'] <= pd.to_datetime(date)) ]
       
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
 
        return 0
##################################----------------------- CREANCES EN SOUFFRANCE-----------------------------------##########################################
# Filtré par pays et par Type de financement
def encours_pme_csb_fpays_ftype(df_pme_csb, pays, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_csb[
            (df_pme_csb['Libelle Pays'] == pays) &
            (df_pme_csb['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_csb['Libelle Colonne'] == type_financement)
        ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
#Financement Global mais filtré par pays
def encours_pme_csb_fpays_type(df_pme_csb, pays, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_csb[
            (df_pme_csb['Libelle Pays'] == pays) &
            (df_pme_csb['Arrete'] <= pd.to_datetime(date)) ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0

#Uemoa mais filtré par type
def encours_pme_csb_pays_ftype(df_pme_csb, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_csb[
            (df_pme_csb['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_csb['Libelle Colonne'] == type_financement)]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
# UEMOA + Financement Global
def encours_pme_csb_pays_type(df_pme_csb, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_csb[
            (df_pme_csb['Arrete'] <= pd.to_datetime(date)) ]
       
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
 
        return 0
################################-----------------------REPARTITION LT DU CREDIT PME----------------------------------######################################
# Filtré par pays et par Type de financement
def encours_pme_lt_fpays_ftype(df_pme_lt, pays, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_lt[
            (df_pme_lt['Libelle Pays'] == pays) &
            (df_pme_lt['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_lt['Libelle Colonne'] == type_financement)
        ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0

#Financement Global mais filtré par pays
def encours_pme_lt_fpays_type(df_pme_lt, pays, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_lt[
            (df_pme_lt['Libelle Pays'] == pays) &
            (df_pme_lt['Arrete'] <= pd.to_datetime(date)) ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0

#Uemoa mais filtré par type
def encours_pme_lt_pays_ftype(df_pme_lt, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_lt[
            (df_pme_lt['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_lt['Libelle Colonne'] == type_financement)]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
# UEMOA + Financement Global
def encours_pme_lt_pays_type(df_pme_lt, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_lt[
            (df_pme_lt['Arrete'] <= pd.to_datetime(date)) ]
       
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
 
        return 0
################################-----------------------REPARTITION MT DU CREDIT PME----------------------------------######################################
# Filtré par pays et par Type de financement
def encours_pme_mt_fpays_ftype(df_pme_mt, pays, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_mt[
            (df_pme_mt['Libelle Pays'] == pays) &
            (df_pme_mt['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_mt['Libelle Colonne'] == type_financement)
        ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0

#Financement Global mais filtré par pays
def encours_pme_mt_fpays_type(df_pme_mt, pays, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_mt[
            (df_pme_mt['Libelle Pays'] == pays) &
            (df_pme_mt['Arrete'] <= pd.to_datetime(date)) ]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0

#Uemoa mais filtré par type
def encours_pme_mt_pays_ftype(df_pme_mt, date, type_financement):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_mt[
            (df_pme_mt['Arrete'] <= pd.to_datetime(date)) &
            (df_pme_mt['Libelle Colonne'] == type_financement)]
        
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
        return 0
# UEMOA + Financement Global
def encours_pme_mt_pays_type(df_pme_mt, date):
    try:
        date_selected =pd.to_datetime(date)
        df_filtered = df_pme_mt[
            (df_pme_mt['Arrete'] <= pd.to_datetime(date)) ]
       
        if not df_filtered.empty:
            max_date = df_filtered['Arrete'].max()
            result = df_filtered[df_filtered['Arrete'] == max_date]['Valeurn'].sum()
            return result
        else:
            return 0
    except AssertionError as e:
        print(f"Erreur dans encours_pme: {e}")
 
        return 0
############################################---------------------FONCTION-SHOW-ENCOURS-----------------------###########################################

def show_encours (pays,date,select_type):
    try :
        date_selected = pd.to_datetime(date)
        
        
        if pays == 'UEMOA' :
            
            result_encours_credit= encours_uemoa(df_g_credit, date_selected)
            result_encours_aft = encours_uemoa(df_g_aft, date_selected)
            result_encours_cb =encours_uemoa(df_g_cb,date_selected)
            result_encours_csb = encours_uemoa(df_g_csb,date_selected)
            result_total_depreciation = encours_uemoa(df_g_depreciation,date_selected)
            resultat_total_emplois = encours_uemoa(df_g_emplois,date_selected)
            resultat_titre1 = encours_uemoa(df_g_titres[df_g_titres['Libelle Poste']=='Titres d investissement'],date_selected)
            resultat_titre2 = encours_uemoa(df_g_titres[df_g_titres['Libelle Poste']=='Titres de transaction'],date_selected)
            resultat_titre3 = encours_uemoa(df_g_titres[df_g_titres['Libelle Poste']=='Titres de placement et titres de l activité de portefeuille'],date_selected)
            result_encours_lt = encours_g_lt_pays(df_g_lt,date_selected)
            result_encours_mt = encours_g_mt_pays(df_g_mt,date_selected)
            result_encours_ct = encours_g_ct_pays(df_g_ct,date_selected)
            #result_taux_degra_pme = degra_pme_uemoa(data_comb_uemoa,date_selected)
            
            
            if select_type =='Financement Global' :
                result_encours_credit_pme = encours_pme_credit_pays_type(df_pme_credit,date_selected)
                result_encours_aft_pme = encours_pme_aft_pays_type(df_pme_aft,date_selected)
                result_encours_cb_pme = encours_pme_cb_pays_type(df_pme_cb,date_selected)
                result_encours_csb_pme = encours_pme_csb_pays_type(df_pme_csb,date_selected)
                result_encours_lt_pme = encours_pme_lt_pays_type(df_pme_lt, date_selected)
                result_encours_mt_pme = encours_pme_mt_pays_type(df_pme_mt, date_selected)
                
            else : 
                result_encours_credit_pme = encours_pme_credit_pays_ftype(df_pme_credit, date_selected, select_type)
                result_encours_aft_pme = encours_pme_aft_pays_ftype(df_pme_aft, date_selected, select_type)
                result_encours_cb_pme = encours_pme_cb_pays_ftype(df_pme_cb, date_selected, select_type)
                result_encours_csb_pme = encours_pme_csb_pays_ftype(df_pme_csb, date_selected, select_type)
                result_encours_lt_pme = encours_pme_lt_pays_ftype(df_pme_lt,date_selected,select_type)
                result_encours_mt_pme = encours_pme_mt_pays_ftype(df_pme_mt,date_selected,select_type)
               
        else : 
            result_encours_credit= encours_poste(df_g_credit,pays, date_selected)
            result_encours_aft = encours_poste(df_g_aft,pays, date_selected)
            result_encours_cb = encours_poste(df_g_cb,pays,date_selected)
            result_encours_csb = encours_poste(df_g_csb,pays,date_selected)
            result_total_depreciation = encours_poste(df_g_depreciation,pays,date_selected)
            resultat_total_emplois = encours_poste(df_g_emplois,pays,date_selected)
            
            resultat_titre1 = encours_poste(df_g_titres[df_g_titres['Libelle Poste']=='Titres d investissement'],pays,date_selected)
            resultat_titre2 = encours_poste(df_g_titres[df_g_titres['Libelle Poste']=='Titres de transaction'],pays,date_selected)
            resultat_titre3 = encours_poste(df_g_titres[df_g_titres['Libelle Poste']=='Titres de placement et titres de l activité de portefeuille'],pays,date_selected)
            
            result_encours_lt = encours_g_lt_fpays(df_g_lt,pays,date_selected)
            result_encours_mt = encours_g_mt_fpays(df_g_mt,pays,date_selected)
            result_encours_ct = encours_g_ct_fpays(df_g_ct,pays,date_selected)
            #result_taux_degra_pme = degra_pme_pays(data_comb_pays,date_selected,pays)
            
            if select_type =='Financement Global' :
                result_encours_credit_pme = encours_pme_credit_fpays_type(df_pme_credit,pays,date_selected)
                result_encours_aft_pme = encours_pme_aft_fpays_type(df_pme_aft,pays,date_selected)
                result_encours_cb_pme = encours_pme_cb_fpays_type(df_pme_cb,pays,date_selected)
                result_encours_csb_pme = encours_pme_csb_fpays_type(df_pme_csb,pays,date_selected)
                result_encours_lt_pme = encours_pme_lt_fpays_type(df_pme_lt, pays, date_selected)
                result_encours_mt_pme = encours_pme_mt_fpays_type(df_pme_mt, pays, date_selected)
                
            else : 
                result_encours_credit_pme = encours_pme_credit_fpays_ftype(df_pme_credit,pays, date_selected, select_type)
                result_encours_aft_pme = encours_pme_aft_fpays_ftype(df_pme_aft,pays, date_selected, select_type)
                result_encours_cb_pme = encours_pme_cb_fpays_ftype(df_pme_cb,pays, date_selected, select_type)
                result_encours_csb_pme = encours_pme_csb_fpays_ftype(df_pme_csb,pays, date_selected, select_type)
                result_encours_lt_pme = encours_pme_lt_fpays_ftype(df_pme_lt,pays,date_selected,select_type)
                result_encours_mt_pme = encours_pme_mt_fpays_ftype(df_pme_mt,pays,date_selected,select_type)
        credit_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global de Crédits</span>: {result_encours_credit:,.0f}"
        aft_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global de l'Affacturage</span> : {result_encours_aft:,.0f}"
        cb_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global du Crédit-Bail</span> : {result_encours_cb:,.0f}"
        csb_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global des Créances en Souffrance</span> : {result_encours_csb:,.0f}"

        degra_value = percent_encours(result_encours_csb, result_encours_credit, result_total_depreciation)
        taux_degradation_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Taux de dégradation du portefeuille</span> : {degra_value:.2f}%"

        propor_titres_value = rapport(resultat_titre1, resultat_titre2, resultat_titre3, resultat_total_emplois)
        titres_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Proportion des titres dans les emplois de la banque</span> : {propor_titres_value:.2f}%"
        
        lt_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global de Crédits Long terme</span>: {result_encours_lt:,.0f}"
        mt_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global de Crédits Moyen terme</span>: {result_encours_mt:,.0f}"
        ct_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Global de Crédits Court terme</span>: {result_encours_ct:,.0f}"

        prop_aff_pme = rapport(result_encours_aft_pme,0,0,result_encours_credit_pme)
        prop_aff_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'> Poids de l'Affacturage dans les Crédits PME</span> : {prop_aff_pme:.2f}%"
        prop_cb_pme= rapport(result_encours_cb_pme,0,0,result_encours_credit_pme)
        prop_cb_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'> Poids du Crédit-Bail dans les Crédits PME</span> : {prop_cb_pme:.2f}%"

        taux_credit_pme= rapport(result_encours_credit_pme,0,0,result_encours_credit)
        taux_credit_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'> Poids des Crédits PME dans les Crédits Globaux </span> : {taux_credit_pme:.2f}%"

        prop_aff = rapport(result_encours_aft,0,0,result_encours_credit)
        prop_aff_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'> Poids de l'Affacturage dans les Crédits Globaux </span> : {prop_aff:.2f}%"
        prop_cb = rapport(result_encours_cb,0,0,result_encours_credit)
        prop_cb_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'> Poids du Crédit-Bail dans les Crédits Globaux </span> : {prop_cb:.2f}%"
        
        
        
        result_total_titres = total_titres_affiche(resultat_titre1, resultat_titre2, resultat_titre3)
        total_titres_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours des Titres d'investissement</span> : {result_total_titres:,.0f}"

        aft_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours Affacturage PME</span> : {result_encours_aft_pme:,.0f}"
        credit_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours de Crédits PME</span> : {result_encours_credit_pme:,.0f}"
        cb_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours du Crédit-Bail PME</span> : {result_encours_cb_pme:,.0f}"
        csb_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours des Créances en Souffrance PME</span> : {result_encours_csb_pme:,.0f}"
        lt_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours des Crédits Long Terme PME</span> : {result_encours_lt_pme:,.0f}"
        mt_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'>Encours des Crédits Moyen Terme PME</span> : {result_encours_mt_pme:,.0f}"
        #taux_degra_pme_display.object = f"<span style='font-size: 14px; font-weight: 600; color:black'> Taux de dégradation PME </span> : {result_taux_degra_pme:.2f}%"

        
        return   
       
    except AssertionError as e:
        print(f"Erreur dans show_encours: {e}")
        return pn.Column(pn.pane.HTML("<div style='color:red'>Une erreur est survenue lors du calcul des encours 3.</div>"))


#FONCTION POUR Mettre à jour le graphique de la page 1
def update_graph_2(date, forme):
    graph_spinner.value = True  # Afficher le message de chargement
    df_filtered = df_g[(df_g['Arrete'] == pd.to_datetime(date)) & (df_g['Libelle Poste'] == forme)]
    
    # Grouper par 'Libelle Pays' et sommer 'Valeurn'
    grouped_df = df_filtered.groupby('Libelle Pays')['Valeurn'].sum().reset_index()
    
    # Créer le graphique basé sur les données groupées
    result = grouped_df.hvplot.bar(x='Libelle Pays', y='Valeurn', title=f'Encours {forme} au {date}')
    
    graph_spinner.value = False  # Cacher le message de chargement
    return result


#FONCTION DE traitement du dataframe de la page 02
def var_kpi_g(df, country, periodicity, start_date, end_date, indicators):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    if country == 'UEMOA':
        # Filter for the UEMOA region
        df_fil = df[(df['Arrete'] >= start_date) & (df['Arrete'] <= end_date)].copy()
        
        # Aggregate based on the periodicity
        if periodicity == 'Trimestrielle':
            df_fil['Trim'] = df_fil['Arrete'].dt.to_period('Q')
            df_fil = df_fil.sort_values(by='Arrete').drop_duplicates(subset=['Trim', 'Libelle Pays'], keep='last')
            df_agg = df_fil.groupby(['Trim'])[indicators].sum().reset_index()
        elif periodicity == 'Mensuelle':
            df_fil['Month'] = df_fil['Arrete'].dt.to_period('M')
            df_agg = df_fil.groupby(['Month'])[indicators].sum().reset_index()
        elif periodicity == 'Annuelle':
            df_fil['Year'] = df_fil['Arrete'].dt.year
            df_fil = df_fil.sort_values(by='Arrete').drop_duplicates(subset=['Year', 'Libelle Pays'], keep='last')
            df_agg = df_fil.groupby(['Year'])[indicators].sum().reset_index()
        df_agg['Libelle Pays'] = "UEMOA"
        col = df_agg.pop("Libelle Pays")
        df_agg.insert(1, "Libelle Pays",col)

    else:
        # Filter for the selected country
        df_fil = df[(df['Libelle Pays'] == country) & (df['Arrete'] >= start_date) & (df['Arrete'] <= end_date)].copy()
        
        # Aggregate based on the periodicity
        if periodicity == 'Trimestrielle':
            df_fil['Trim'] = df_fil['Arrete'].dt.to_period('Q')
            df_agg = df_fil.groupby(['Trim', 'Libelle Pays'])[indicators].last().reset_index()
        elif periodicity == 'Mensuelle':
            df_fil['Month'] = df_fil['Arrete'].dt.to_period('M')
            df_agg = df_fil.groupby(['Month', 'Libelle Pays'])[indicators].last().reset_index()
        elif periodicity == 'Annuelle':
            df_fil['Year'] = df_fil['Arrete'].dt.year
            df_agg = df_fil.groupby(['Year', 'Libelle Pays'])[indicators].last().reset_index()

        # Calculate percentage variation for each indicator
    for indicator in indicators:
        df_agg[f'Variation {indicator}'] = df_agg[indicator].pct_change().fillna(0) * 100
        df_agg[f'Variation {indicator}'] = df_agg[f'Variation {indicator}'].apply(lambda x: f"{x:.2f}%")
    
    return df_agg
def var_kpi_pme(df, country, periodicity, start_date,end_date, indicators_pme, type_pme):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    if country == 'UEMOA':
        if type_pme == 'Financement Global' :
            df_fil = df[(df['Arrete'] >= start_date) & (df['Arrete'] <= end_date)].copy()
            
            if periodicity == 'Trimestrielle':
                df_fil['Trim'] = df_fil['Arrete'].dt.to_period('Q')
                df_fil = df_fil.sort_values(by='Arrete').drop_duplicates(subset=['Trim', 'Libelle Pays','Libelle Colonne'], keep='last')
                df_agg = df_fil.groupby(['Trim'])[indicators_pme].sum().reset_index()
                
            elif periodicity == 'Mensuelle':
                df_fil['Month'] = df_fil['Arrete'].dt.to_period('M')
                df_agg = df_fil.sort_values(by='Arrete').drop_duplicates(subset=['Month', 'Libelle Pays','Libelle Colonne'], keep='last')
                df_agg = df_agg.groupby(['Month'])[indicators_pme].sum().reset_index()
            elif periodicity == 'Annuelle':
                df_fil['Year'] = df_fil['Arrete'].dt.year
                df_agg = df_fil.sort_values(by='Arrete').drop_duplicates(subset=['Year', 'Libelle Pays','Libelle Colonne'], keep='last')
                df_agg = df_agg.groupby(['Year'])[indicators_pme].sum().reset_index()
        else : 
            df_fil = df[(df['Arrete'] >= start_date) & (df['Arrete'] <= end_date) & (df['Libelle Colonne'] == type_pme)].copy()
            
            if periodicity == 'Trimestrielle':
                df_fil['Trim'] = df_fil['Arrete'].dt.to_period('Q')
                df_agg = df_fil.sort_values(by ='Arrete').drop_duplicates(subset=['Trim','Libelle Pays','Libelle Colonne'],keep='last')
                df_agg = df_agg.groupby(['Trim'])[indicators_pme].sum().reset_index()
                

            elif periodicity == 'Mensuelle':
                df_fil['Month'] = df_fil['Arrete'].dt.to_period('M')
                df_agg = df_fil.sort_values(by ='Arrete').drop_duplicates(subset=['Month','Libelle Colonne','Libelle Pays'],keep='last')
                df_agg = df_agg.groupby(['Month'])[indicators_pme].sum().reset_index()
                
            elif periodicity == 'Annuelle':
                df_fil['Year'] = df_fil['Arrete'].dt.year
                df_agg = df_fil.sort_values(by ='Arrete').drop_duplicates(subset=['Year','Libelle Pays','Libelle Colonne'],keep='last')
                
                df_agg = df_agg.groupby(['Year'])[indicators_pme].sum().reset_index()

        df_agg['Libelle Pays'] = "UEMOA"
        col = df_agg.pop("Libelle Pays")
        df_agg.insert(1, "Libelle Pays",col)
            
        
    else  :
        if type_pme == 'Financement Global' :
            df_fil = df[(df['Libelle Pays'] == country) & (df['Arrete'] >= start_date) & (df['Arrete'] <= end_date)].copy()
            
            if periodicity == 'Trimestrielle':
                df_fil['Trim'] = df_fil['Arrete'].dt.to_period('Q')
                df_agg = df_fil.sort_values(by = 'Arrete').drop_duplicates(subset =['Trim','Libelle Colonne'], keep='last')
                df_agg = df_agg.groupby(['Trim', 'Libelle Pays'])[indicators_pme].sum().reset_index()
         
            elif periodicity == 'Mensuelle':
                df_fil['Month'] = df_fil['Arrete'].dt.to_period('M')
                df_agg = df_fil.groupby(['Month', 'Libelle Pays'])[indicators_pme].sum().reset_index()
            elif periodicity == 'Annuelle':
                df_fil['Year'] = df_fil['Arrete'].dt.year
                df_fil = df_fil.sort_values(by = 'Arrete').drop_duplicates(subset =['Year','Libelle Colonne'], keep='last')
                df_agg = df_fil.groupby(['Year', 'Libelle Pays'])[indicators_pme].sum().reset_index()
        else : 
            df_fil = df[(df['Libelle Pays'] == country) & (df['Arrete'] >= start_date) & (df['Arrete'] <= end_date) & (df['Libelle Colonne'] == type_pme)].copy()
            
            if periodicity == 'Trimestrielle':
                df_fil['Trim'] = df_fil['Arrete'].dt.to_period('Q')
                df_agg = df_fil.groupby(['Trim', 'Libelle Pays']).last().reset_index()
                df_agg = df_agg[['Trim'] + indicators_pme]  # Sélectionner les colonnes souhaitées
            elif periodicity == 'Mensuelle':
                df_fil['Month'] = df_fil['Arrete'].dt.to_period('M')
                df_agg = df_fil.groupby(['Month', 'Libelle Pays']).last().reset_index()
                df_agg = df_agg[['Month'] + indicators_pme]  # Sélectionner les colonnes souhaitées
            elif periodicity == 'Annuelle':
                df_fil['Year'] = df_fil['Arrete'].dt.year
                df_agg = df_fil.groupby(['Year', 'Libelle Pays']).last().reset_index()
                df_agg = df_agg[['Year'] + indicators_pme]  # Sélectionner les colonnes souhaitées
    
        # Calculer la variation en pourcentage pour chaque indicateur
    for indicator in indicators_pme:
        df_agg[f'Variation {indicator}'] = df_agg[indicator].pct_change().fillna(0) * 100
        df_agg[f'Variation {indicator}'] = df_agg[f'Variation {indicator}'].apply(lambda x: f"{x:.2f}%")
    
        
    return df_agg


# AFFichage des messages d'infos
info_message =  """
<div class="border-box">
    <h1> Dashboard de Suivi du Financement des Économies de l'UEMOA ! Version 1.0 (Première) </h1>
    <h2> Bienvenue, veuillez lire ce guide en vue d'une prise en main rapide du DASHBOARD SFE 1.0 </h2>
    <p> 
        Ce tableau de bord est conçu pour vous aider à suivre les indicateurs clés du financement de la zone UEMOA de manière efficace. Voici comment l'utiliser : 
    </p>
    <p> 
        La Page 1 donne un apperçu rapide des indicateurs Clés et la Page 2 en donne une analyse en tendance selon la périodicité souhaitée 
    </p>
    <p> 
        Dans le menu de gauche se retrouve des Filtres et 3 Pages disponibles dont 2 Pages opérationnelles (Page 1 et Page 2)
    </p> 
    <p> 
                                                            PAGE 1 
    </p>
    <ul>
        <li>Sélectionnez tout à gauche la zone sur laquelle vous voulez faire votre analyse dans le menu déroulant "Selectionner un pays".</li> 
        <li>Choisissez la date à laquelle vous souhaitez voir vos indicateurs dans le menu déroulant " Selectionner une date".</li> 
        <li>Dans le cas des PME, vous pouvez observer la nature du financement octroyer à travers le menu déroulant "Sélectionner le type de Financement".</li> 
        <li>Vous pouvez ainsi observer vos indicateurs à l'encadré droit du dashboard.</li>
        <li> WARMING : SI VOUS N'OBSERVEZ AUCUNE ACTUALISATION UNE FOIS LES FILTRES CHOISIS VEUILLEZ ACTUALISER LA PAGE EN CLIQUANT SUR PAGE 1 .</li>
    </ul>
    <p> 
                                                            PAGE 2 
    </p>
    <p> la logique des filtres reste conservée (les filtres du menu déroulant de gauche sont valables sur toutes les pages
        <p> La page 2 affiche les memes indicateurs que la page 1 sauf qu'ils sont en série.
        <p> Vous pouvez choisir la périoidicté (Periodicity) des données et la période sur laquelle faire l'analyse (Date de début, Date de fin)
        <p> Une fois que vous avez défini vos critères, cliquez sur le bouton "Exporter" pour télécharger les données filtrées au format Excel
    <p> Amusez-vous à explorer les différentes options et à tirer le meilleur parti de vos données !
    </p> 
</div> 
"""
# Fonction d'exportation des données filtrées de la page 2
filtered_df =pd.DataFrame()
def export_excel():
 
    output = BytesIO() 
    filtered_df.to_excel(output, index=False)
    output.seek(0) 
    return output
export_button = pn.widgets.FileDownload(filename='filtered_data.xlsx', callback=export_excel, button_type='success')


# Mise à jour 
def update_view(event=None):
    if data_loaded: 
        try:
            show_encours(select_country.value, date_select.value,select_type.value)
            dashboard_content.object = show_encours(select_country.value, date_select.value,select_type.value)
        except Exception as e:
            print(f"Erreur dans update_view: {e}")
            dashboard_content.object = pn.pane.Markdown(f"Une erreur est survenue dans la mise à jour du dashboard: {e}")

#select_country.param.watch(update_view, 'value')
#date_select.param.watch(update_view, 'value')
#select_type.param.watch(update_view, 'value')

def view (date, forme):
    graph_spinner.value = True
    result = update_graph_2(date, forme)
    graph_spinner.value = False  # Désactiver le spinner après les calculs
    return pn.Column(result)
view = pn.bind(view, date_select.param.value, forme_g_select.param.value)

##########-------------------------------FONCTIONS MISE A JOUR DE LA PAGE 1 ----------------------------------####################################
@pn.depends(select_country.param.value, credit_var.param.value, periodicity.param.value, start_date_picker.param.value,end_date_picker.param.value,var_pme.param.value,select_type.param.value)
def maj_var(country, indicators, periodicity,start_date,end_date,indicators_pme,type_pme ):
    global filtered_df
    frame_layout = pn.pane.Markdown("Aucun indicateur sélectionné.")  # Initialisation par défaut
    frame_layout_pme = pn.pane.Markdown("Aucun indicateur PME sélectionné.")  # Initialisation par défaut
    
    if indicators:
        frame = var_kpi_g(merged_g, country, periodicity,start_date_picker.value,end_date_picker.value,indicators)
        filtered_df = frame
        frame_layout = pn.pane.DataFrame(frame, width=1200, height=800)
        return frame_layout
    
    elif indicators_pme : 
        frame_pme = var_kpi_pme(merged_pme, country, periodicity,start_date_picker.value,end_date_picker.value,indicators_pme,type_pme)
        filtered_df= frame_pme
        frame_layout_pme = pn.pane.DataFrame(frame_pme, width=1300, height=800)
        return frame_layout_pme


# Etape 3 : Le chargement et le traitement des données importées
df_g = None  # Fichier global
df_pme = None  # Fichiers PME combinés
progress = pn.indicators.Progress(name="Progression", bar_color="success", value=0, max=100)

























### Pré traitement des fichiers 

global_loaded = False
pme_loaded = False
data_loaded = False


dashboard_content = pn.Column(sizing_mode="stretch_both")
#file_input = pn.widgets.FileInput(accept='.xlsx', width=300)

file_input_global = pn.widgets.FileInput(name="Importer le fichier global (Excel)", accept ='.xlsx')
file_input_pme = pn.widgets.FileInput(name="Importer les fichiers PME (Excel, multi-sélection possible)", multiple=True, accept ='.xlsx')
#progress = pn.indicators.Progress(name="Progression", bar_color="primary", value=0, max=100)

process_button = pn.widgets.Button(name='Lancer le traitement des données', button_type='primary')
progress = pn.indicators.Progress(name="Progression", bar_color="primary", value=0, max=100)

page_buttons = pn.Column(
    pn.widgets.Button(name='Importation des données', button_type='default', width=300, icon = 'download'),
    pn.widgets.Button(name='Indicateurs de Financement', button_type='default', width=300, icon ='zoom-in'),
    pn.widgets.Button(name='Extraction de base de donnée', button_type='default', width=300, icon ='upload'),
    pn.widgets.Button(name='En cours de développement...', button_type='default', width=300, icon='settings-cog')
)
# CSS pour l'encadré
encadre_style = """
.encadre-gauche {
    border: 2px solid black; 
    padding: 20px;
    border-radius: 5px;
    background-color: #9E6C12;  
    height: 200%;  
    width: 370px;  
    box-sizing: border-box;  
}
"""
pn.config.raw_css.append(encadre_style)


def update_widgets():
    global dates_list, pme_type
    # Vérifier si les données nécessaires sont disponibles
    if dates_list and pme_type:
        date_select.options = dates_list
        select_type.options = pme_type




# Traitement des fichiers
def process_data():
    global df_g, df_pme, merged_g, merged_pme,data_loaded, pme_loaded, global_loaded
    global df_g_credit, df_g_aft, df_g_cb, df_g_csb, df_g_lt, df_g_mt, df_g_ct
    global df_pme_aft, df_pme_credit, df_pme_cb, df_pme_csb, df_pme_lt, df_pme_mt
    global df_g_aft, df_g_credit, df_g_cb, df_g_csb, df_g_depreciation, df_g_emplois, df_g_titres, dates_list, pme_type

    # Initialisation de la progression
    progress.value = 0
    try: 
        # Traitement fichier global
        if file_input_global.value:
            try:
                progress.value = 10
                progress.name = "Chargement du fichier global..."
                
                # Chargement du fichier global
                df_g = pd.read_excel(file_input_global.value)
                


                # Opérations sur le fichier global
                df_g['Arrete'] = pd.to_datetime(df_g['Arrete'], errors='coerce', dayfirst=True)

                dates_list =df_g['Arrete'].dt.strftime('%Y-%m-%d').unique().tolist()

                df_g['Libelle Pays'] = df_g['Libelle Pays'].replace({
                    "Bénin": "Benin",
                    "Burkina Faso": "Burkina",
                    "Côte d Ivoire": "Côte d'Ivoire"
                })
                df_g.sort_values(by="Arrete", ascending=False, inplace=True)
                progress.value = 25
                # Découpage en mini-DataFrames
                df_g_credit = df_g[df_g["Libelle Poste"] == "Crédits nets"]
                df_g_aft = df_g[df_g["Libelle Poste"] == "Affacturage"]
                df_g_cb = df_g[df_g["Libelle Poste"] == "Crédit de location-financement"]
                df_g_csb = df_g[df_g["Libelle Poste"] == "Créances en souffrance"]
                df_g_depreciation = df_g[df_g["Libelle Poste"] == "Depreciations"]
                df_g_titres = df_g[df_g['Libelle Poste'].isin([
                                'Titres d investissement', 'Titres de transaction',
                                'Titres de placement et titres de l activité de portefeuille'
                            ])]
                df_g_emplois = df_g[df_g['Libelle Poste'] == 'Total emplois-I+II']
                df_g_lt = df_g[df_g['Libelle Poste'] == 'Crédits à long terme']
                df_g_mt = df_g[df_g['Libelle Poste'] == 'Crédits à moyen terme']
                df_g_ct = df_g[df_g['Libelle Poste'] == 'Crédits à court terme']
                progress.value = 35
                # Agrégations
                egc = df_g_credit.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                egc.rename(columns={'Valeurn': 'Encours Global Crédit'}, inplace=True)

                ega = df_g_aft.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                ega.rename(columns={'Valeurn': 'Encours Global Aft'}, inplace=True)

                egcb = df_g_cb.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                egcb.rename(columns={'Valeurn': 'Encours Global Crédit-Bail'}, inplace=True)

                egcsb = df_g_csb.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                egcsb.rename(columns={'Valeurn': 'Encours Global Créance en souffrance'}, inplace=True)

                eglt = df_g_lt.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                eglt.rename(columns={'Valeurn': 'Encours Global Crédit Long Terme'}, inplace=True)

                egmt = df_g_mt.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                egmt.rename(columns={'Valeurn': 'Encours Global Crédit Moyen Terme'}, inplace=True)

                egct = df_g_ct.groupby(['Arrete', 'Libelle Pays'])['Valeurn'].sum().reset_index()
                egct.rename(columns={'Valeurn': 'Encours Global Crédit Court Terme'}, inplace=True)
                progress.value = 45
                # Fusions successives
                merged1 = pd.merge(egc, ega, on=['Arrete', 'Libelle Pays'], how='inner')
                merged2 = pd.merge(merged1, egcb, on=['Arrete', 'Libelle Pays'], how='inner')
                merged3 = pd.merge(merged2, egcsb, on=['Arrete', 'Libelle Pays'], how='inner')
                merged4 = pd.merge(merged3, eglt, on=['Arrete', 'Libelle Pays'], how='inner')
                merged5 = pd.merge(merged4, egmt, on=['Arrete', 'Libelle Pays'], how='inner')
                merged_g = pd.merge(merged5, egct, on=['Arrete', 'Libelle Pays'], how='inner')

                progress.value = 50
                #pn.pane.Markdown("Traitement des données terminé pour le fichier global!", styles={'color': 'green'}).servable()
                
                global_loaded = True
                #dashboard_content[:] = [pn.pane.Markdown("Traitement des données Globales terminé avec succès!", styles={'color': 'green'}).servable()]
            except Exception as e:
                dashboard_content[:] =[pn.pane.Markdown(f"Erreur lors du traitement du fichier global : {e}", styles={'color': 'red'}).servable()]
                
        else :
            dashboard_content[:] = [pn.pane.Markdown("**Erreur : Aucun fichier global n'a été importé.**", styles={'color': 'red'})]
            return
        # Traitement fichiers PME
        if file_input_pme.value:
            try:
                progress.value = 55
                progress.name = "Chargement des fichiers PME..."
                # Chargement des fichiers PME
                pme_dataframes = [
                    
                    pd.read_excel(file) for file in file_input_pme.value
                ]
                df_pme = pd.concat(pme_dataframes, ignore_index=True)


                # Opérations sur les fichiers PME
                df_pme['Arrete'] = pd.to_datetime(df_pme['Arrete'], errors='coerce', dayfirst=True)
                

                df_pme['Libelle Pays'] = df_pme['Libelle Pays'].replace({
                    "Bénin": "Benin",
                    "Burkina Faso": "Burkina",
                    "Côte d Ivoire": "Côte d'Ivoire"
                })
                df_pme['Libelle Colonne'] = df_pme['Libelle Colonne'].replace({
                    "Autres societes financieres\tSocietes d assurance et Fonds de pension ": "Autres Sociétés Financières",
                    "Autres societes financieres\tSocietes d'assurance et Fonds de pension ": "Autres Sociétés Financières",
                    "Autres societes financieres\tAutres intermediaires financiers": "Autres Sociétés Financières",
                    "Autres societes financieres\tAuxiliaires financiers ": "Autres Sociétés Financières",

                    "Societes non financieres Publiques \t": "Sociétés Non Financières",
                    "Societes non financieres Autres \t": "Sociétés Non Financières",
                    "Menages Entreprises individuelles\t": "Ménages & Entreprises Individuelles",
                    "Menages Particuliers\t": "Ménages & Entreprises Individuelles"
                })
                pme_type = df_pme['Libelle Colonne'].unique().tolist()
                pme_type.append('Financement Global')
                df_pme.sort_values(by="Arrete", ascending=False, inplace=True)
                
                progress.value = 65
                # Découpage en mini-DataFrames (PME)
                df_pme_aft = df_pme[df_pme['POSTE'] == 'Affacturage / PME-PMI']
                df_pme_credit = df_pme[df_pme['POSTE'] == 'Credits a la clientele / Credits aux PME-PMI']
                df_pme_cb = df_pme[df_pme['POSTE'] == 'Credit de location-financement / PME-PMI']
                df_pme_csb = df_pme[df_pme['POSTE'] == 'Creances en souffrance / PME-PMI']
                df_pme_lt = df_pme[df_pme['POSTE'] == 'Credits a long terme / PME-PMI']
                df_pme_mt = df_pme[df_pme['POSTE'] == 'Credits a moyen terme / PME-PMI']
                progress.value = 70
                # Agrégations et fusions (PME)
                ecpme = df_pme_credit.groupby(['Arrete', 'Libelle Pays', 'Libelle Colonne'])['Valeurn'].sum().reset_index()
                ecpme.rename(columns={'Valeurn': 'Encours Crédit PME'}, inplace=True)

                eapme = df_pme_aft.groupby(['Arrete', 'Libelle Pays', 'Libelle Colonne'])['Valeurn'].sum().reset_index()
                eapme.rename(columns={'Valeurn': 'Encours Aft PME'}, inplace=True)

                ecbpme = df_pme_cb.groupby(['Arrete', 'Libelle Pays', 'Libelle Colonne'])['Valeurn'].sum().reset_index()
                ecbpme.rename(columns={'Valeurn': 'Encours Crédit-Bail PME'}, inplace=True)

                ecsbpme = df_pme_csb.groupby(['Arrete', 'Libelle Pays', 'Libelle Colonne'])['Valeurn'].sum().reset_index()
                ecsbpme.rename(columns={'Valeurn': 'Encours Créance en Souffrance PME'}, inplace=True)
                progress.value = 75
                eltpme = df_pme_lt.groupby(['Arrete', 'Libelle Pays', 'Libelle Colonne'])['Valeurn'].sum().reset_index()
                eltpme.rename(columns={'Valeurn': 'Encours Crédit Long Terme PME'}, inplace=True)
                progress.value = 75
                emtpme = df_pme_mt.groupby(['Arrete', 'Libelle Pays', 'Libelle Colonne'])['Valeurn'].sum().reset_index()
                emtpme.rename(columns={'Valeurn': 'Encours Crédit Moyen Terme PME'}, inplace=True)
                progress.value = 90
                merged1 = pd.merge(ecpme, eapme, on=['Arrete', 'Libelle Pays', 'Libelle Colonne'], how='inner')
                merged2 = pd.merge(merged1, ecbpme, on=['Arrete', 'Libelle Pays', 'Libelle Colonne'], how='inner')
                merged3 = pd.merge(merged2, ecsbpme, on=['Arrete', 'Libelle Pays', 'Libelle Colonne'], how='inner')
                merged4 = pd.merge(merged3, eltpme, on=['Arrete', 'Libelle Pays', 'Libelle Colonne'], how='inner')
                merged_pme = pd.merge(merged4, emtpme, on=['Arrete', 'Libelle Pays', 'Libelle Colonne'], how='inner')

                progress.value = 100
                dashboard_content[:] = [pn.pane.Markdown("Traitement des données PME terminé avec succès!", styles={'color': 'green'}).servable()]
                pme_loaded = True
            except Exception as e:
                dashboard_content[:] = [pn.pane.Markdown(f"Erreur lors du traitement des fichiers PME : {e}", styles={'color': 'red'}).servable()]
                
            
        else :
            dashboard_content[:] = [pn.pane.Markdown(f"Erreur : Veuillez Charger les fichiers PME : {e}", styles={'color': 'red'}).servable()]
            return
        # Finalisation
        
        if global_loaded and pme_loaded:
            dashboard_content[:] = [pn.pane.Markdown("**Tous les fichiers ont été importés et traités avec succès !**", styles={'color': 'green'})]
            data_loaded = True
        else:
            dashboard_content[:] = [pn.pane.Markdown("**Erreur : Échec du traitement des fichiers.**", styles={'color': 'red'})]
        update_widgets()

    except Exception as e:
        #data_loaded = False
        dashboard_content[:] = [pn.pane.Markdown(f"**Erreur Méga Chelou : {e}**", styles={'color': 'red'})]



def start_processing(event):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    executor.submit(process_data)
process_button.on_click(start_processing)





# Gestion des pages
def change_page(event):
    global data_loaded
    grid = pn.GridSpec(sizing_mode="stretch_both")
    
    # Page 0 : Importation des fichiers
    if event.obj.name == 'Importation des données':
        dashboard_content[:] = [pn.Column(
            pn.pane.Markdown("**Importation des données - Veuillez charger vos données :**"),
            file_input_global,
            file_input_pme,
            process_button,
            progress,
            pn.Spacer(height=20),  # Espace supplémentaire pour aérer l'interface
        )]
        
    elif not data_loaded : 
        dashboard_content[:] = [pn.pane.Markdown("**Veuillez importer et traiter les données sur la Page 0 avant d'accéder aux autres pages.**", styles={'color': 'red'})]
    
    elif event.obj.name == 'Indicateurs de Financement':
        dashboard_content[:] = [loading_spinner]
        dashboard_content.loading = True
        select_country.param.watch(update_view, 'value')
        date_select.param.watch(update_view, 'value')
        select_type.param.watch(update_view, 'value')

        # Appel des fonctions pour préparer les données de la Page 1
        show_encours(select_country.value, date_select.value, select_type.value)

        # Construction de la grille pour la Page 1
        grid[0, 0] = pn.Column(
            mt_pme_display, prop_aff_pme_display, prop_cb_pme_display, taux_credit_pme_display
        )
        grid[0, 1] = pn.Column(cb_display, csb_display, credit_display, aft_display)
        grid[0, 2] = pn.Column(lt_display, mt_display, lt_pme_display, total_titres_display)
        grid[1, 0] = pn.Column(ct_display, credit_pme_display, titres_display, taux_degradation_display)
        grid[1, 1] = pn.Column(aft_pme_display, prop_aff_display, taux_degra_pme_display)
        grid[1, 2] = pn.Column(cb_pme_display, csb_pme_display)
        grid[3:5, :] = pn.Column(
            pn.Row(forme_g_select, graph_spinner),
            view,
            css_classes=['border-box']
        )
        dashboard_content[:] = [grid]
        dashboard_content.loading = False

    elif event.obj.name == 'Extraction de base de donnée':
        dashboard_content[:] = [loading_spinner]
        dashboard_content.loading = True
        grid = pn.GridSpec(sizing_mode="stretch_both",height=400)
        # Construction de la grille pour la Page 2
        grid[0, :3] = pn.Row(start_date_picker, end_date_picker, periodicity)
        grid[1, :2] = pn.Row(select_type,pn.Spacer(width =25), var_pme)
        grid[2, :2] = pn.Row(credit_var, export_button)
        grid[3, :3] = maj_var

        dashboard_content[:] = [grid]
        dashboard_content.loading = False

    # Page 3 : Une page HTML simple
    elif event.obj.name == 'En cours de développement...':
        dashboard_content[:] = [pn.pane.HTML("<div style='height:100%;'>Ceci est la page 3 du dashboard, en cours de développement</div>")]

    else:
        dashboard_content[:] = [
            pn.pane.Markdown("**Page inconnue. Veuillez vérifier votre sélection.**", styles={'color': 'red'})
        ]
    

    

for btn in page_buttons:
    btn.on_click(change_page)

# Mettre à jour le CSS pour intégrer le fond coloré
dashboard_styles = {
    'background-color': '#9E6C12', 
    'border': '2px solid black',
    'border-radius': '5px', 
    'padding': '10px', 
    'height': '120%',
    'width': 'calc(100% )'  # Ajuster la largeur de l'encadré pour prendre plus de place
}


# Appliquer le CSS globalement
pn.config.raw_css.append(dashboard_styles)



# Encadré gauche
encadre_gauche = pn.Column(
    pn.pane.Markdown('<div style="font-size:20px; text-align:center; font-weight:bold;">Menue</div>'),
    pn.Spacer(height=15),
    pn.pane.Markdown('<div style="font-size:20px; text-align:center; font-weight:bold;">Choix des filtres</div>'),
    pn.Spacer(height=15),
    select_country,
    select_type,
    date_select,
    pn.Spacer(height=25),
    pn.pane.Markdown('<div style="font-size:20px; text-align:center; font-weight:bold;">Pages de navigation</div>'),
    page_buttons,
    css_classes=["encadre-gauche"]
)
filters = pn.Column(select_country, select_type, date_select, css_classes=['border-box'])

# Layout principal
layout = pn.Row(
    encadre_gauche,
    dashboard_content
)

layout.show()







