import pandas as pd
import numpy as np
from datetime import datetime 


# df_2018 = pd.read_excel('C:/Users/ckoupoh/Documents/PME_SFE/files/situation financiere_data_2018.xlsx')
# df_2019 = pd.read_excel('C:/Users/ckoupoh/Documents/PME_SFE/files/situation financiere_data_2019.xlsx')
# df_2021 = pd.read_excel('C:/Users/ckoupoh/Documents/PME_SFE/files/situation financiere_data_2021.xlsx')
# df_2022 = pd.read_excel('C:/Users/ckoupoh/Documents/PME_SFE/files/situation financiere_data_2022.xlsx')
# df_2023 = pd.read_excel('C:/Users/ckoupoh/Documents/PME_SFE/files/situation financiere_data_2023.xlsx')
# df_2024 = pd.read_excel('C:/Users/ckoupoh/Documents/PME_SFE/files/situation financiere_data_2024.xlsx')



def get_mois(m_mois):
    if   m_mois == 'Janvier': rk = '01'
    elif m_mois == 'Février': rk = '02'
    elif m_mois == 'Mars': rk = '03'
    elif m_mois == 'Avril': rk = '04'
    elif m_mois == 'Mai': rk = '05'
    elif m_mois == 'Juin': rk = '06'
    elif m_mois == 'Juillet': rk = '07'
    elif m_mois == 'Août': rk = '08'
    elif m_mois == 'Septembre': rk = '09'
    elif m_mois == 'Octobre': rk = '10'
    elif m_mois == 'Novembre': rk = '11'
    elif m_mois == 'Décembre': rk = '12'

    return rk

#Presenter credit_net par period / Date répétitive
def get_credit(df, m_pays , m_poste, d_year, d_period):

    #date_deb = datetime.strptime(d_debut, "%Y-%m-%d")
    #date_fin = datetime.strptime(d_fin, "%Y-%m-%d")

    if d_period == 'Mensuel':
        d_period = 'M'
    elif d_period == 'Trimestriel':
        d_period = 'Q'
    elif d_period == 'Semestriel':
        d_period = '2Q'
    else:
        d_period = 'A'

    V = df.loc[(df['Libelle Poste']  == m_poste) & (df['Libelle Pays']  == m_pays)]
    V= V.loc[str(d_year)]
    valeur = round(V['Valeurn'].resample(d_period).sum()/1000, 2)  

    return valeur.index, valeur.values

def conclusionStat(annee, m_zone, m_emprunt, HPR_emprunt, treso, HPR_treso, affactu, HPR_affactu, campagne, HPR_campagne):

    R_HPR_emprunt = ""
    R_tx_treso = ""
    R_tx_campagn = ""

    if m_zone == 'UEMOA': m_zone = ', dans la zone UEMOA'
    elif m_zone == 'Bénin': m_zone = 'au Bénin'
    elif m_zone == 'Burkina': m_zone = 'au Burkina Faso'
    elif m_zone == "Côte d'Ivoire": m_zone = "en Côte d'Ivoire"
    elif m_zone == 'Guinée Bissaù': m_zone = 'en Guinée Bissaù'
    elif m_zone == 'Mali': m_zone = 'au Mali'
    elif m_zone == 'Niger': m_zone = 'au Niger'
    elif m_zone == 'Sénégal': m_zone = 'au Sénégal'
    elif m_zone == 'Togo': m_zone = 'au Togo'

    if HPR_emprunt>0:
        R_HPR_emprunt = 'hausse de **' +str(HPR_emprunt)+ "**%  comparativement à "+str(annee -1)
    elif HPR_emprunt == 0:
        R_HPR_emprunt = 'valeur similaire à '+str(annee -1)
    elif HPR_emprunt <0:
        R_HPR_emprunt = 'baisse de **' +str(HPR_emprunt)+ "**%  par rapport à "+str(annee -1)

    if HPR_treso>0:
        R_tx_treso = 'hausse de **' +str(HPR_treso)+ "**% en glissement annuel"
    elif HPR_treso == 0:
        R_tx_treso = 'valeur identique à ' +str(annee -1)
    elif HPR_treso <0:
        R_tx_treso = 'baisse de **' +str(HPR_treso)+ "**% par rapport à l'année antérieur"

    if HPR_affactu>0:
        R_tx_affactu = 'augmentation de **' +str(HPR_affactu)+ "**% comparativement à l'exercice précédent"
    elif HPR_affactu == 0:
        R_tx_affactu = 'valeur similaire à la période antérieure' 
    elif HPR_affactu <0:
        R_tx_affactu = 'diminution de **' +str(HPR_affactu)+ "**% par rapport à l'exercice précédent"

    if HPR_campagne>0:
        R_tx_campagn = 'augmentation de**' +str(HPR_campagne)+ "**% comparativement à l'année dernière"
    elif HPR_campagne == 0:
        R_tx_campagn = "semblable au montant de l'année antérieur"
    elif HPR_campagne <0:
        R_tx_campagn = 'diminution de **' +str(HPR_campagne)+ "**% par rapport à l'année antérieure"

    ## Au cours du mois de Janvier 2025, le montant total d'emprunts obligataires s'est établi à 10 mds, 
    res = "Au cours de l'année **" + str(annee) + "**, le montant total des dépôts et emprunts **"+m_zone +  "** s'est établi à **" +str(round(m_emprunt/1000,2)) +"** milliards de FCFA, soit une "+R_HPR_emprunt+ ". De plus, les operations de tresorerie ont été évaluées à **" +str(round(treso/1000,2))+ "** millions de FCFA. Soit une "+R_tx_treso+". "+"Par ailleurs, le montant total de l'affacturage sur la même période était de **"+str(round(affactu/1000,2))+"** soit une "+R_tx_affactu+". Les Crédits de campagne ont été évalués à **" +str(round(campagne/1000,2))+"** milliards de FCFA, soit une "+R_tx_campagn+"."

    return res


#########*********************SECOND LIGNE************************#######################

def get_indicateur(v_df,m_post, m_pays, m_annee):

    
    #df = v.loc[v['Libelle Poste']  == m_post]

    if m_pays == 'UEMOA':
        df = v_df.loc[(v_df['Libelle Poste']  == m_post) & (v_df['Libelle Pays']  != '')] 
    else:
        df = v_df.loc[(v_df['Libelle Poste']  == m_post) & (v_df['Libelle Pays']  == m_pays)]

    df = df.loc[str(m_annee)]
    v_actual = round((df['Valeurn'].sum()/1000),2)

    m_delta = 0

    if m_annee == '2018':
        m_delta = 0
    else:
        #m_past = int(m_annee)-1
        vf = v_df.loc[v_df['Libelle Poste']  == m_post]
        m_past = vf.loc[str(m_annee - 1)]
        #v_past = round(m_past['Valeurn'].sum()/1000, 2)

        m_delta = ((df['Valeurn'].sum()/m_past['Valeurn'].sum())-1)*100

    return v_actual, round(m_delta, 2)

def get_autres_postes(v, m_annee, post_1):
    l_LT = []

    for i in ['Bénin',"Burkina Faso","Côte d'Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"]:
        if i == 'UEMOA':
            V_LT = v.loc[(v['Libelle Poste']  == post_1) & (v['Libelle Pays']  != "")]
        else:
            V_LT = v.loc[(v['Libelle Poste']  == post_1) & (v['Libelle Pays']  == i)]

        V_LT_yr = V_LT.loc[str(m_annee)]
        V_LT = V_LT_yr.loc[str(m_annee)]['Valeurn']
        
        l_LT.append(round(V_LT.values.sum()/1000,2))

    return l_LT

def get_pourcentage_credit(v, m_pays, v_annee, l_instru):
    l_res = []
    for i in l_instru:
        if m_pays == 'UEMOA':
            V_LT = v.loc[(v['Libelle Poste']  == i)]
        else:
            V_LT = v.loc[(v['Libelle Poste']  == i) & (v['Libelle Pays']  == m_pays)]
            

        V_LT_yr = V_LT.loc[str(v_annee)]
        V_LT = V_LT_yr.loc[str(v_annee)]['Valeurn'].sum()

        l_res.append(V_LT)

    total = sum(l_res)
    vf = [round(x*100/ total, 2)  for x in l_res]

    return vf

def get_classement_Instrument(v, m_pays, v_annee):

    df = ""
    if m_pays == 'UEMOA':
        df = v.loc[v['Libelle Pays']  != ""]
    else:
        df = v.loc[v['Libelle Pays']  == m_pays]
    
    df = df.loc[str(v_annee)]
    df = round(df.groupby("Libelle Poste")['Valeurn'].sum()/1000,2)
    df = df.sort_values(ascending=False)

    vf = df[[ 'Crédits à long terme', 
        'Crédits à moyen terme',
        'Crédits à court terme',
        'Crédits de campagne',
        'Crédit de location-financement', 'Affacturage',
        'Titres de transaction',
        'Titres d investissement',
        'Titres de placement et Autres'
        ]].sort_values(ascending=False) #'Titres de placement et titres de l activité de portefeuille'
    
    return vf

def get_Instrument_by_year(v, m_pays, m_instru):
    m_data = []
    for i in range(2018, 2025):
        vf = v.loc[str(i)]
        V_LT = vf.loc[(vf['Libelle Poste']  == m_instru) & (vf['Libelle Pays']  == m_pays)]
        
        V_LT = V_LT['Valeurn'].sum()
        m_data.append(V_LT)
        
    
    return m_data

def conclusionStat_2lign(v_df, m_zone, m_annee, montant_CT, montant_MT): #, HPR_LT,  HPR_MT, montant_CT, HPR_CT , montant_LT, montant_MT, montant_CT

    v = v_df.sort_values(ascending=True, by='Arrete')
    v = v.set_index(['Arrete'])
    
    HPR_CT = 0
    HPR_MT = 0
    R_HPR_CT = ""
    R_tx_MT = ""
    montant_CT = 0
    montant_MT = 0


    if m_zone == 'UEMOA':
        df_CT = v.loc[(v['Libelle Poste']  == 'Crédits à court terme') & (v['Libelle Pays']  != '')] 
        df_MT = v.loc[(v['Libelle Poste']  == 'Crédits à moyen terme') & (v['Libelle Pays']  != '')] 
        df_LT = v.loc[(v['Libelle Poste']  == 'Crédits à long terme') & (v['Libelle Pays']  != '')] 
    else:
        df_CT = v.loc[(v['Libelle Poste']  == 'Crédits à court terme') & (v['Libelle Pays']  == m_zone)]
        df_MT = v.loc[(v['Libelle Poste']  == 'Crédits à moyen terme') & (v['Libelle Pays']  == m_zone)]
        df_LT = v.loc[(v['Libelle Poste']  == 'Crédits à long terme') & (v['Libelle Pays']   == m_zone)]
    
    if m_annee == '2018':
        m_delta = 0
    elif m_annee != '2018':

        CT_actual = df_CT.loc[str(m_annee)]
        CT_pass = df_CT.loc[str(m_annee - 1)]

        CT_actual = df_CT.loc[str(m_annee)]
        CT_pass = df_CT.loc[str(m_annee - 1)]
        montant_CT = CT_actual['Valeurn'].sum()
       # print('Montant CT :', montant_CT)
        past_CT = CT_pass['Valeurn'].sum() 
        
        HPR_CT = (montant_CT/past_CT)-1
        HPR_CT = round(HPR_CT*100, 2)

        MT_actual = df_MT.loc[str(m_annee)]
        MT_pass = df_MT.loc[str(m_annee - 1)]

        montant_MT = MT_actual['Valeurn'].sum()
        pass_montant_MT = MT_pass['Valeurn'].sum()
        HPR_MT = (montant_MT/pass_montant_MT)-1
        HPR_MT = round(HPR_MT*100, 2)

    if m_zone == 'UEMOA': m_zone = ', dans la zone UEMOA'
    elif m_zone == 'Bénin': m_zone = 'au Bénin'
    elif m_zone == 'Burkina': m_zone = 'au Burkina Faso'
    elif m_zone == "Côte d'Ivoire": m_zone = "en Côte d'Ivoire"
    elif m_zone == 'Guinée Bissaù': m_zone = 'en Guinée Bissaù'
    elif m_zone == 'Mali': m_zone = 'au Mali'
    elif m_zone == 'Niger': m_zone = 'au Niger'
    elif m_zone == 'Sénégal': m_zone = 'au Sénégal'
    elif m_zone == 'Togo': m_zone = 'au Togo'

    res = ""

    if HPR_CT>0:
        R_HPR_CT = 'soit une hausse de **' +str(HPR_CT)+ "**%  comparativement à l'année antérieure"
    elif HPR_CT == 0:
        R_HPR_CT = "soit une valeur similaire à l'année antérieure" 
    elif HPR_CT <0:
        R_HPR_CT = 'soit une baisse de **' +str(HPR_CT)+ "**%  par rapport à l'année antérieure"

    if HPR_MT>0:
        R_tx_MT = ' soit une augmentation de **' +str(HPR_MT)+ "**%."
    elif HPR_MT == 0:
        R_tx_MT = "semblable au montant de l'année antérieur"
    elif HPR_MT <0:
        R_tx_MT = ' soit une diminution de **' +str(HPR_MT)+ "**%."

    res = "Les crédits à court terme et à moyen terme " +m_zone+ " ont été respectivement évalués à **" +str(round(montant_CT/1000, 2) )+ "** ( " + R_HPR_CT + ") et **" +str(round(montant_MT/1000, 2))+"** milliards de FCFA (" +R_tx_MT+ ")."
    return res

###################################BANKS######################################################

def get_transform_colonne(m_list):
    new_list = []
    for x in m_list:
        if x== 'Crédits à long terme':
            x = 'Crédits LT'
            new_list.append(x)
        elif x == 'Crédits à moyen terme':
            x = 'Crédits MT'
            new_list.append(x)
        elif x == 'Crédits à court terme':
            x = 'Crédits CT'
            new_list.append(x)
        elif x == 'Crédits de campagne':
            x = 'C. campagne'
            new_list.append(x)
        elif x == 'Crédit de location-financement':
            x = 'C. location'
            new_list.append(x)
        elif x == 'Affacturage':
            x = 'Affacturage'
            new_list.append(x)
        elif x == 'Titres de transaction':
            x = 'T. Transac°'
            new_list.append(x)
        elif x == 'Titres d investissement':
            x = 'T. Invest.'
            new_list.append(x)
        elif x == 'Titres de placement et Autres':
            x = 'T. Placem.'
            new_list.append(x)

    return new_list

def get_trans_bank():
    return 0

def get_ress_empl(v, m_bank):

    post_1 = "Total emplois-I+II"                                                               
    post_2 = "Total ressources- III+IV+V" 

    ress_list = []
    emp_list = []

    for x in range(2018, 2025):
        vf = v.loc[str(x)]
        V_1 = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == post_1) ]
        V_1 = round(V_1['Valeurn'].sum()/1000, 2)
        emp_list.append(V_1)

        V_2 = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == post_2) ]
        V_2 = round(V_2['Valeurn'].sum()/1000, 2)
        ress_list.append(V_2)

    return ress_list, emp_list

def struct_emp_ressource(v, m_bank, m_annee):

    vf = v.loc[str(m_annee)]
    # V_tot_ress = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Total emplois-I+II") ]
    # total_ress = V_tot_ress['Valeurn'].sum()

    v_fpropres = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Capitaux propres et ressources assimilés") ]
    res_fpropres = v_fpropres['Valeurn'].sum()

    v_dep_empr = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Dépots et emprunts") ]
    res_depot_empr = v_dep_empr['Valeurn'].sum()

    total_ress = res_fpropres + res_depot_empr

    ##################### Emplois #######################################

    cred_CT = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Crédits à court terme") ]
    valeur_CT = cred_CT['Valeurn'].sum()

    cred_MT = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Crédits à moyen terme") ]
    valeur_MT = cred_MT['Valeurn'].sum()

    cred_LT = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Crédits à long terme") ]
    valeur_LT = cred_LT['Valeurn'].sum()

    total_cred = valeur_CT+ valeur_MT + valeur_LT

    titre_pf = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Titres de placement et Autres") ] #"Autres Emplois"
    v_titre = titre_pf['Valeurn'].sum()

    autre_emp = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Autres Emplois") ]
    Autres_emploi = autre_emp['Valeurn'].sum()

    total_emploi =  Autres_emploi + total_cred + v_titre

    ##################### RATIOS #######################################

    part_ress = round((total_ress / (total_ress+total_emploi))*100, 0)
    part_emploi = round((total_emploi / (total_ress+total_emploi))*100, 0)
    # print(part_ress, part_emploi)
    part_cred = round((total_cred / (total_ress+total_emploi))*100, 0)
    part_titre = round((v_titre / (total_ress+total_emploi))*100, 0)
    part_autre_emploi = round((Autres_emploi / (total_ress+total_emploi))*100, 0)

    part_FPropre = round((res_fpropres / (total_ress+total_emploi))*100, 0)
    part_dep_empr = round((res_depot_empr / (total_ress+total_emploi))*100, 0)
    #part_divers = round((divers_ress / (total_ress+total_emploi))*100, 2)

    return [100, 
            part_emploi,part_ress, 
            part_cred, part_titre, part_autre_emploi,
            part_FPropre, part_dep_empr]

def struct_emplois(v, m_bank, m_annee):

    vf = v.loc[str(m_annee)]
    cred_CT = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Crédits à court terme") ]
    valeur_CT = cred_CT['Valeurn'].sum()

    cred_MT = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Crédits à moyen terme") ]
    valeur_MT = cred_MT['Valeurn'].sum()

    cred_LT = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Crédits à long terme") ]
    valeur_LT = cred_LT['Valeurn'].sum()

    total_cred = valeur_CT+ valeur_MT + valeur_LT

    titre_pf = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Titres de placement et titres de l activité de portefeuille") ]
    v_titre = titre_pf['Valeurn'].sum()

    total_emp = vf.loc[(vf['Sigle Assujetti']  == m_bank) & (vf['Libelle Poste']  == "Total emplois-I+II") ]
    total_emploi = total_emp['Valeurn'].sum()

    autre_emploi = total_emploi-(total_cred + v_titre)

    return total_emploi, total_cred, v_titre, autre_emploi


def get_instru_banks(v, m_bank, m_date):
    
    m_data = []
    l_instru = [ 'Crédits à long terme', 
    'Crédits à moyen terme',
    'Crédits à court terme',
    'Crédits de campagne',
    'Crédit de location-financement', 'Affacturage',
    'Titres de transaction',
    'Titres d investissement',
    'Titres de placement et Autres']

    for i in l_instru:
        v = v.loc[str(m_date)]
        V_LT = v.loc[(v['Sigle Assujetti']  == m_bank) & (v['Libelle Poste']  == i) ]
        V_LT = round(V_LT['Valeurn'].sum()/1000,2)
        m_data.append(V_LT)

    #print(m_data)
    df = pd.DataFrame({'Instru':l_instru, 'value':m_data})
    df.sort_values(ascending= False,by='value', inplace= True)
    return df.Instru.values, df.value.values

def top_ranking_bank(v, m_date, m_poste):
    m_data = []
    list_bank = v['Sigle Assujetti'].unique()
    for i in list_bank:
        v = v.loc[str(m_date)]
        V_LT = v.loc[(v['Sigle Assujetti']  == i) & (v['Libelle Poste']  == m_poste) ]
        V_LT = round(V_LT['Valeurn'].sum()/1000, 2)
        m_data.append(V_LT)

    df = pd.DataFrame({'Bank':list_bank, 'value':m_data})#m_data
    df.sort_values(ascending= False,by='value', inplace= True)
    return df.Bank.values[:7], df.value.values[:7]

def flop_ranking_bank(v, m_date, m_poste):
    m_data = []
    list_bank = v['Sigle Assujetti'].unique()
    for i in list_bank:
        v = v.loc[str(m_date)]
        V_LT = v.loc[(v['Sigle Assujetti']  == i) & (v['Libelle Poste']  == m_poste) ]
        V_LT = round(V_LT['Valeurn'].sum()/1000, 2)
        m_data.append(V_LT)

    df = pd.DataFrame({'Bank':list_bank, 'value':m_data})#m_data
    df.sort_values(ascending= True,by='value', inplace= True)

    flop_vf = df.loc[df['value'] >=1]
    flop_max = df.loc[df['value'] <1]
    return flop_vf.Bank.values[:7], flop_vf.value.values[:7], flop_max.Bank.values.tolist()[:5], len(flop_max)


def get_radar_data(vf, m_year, m_bank): 

    m_data = []
    m_poste=["Crédits nets", "Créances nets en souffrance", "Caisse","Creances douteuses ou litigieuses", "Crédits à court terme",
               "Capitaux propres et ressources assimilés", "Capital-Dotation-Réserves",
               "Dépots et emprunts à terme", "Depots clientelle à terme","Excedent ou deficit"]
    
    for i in m_poste:
        v = vf.loc[str(m_year)]
        V_LT = v.loc[(v['Sigle Assujetti']  == m_bank) & (v['Libelle Poste']  == i)]
        V_LT = round(V_LT['Valeurn'].sum()/1000, 2)

        if V_LT <0: V_LT = 0
        m_data.append(V_LT)

    return m_data

def get_solidite_ratio(df, m_bank):

    l_solvabilite_globale = []
    l_fonds_propres = []

    for i in ['2018','2019','2021','2022','2023','2024']:
        v_1 = df.loc[i]
        V = v_1.loc[(v_1['Libelle Poste']  == "Capitaux propres et ressources assimilés") & (v_1['Sigle Assujetti']  == m_bank) ]
        val_capitaux = V['Valeurn'].sum()
        # print('Capitaux prop', val_capitaux)

        v_2 = df.loc[i]
        V = v_2.loc[(v_2['Libelle Poste']  == "Total emplois-I+II") & (v_2['Sigle Assujetti']  == m_bank) ]
        tot_emplois = V['Valeurn'].sum()

        v_3 = df.loc[i]
        V = v_3.loc[(v_3['Libelle Poste']  == "Autres fonds propres") & (v_3['Sigle Assujetti']  == m_bank) ]
        autr_FP = V['Valeurn'].sum()

        v_4 = df.loc[i]
        V = v_4.loc[(v_4['Libelle Poste']  == "Capital-Dotation-Réserves") & (v_4['Sigle Assujetti']  == m_bank) ]
        dot_reserve = V['Valeurn'].sum()
        # print('num', dot_reserve+autr_FP)

        ratio = round((val_capitaux/tot_emplois)*100, 2)
        l_solvabilite_globale.append(ratio)

        ratio = round(((dot_reserve+autr_FP)/tot_emplois)*100, 2)
        l_fonds_propres.append(ratio)

    return l_solvabilite_globale, l_fonds_propres

def get_liquidite_ratio(df, m_bank):

    l_liquidity_imm = []
    l_empl_ress = []

    for i in ['2018','2019','2021','2022','2023','2024']:
        v_1 = df.loc[i]
        V = v_1.loc[(v_1['Libelle Poste']  == "Caisse") & (v_1['Sigle Assujetti'] == m_bank) ]
        val_caisse = V['Valeurn'].sum()

        v_2 = df.loc[i]
        V = v_2.loc[(v_2['Libelle Poste']  == "Operations de tresorerie et inetbancaires") & (v_2['Sigle Assujetti'] == m_bank) ]
        treso = V['Valeurn'].sum()

        v_3 = df.loc[i]
        V = v_3.loc[(v_3['Libelle Poste']  == "Comptes ordinaires crediteurs") & (v_3['Sigle Assujetti'] == m_bank) ]
        compte_cred = V['Valeurn'].sum()

        v_4 = df.loc[i]
        V = v_4.loc[(v_4['Libelle Poste']  == "Total emplois-I+II") & (v_4['Sigle Assujetti'] == m_bank) ]
        tot_emploi= V['Valeurn'].sum()

        v_5 = df.loc[i]
        V = v_5.loc[(v_5['Libelle Poste']  == "Total ressources- III+IV+V") & (v_5['Sigle Assujetti'] == m_bank) ]
        tot_ress= V['Valeurn'].sum()

        ratio_1 = round((tot_emploi/tot_ress)*100, 2)
        l_empl_ress.append(ratio_1)

        ratio_2 = round(((val_caisse+treso)/compte_cred)*100, 2)
        l_liquidity_imm.append(ratio_2)

    return l_liquidity_imm, l_empl_ress


def get_qualityPF(df, m_bank):
    l_creance_souff = [] #creance_souff/credit_nets
    l_creance_dout = [] #creance_dout/credit_nets
    l_couv_creance = [] #Depre/creance_souff

    for i in ['2018','2019','2021','2022','2023','2024']:
        v_1 = df.loc[i]
        V = v_1.loc[(v_1['Libelle Poste']  == "Creances douteuses ou litigieuses") & (v_1['Sigle Assujetti'] == m_bank) ]
        val_crean_douteuse = V['Valeurn'].sum()

        v_2 = df.loc[i]
        V_c_net = v_2.loc[(v_2['Libelle Poste']  == "Crédits nets") & (v_2['Sigle Assujetti'] == m_bank) ]
        val_cred_net = V_c_net['Valeurn'].sum()

        v_3 = df.loc[i]
        creance_souff = v_3.loc[(v_3['Libelle Poste']  == "Créances en souffrance") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_crea_souff = creance_souff['Valeurn'].sum()

        v_4 = df.loc[i]
        depreciation = v_4.loc[(v_4['Libelle Poste']  == "Depreciations") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_deprec = depreciation['Valeurn'].sum()

        ratio_1 = round((val_crea_souff/val_cred_net)*100, 2)
        l_creance_souff.append(ratio_1)

        ratio_2 = round((val_crean_douteuse/val_cred_net)*100, 2)
        l_creance_dout.append(ratio_2)

        ratio_3 = round((val_deprec/val_crea_souff)*100, 2)
        l_couv_creance.append(ratio_3)

    return l_creance_souff, l_creance_dout, l_couv_creance

def get_rentability(df, m_bank):

    l_ROA = [] # Excedent ou deficit/total emploi
    l_ROE = [] # Excedent ou deficit/cap propr

    for i in ['2018','2019','2021','2022','2023','2024']:
        v_1 = df.loc[i]
        V = v_1.loc[(v_1['Libelle Poste']  == "Excedent ou deficit") & (v_1['Sigle Assujetti'] == m_bank) ]
        val_execedent = V['Valeurn'].sum()

        v_2 = df.loc[i]
        V_emploi = v_2.loc[(v_2['Libelle Poste']  == "Total emplois-I+II") & (v_2['Sigle Assujetti'] == m_bank) ]
        val_emplois = V_emploi['Valeurn'].sum()

        v_3 = df.loc[i]
        cap_prop = v_3.loc[(v_3['Libelle Poste']  == "Capitaux propres et ressources assimilés") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_cap_prop = cap_prop['Valeurn'].sum()

        ratio_1 = round((val_execedent/val_emplois)*100, 2)
        l_ROA.append(ratio_1)

        ratio_2 = round((val_execedent/val_cap_prop)*100, 2)
        l_ROE.append(ratio_2)


    return l_ROA, l_ROE


def get_structure(df, m_bank):

    l_tx_interm = [] # credit nets/total emploi
    l_autonomie = [] # cap propr/Total ress
    l_depot_stab = [] # (depot client+Compte epargne)/Total ress


    for i in ['2018','2019','2021','2022','2023','2024']:
        v_1 = df.loc[i]
        V = v_1.loc[(v_1['Libelle Poste']  == "Crédits nets") & (v_1['Sigle Assujetti'] == m_bank) ]
        credit_net = V['Valeurn'].sum()

        v_2 = df.loc[i]
        V_emploi = v_2.loc[(v_2['Libelle Poste']  == "Total emplois-I+II") & (v_2['Sigle Assujetti'] == m_bank) ]
        val_emplois = V_emploi['Valeurn'].sum()

        v_3 = df.loc[i]
        cap_prop = v_3.loc[(v_3['Libelle Poste']  == "Capitaux propres et ressources assimilés") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_cap_prop = cap_prop['Valeurn'].sum()

        v_4 = df.loc[i]
        tot_ress = v_4.loc[(v_4['Libelle Poste']  == "Total ressources- III+IV+V") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_tot_ress = tot_ress['Valeurn'].sum()

        v_5 = df.loc[i]
        dep_client = v_5.loc[(v_5['Libelle Poste']  == "Depots clientelle à terme") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_dep_client = dep_client['Valeurn'].sum()

        v_6 = df.loc[i]
        reg_special = v_6.loc[(v_6['Libelle Poste']  == "Comptes d epargne à regime special") & (v_3['Sigle Assujetti'] == m_bank) ]
        val_reg_special = reg_special['Valeurn'].sum()

        ratio_1 = round((credit_net/val_emplois)*100, 2)
        l_tx_interm.append(ratio_1)

        ratio_2 = round((val_cap_prop/val_tot_ress)*100, 2)
        l_autonomie.append(ratio_2)

        ratio_3 = round(((val_reg_special+val_dep_client)/val_tot_ress)*100, 2)
        l_depot_stab.append(ratio_3)


    return l_tx_interm, l_autonomie, l_depot_stab