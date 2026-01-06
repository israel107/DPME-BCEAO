import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import PME_analyse as pa
import charts as ch
import numpy as np
from pathlib import Path

st.set_page_config(page_title="DPME Dashboard", page_icon="📈", layout="wide")
st.markdown("<h2 style='text-align: left; font-size: 40px;  font-weight: bold;'>Tableau de bord du DPME</h2>", unsafe_allow_html=True)
BASE_DIR = Path(__file__).parent

# -------------------------------
# DATA & VARIABLES
# -------------------------------

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

@st.cache_data
def load_data(path, feuille):
    return pd.read_excel(path, sheet_name=feuille)

df_ALL = load_data('./PME_ALL_Dec_2025.xlsx', ["data_2018", "data_2019","data_2020","data_2021","data_2022",
                                                                                                 "data_2024" ])
df_2023 = load_data("./PME_2023_DEC.xlsx", "data_2023")

df_2018 = df_ALL['data_2018']
df_2019 = df_ALL['data_2019']
df_2020 = df_ALL['data_2020']
df_2021 = df_ALL['data_2021']
df_2022 = df_ALL['data_2022']
df_2024 = df_ALL['data_2024']

data_2018 = df_2018.sort_values(ascending=True, by='Arrete')
df_2018_dx = data_2018.set_index(['Arrete'])

data_2019 = df_2019.sort_values(ascending=True, by='Arrete')
df_2019_dx = data_2019.set_index(['Arrete'])

data_2020 = df_2020.sort_values(ascending=True, by='Arrete')
df_2020_dx = data_2020.set_index(['Arrete'])

data_2021 = df_2021.sort_values(ascending=True, by='Arrete')
df_2021_dx = data_2021.set_index(['Arrete'])

data_2022 = df_2022.sort_values(ascending=True, by='Arrete')
df_2022_dx = data_2022.set_index(['Arrete'])

data_2023 = df_2023.sort_values(ascending=True, by='Arrete')
df_2023_dx = data_2023.set_index(['Arrete'])

data_2024 = df_2024.sort_values(ascending=True, by='Arrete')
df_2024_dx = data_2024.set_index(['Arrete'])

all_pays = ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo","UEMOA"]

nbr_SAE_UEMOA = sum([12,18,10,5,8, 16, 33, 26])
df_SAE = pd.DataFrame({
    "Pays": all_pays,
    "Nombre SAE":[12,18,10,5,8, 16, 33, 26, nbr_SAE_UEMOA]
})

all_years = ['2018','2019','2020','2021','2022','2023']

all_period = ['Mensuel','Trimestriel','Semestriel','Annuel']

tab_instru = ["Portefeuille d'effets commerciaux  ", 'Credits a la clientele  ','Credits a long terme  ', 
              'Affacturage  ','Autres a court terme  ', 'Credit de location-financement  ',
    'Credits a moyen terme  ', 'Creances en souffrance  ']

list_bank = df_2024_dx['Sigle Assujetti'].unique()

# -----------------------------------------------------------------------------------------------------------------------------------
# SLIDE BAR
# -----------------------------------------------------------------------------------------------------------------------------------

with st.sidebar:
    m_pays = st.selectbox('Pays', all_pays, 0)
    m_period_DPME = st.selectbox('Périodes DPME', ['juin 2021','déc 2021','juin 2022','déc 2022','juin 2023','déc 2023','juin 2024','déc 2024'], 0)
    v_annee = st.slider("Années", 2018, 2023, 2022)
    multi_pays = st.multiselect('Select instrument (chart line)', all_pays, ['Bénin',"Burkina Faso"])
    m_bank = st.selectbox('Banques', list_bank, 0)
     
    
l_res = []
for i in ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"]:
    df_P_2018 = df_2018_dx.loc[df_2018_dx['Libelle Pays']  == i]
    val_P_2018 = round(df_P_2018['Valeurn'].sum()/1000,2)

    df_P_2019 = df_2019_dx.loc[df_2019_dx['Libelle Pays']  == i]
    val_P_2019 = round(df_P_2019['Valeurn'].sum()/1000,2)

    df_P_2020 = df_2020_dx.loc[df_2020_dx['Libelle Pays']  == i]
    val_P_2020 = round(df_P_2020['Valeurn'].sum()/1000,2)

    df_P_2021 = df_2021_dx.loc[df_2021_dx['Libelle Pays']  == i]
    val_P_2021 = round(df_P_2021['Valeurn'].sum()/1000,2)

    df_P_2022 = df_2022_dx.loc[df_2022_dx['Libelle Pays']  == i]
    val_P_2022 = round(df_P_2022['Valeurn'].sum()/1000,2)

    df_P_2023 = df_2023_dx.loc[df_2023_dx['Libelle Pays']  == i]
    val_P_2023 = round(df_P_2023['Valeurn'].sum()/1000,2)

    df_P_2024 = df_2024_dx.loc[df_2024_dx['Libelle Pays']  == i]
    val_P_2024 = round(df_P_2024['Valeurn'].sum()/1000,2)

    l_res.append([val_P_2018, val_P_2019, val_P_2020, val_P_2021, val_P_2022, val_P_2023, val_P_2024])

df_pays = pd.DataFrame({
    "years": ['2018','2019','2020','2021','2022','2023','2024'],
    "Bénin": l_res[0],
    "Burkina Faso": l_res[1],
    "Côte d Ivoire": l_res[2],
    "Guinée Bissau": l_res[3],
    "Mali": l_res[4],
    "Niger": l_res[5],
    "Sénégal": l_res[6],
    "Togo": l_res[7],

})

mot = pa.get_preposition(m_pays)

# ------------------------------------------------------------------------------------------------------------------------------------
# EXPANDER
# -------------------------------------------------------------------------------------------------------------------------------------

PME_benef, tx_benef = pa.get_PME_benef(m_pays, m_period_DPME)
# print(PME_benef, tx_benef)
PME_accomp, tx_accomp = pa.get_PME_accompagn(m_pays, m_period_DPME)
montant_accorde, tx_accord = pa.get_montant_accordes(m_pays, m_period_DPME)
nbr_SAE = pa.get_Nombre_SAE(df_SAE, m_pays)

com_benef, com_accompagne, com_montant = pa.get_commentaire_expander(m_pays, m_period_DPME)

st.markdown('#### STATISTIQUES DPME')

# Transformer les séparators , en .
montant_accorde_fr = f"{montant_accorde:,.0f}".replace(",", ".")
tx_accord_fr = f"{tx_accord:,.2f}%".replace(",", ".")

PME_benef_fr = f"{PME_benef:,.0f}".replace(",", ".")
tx_benef_fr = f"{tx_benef:,.2f}%".replace(",", ".")

PME_accomp_fr = f"{PME_accomp:,.0f}".replace(",", ".")
tx_accomp_fr = f"{tx_accomp:,.2f}%".replace(",", ".")

with st.expander("##### STATISTIQUES " +m_pays+" en "+ m_period_DPME): #+m_pays+" en "+ m_period_DPME

    valeur1, valeur2, valeur3, valeur4 = st.columns(4, gap='small')

    with valeur1:
        st.metric(label="Crédit octroyé (Mns FCFA)", value=montant_accorde_fr, delta=tx_accord_fr)

    with valeur2:
        st.metric(label="Nombre de PME bénéficiaires", value=PME_benef_fr, delta=tx_benef_fr)

    with valeur3:
        st.metric(label="Nombre de PME accompagnées", value=PME_accomp_fr, delta=tx_accomp_fr )

    with valeur4:
        st.metric(label="Nombre de SAE", value=f"{nbr_SAE: ,.0f}", delta=f"{0:.2f}%")

    m_interpr = 20
    st.info("""
        **Commentaires** (_{}_)
            
        - {}
        - {}
        - {}
        - Le nombre de Structures d'Accompagnement et d'Encadrement (**SAE**) de juin 2021 à décembre 2024 a demeuré à **{}**.
        """.format(m_pays,com_benef, com_accompagne, com_montant, nbr_SAE))

# ------------------------------------------------------------------------------------------------------------------------------------
# TAB
# -------------------------------------------------------------------------------------------------------------------------------------

st.markdown('#### <u>Tendances</u>', unsafe_allow_html=True)

l_periode = ['juin 2021','déc 2021','juin 2022','déc 2022',
                 'juin 2023','déc 2023','juin 2024','déc 2024']
DPME_montant_financement = pa.get_DPME_montant_financement(m_pays)
nbr_PME_accompagn = pa.get_nbr_PME_accompagn(m_pays)
nbr_PME_benef = pa.get_nbr_PME_benef(m_pays)

l_pays, l_montant = pa.get_montant_PIE(m_period_DPME)
list_diff = pa.get_Waterfall_data(m_pays)
w_measure = ["relative", "relative","relative", "relative","relative", 
             "relative","relative","relative", "total"]

tab1, tab2, tab3 = st.tabs(["📊 Semestres", "📈 Pays", "⚙️ Situation Financière"])
# ------------------------------------------------------------------------------------------------------------------------------------
# TAB 1
# -------------------------------------------------------------------------------------------------------------------------------------
with tab1: 
    L0_col1, L0_col2, L0_col3 = st.columns(3, gap='small')
    with L0_col1:
        # fig = ch.bar_vertical(l_periode, DPME_montant_financement,"Evolution des montants de crédit octroyé aux PME "+mot+ " "+m_pays,"Semestre", "en Millions FCFA","15%",)
        fig = ch.bar_vertical(l_periode, DPME_montant_financement, "Evolution des montants de crédit octroyé aux PME<br> "+mot+ " "+m_pays,"En millions FCFA", "15%")
        st.plotly_chart(fig, width='stretch')

    with L0_col2:
        
        fig = ch.bar_vertical(l_periode, nbr_PME_accompagn, "Nombre de PME accompagnées dans le cadre<br> du DPME "+mot+ " "+m_pays,"Nombre", "5%")
        st.plotly_chart(fig, width='stretch')

    with L0_col3:
        fig = ch.bar_horizontal(nbr_PME_benef, l_periode,"Nombre de PME bénéficiaires de prêts dans le cadre<br> du DPME "+mot+ " "+m_pays,"Nombre", "Semestre","15%",)
        st.plotly_chart(fig, width='stretch')
# ------------------------------------------------------------------------------------------------------------------------------------
# TAB 2
# -------------------------------------------------------------------------------------------------------------------------------------
with tab2:
    Tab2_col1, Tab2_col2, = st.columns(2, gap='small')

    with Tab2_col1:
        BC_colors = ['rgb(133, 32, 12)','rgb(130, 32, 12)', 'rgb(190, 72, 48)', 'rgb(194, 72, 48)', 'rgb(228, 185, 176)', 'rgb(220, 185, 176)', 'rgb(220, 185, 176)', 'rgb(205, 185, 176)']

        if m_period_DPME[:3] == "déc":
            m_period_DPME = "décembre " +m_period_DPME[-4:]

        fig = ch.chart_pie(l_pays, l_montant ,BC_colors, m_hole=.3, m_size_font=16,
                            m_titre='Part des crédits octroyés par les banques en '+ m_period_DPME+" (en millions FCFA)")
        st.plotly_chart(fig, width='stretch')

    with Tab2_col2:
        w_periode = ['juin 2021','déc 2021','juin 2022','déc 2022',
                 'juin 2023','déc 2023','juin 2024','déc 2024', "total"]
        
        fig = ch.chart_Waterfall(w_periode, list_diff, "Evolution des crédits octroyés aux PME "+mot+" "+m_pays+" (en millions FCFA)", w_measure)
        st.plotly_chart(fig, width='stretch')


# ------------------------------------------------------------------------------------------------------------------------------------
# TAB 3
# -------------------------------------------------------------------------------------------------------------------------------------

with tab3:
    L1_col1, L1_col2, L1_col3 = st.columns(3, gap='small')
    l_val = 0
    with L1_col1:
        if v_annee == 2018:
            l_val = pa.get_value_par_pays(df_2018_dx)
        elif v_annee == 2019:
            l_val = pa.get_value_par_pays(df_2019_dx)
        elif v_annee == 2020:
            l_val = pa.get_value_par_pays(df_2019_dx)
        elif v_annee == 2021:
            l_val = pa.get_value_par_pays(df_2021_dx)
        elif v_annee == 2022:
            l_val = pa.get_value_par_pays(df_2022_dx)
        elif v_annee == 2023:
            l_val = pa.get_value_par_pays(df_2023_dx)
        elif v_annee == 2024:
            l_val = pa.get_value_par_pays(df_2024_dx)
        
        fig = ch.bar_vertical(['Bénin',"Burkina Faso","Côte d'Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"],
                            l_val, 'Evolution du financement des PME en '+ str(v_annee), 'Milliards FCFA',"10%")
        st.plotly_chart(fig, width='stretch')

    with L1_col2:
        fig = ch.scatterMultiSelect(all_years, multi_pays, df_pays, 'Evolution du financement des PME par année', "Milliards FCFA")

        st.plotly_chart(fig, width='stretch')

    with L1_col3:
        data_sel = 0
        l_instru = []
        if v_annee == 2018:
            data_sel = df_2018_dx.loc[df_2018_dx['Libelle Pays'] == m_pays]
        elif v_annee == 2019:
            data_sel = df_2019_dx.loc[df_2019_dx['Libelle Pays'] == m_pays]
        elif v_annee == 2020:
            data_sel = df_2020_dx.loc[df_2020_dx['Libelle Pays'] == m_pays]
        elif v_annee == 2021:
            data_sel = df_2021_dx.loc[df_2021_dx['Libelle Pays'] == m_pays]
        elif v_annee == 2022:
            data_sel = df_2022_dx.loc[df_2022_dx['Libelle Pays'] == m_pays]
        elif v_annee == 2023:
            data_sel = df_2023_dx.loc[df_2023_dx['Libelle Pays'] == m_pays]
        elif v_annee == 2024:
            data_sel = df_2024_dx.loc[df_2024_dx['Libelle Pays'] == m_pays]
        
        for i in tab_instru:
            df_com = data_sel.loc[data_sel['POSTE'] == i]
            val = round(df_com['Valeurn'].sum()/1000, 2)

            l_instru.append(val)

        
        df_instru = pd.DataFrame({
            'res': l_instru,
            'Instru': tab_instru
        })
        vf_instru = df_instru.sort_values(ascending=False, by="res")

        fig = ch.bar_vertical(vf_instru['Instru'].values, vf_instru['res'].values, "Classement des Instruments en "+str(v_annee)+" <u>"+m_pays+"</u>", "Milliards FCFA", "20%")
        # fig.update_layout(margin = dict(t=0, l=0, r=0, b=10))


        st.plotly_chart(fig, width='stretch')
# ------------------------------------------------------------------------------------------------------------------------------------
# LIGNE 2
# -------------------------------------------------------------------------------------------------------------------------------------
st.divider()
st.markdown('#### <u>Banques</u>', unsafe_allow_html=True)
L2_col1, L2_col2 = st.columns([1, 2], gap='small')

with L2_col1:
    
    df_2018 = df_2018_dx.loc[df_2018_dx['Sigle Assujetti'] == m_bank]
    vf_2018 = round(df_2018['Valeurn'].sum()/1000,2)

    df_2019 = df_2019_dx.loc[df_2019_dx['Sigle Assujetti'] == m_bank]
    vf_2019 = round(df_2019['Valeurn'].sum()/1000,2)

    df_2020 = df_2020_dx.loc[df_2020_dx['Sigle Assujetti'] == m_bank]
    vf_2020 = round(df_2020['Valeurn'].sum()/1000, 2)

    df_2021 = df_2021_dx.loc[df_2021_dx['Sigle Assujetti'] == m_bank]
    vf_2021 = round(df_2021['Valeurn'].sum()/1000,2)

    df_2022 = df_2022_dx.loc[df_2022_dx['Sigle Assujetti'] == m_bank]
    vf_2022 = round(df_2022['Valeurn'].sum()/1000,2)

    df_2023 = df_2023_dx.loc[df_2023_dx['Sigle Assujetti'] == m_bank]
    vf_2023 = round(df_2023['Valeurn'].sum()/1000,2)

    df_2024 = df_2024_dx.loc[df_2024_dx['Sigle Assujetti'] == m_bank]
    vf_2024 = round(df_2024['Valeurn'].sum()/1000,2)

    l_res = [vf_2018, vf_2019, vf_2020, vf_2021, vf_2022, vf_2023, vf_2024]

    fig = ch.bar_horizontal(l_res, all_years, "Capitaux octroyés aux PME par "+m_bank,"Milliards FCFA","Années", "15%")
    st.plotly_chart(fig, width='stretch')

with L2_col2:

    data_sel = 0
    choix_list = 0
    l_mois_avt_2023 = ["3101","2802","3103","3004","3105","3006","3107","3108","3009","3110","3011","3112"]
    l_mois = ["31/01","28/02","31/03","30/04","31/05","30/06","31/07","31/08","30/09","31/10","30/11","31/12"]
    m_year = ""

    if v_annee == 2018:
        data_sel = df_2018_dx.loc[df_2018_dx['Sigle Assujetti'] == m_bank]
        choix_list = l_mois_avt_2023
        m_year = "2018 00:00:00"
    elif v_annee == 2019:
        choix_list = l_mois_avt_2023
        data_sel = df_2019_dx.loc[df_2019_dx['Sigle Assujetti'] == m_bank]
        m_year = "2019 00:00:00"
    elif v_annee == 2020:
        choix_list = l_mois_avt_2023
        data_sel = df_2020_dx.loc[df_2020_dx['Sigle Assujetti'] == m_bank]
        m_year = "2020 00:00:00"
        l_mois[1] = "2902"
    elif v_annee == 2021:
        choix_list = l_mois_avt_2023
        data_sel = df_2021_dx.loc[df_2021_dx['Sigle Assujetti'] == m_bank]
        m_year = "2021 00:00:00"
    elif v_annee == 2022:
        choix_list = l_mois_avt_2023
        data_sel = df_2022_dx.loc[df_2022_dx['Sigle Assujetti'] == m_bank]
        m_year = "2022 00:00:00"
    elif v_annee == 2023:
        data_sel = df_2023_dx.loc[df_2023_dx['Sigle Assujetti'] == m_bank]
        choix_list = l_mois
        m_year = "/2023 00:00:00"
    elif v_annee == 2024:
        data_sel = df_2024_dx.loc[df_2024_dx['Sigle Assujetti'] == m_bank]
        choix_list = l_mois
        m_year = "/2024 00:00:00"
        l_mois[1] = "29/02"

    l_resul = []
    vf_reset = data_sel.reset_index() 
    # print("vf reset", vf_reset['Valeurn'].sum())

    for i in choix_list:
        m_ch = i+m_year
        # print("year", m_ch)
        val_mois = vf_reset.loc[vf_reset['Arrete'] == m_ch ]
        #print("Val mois",val_mois['Valeurn'].sum())
        l_resul.append(round(val_mois['Valeurn'].sum()/1000, 2))

    # print(l_resul)
    fig = ch.bar_vertical(["Janv","Fev","Mars","Avr","Mai","Juin","Juil",
                           "Août","Sept","Oct","Nov","Dec"], l_resul, "Evolution mensuelle du financement des PME par "+m_bank+" en "+str(v_annee), "Milliard FCFA","15%",
                           'rgb(133, 32, 12)')
    st.plotly_chart(fig, width='stretch')
# ------------------------------------------------------------------------------------------------------------------------------------
# LIGNE 3
# -------------------------------------------------------------------------------------------------------------------------------------
st.divider()
st.markdown('#### <u>Contribution des banques</u>', unsafe_allow_html=True)
L3_col1, L3_col2 = st.columns(2, gap='small')
BC_colors = ['rgb(133, 32, 12)', 'rgb(194, 72, 48)', 'rgb(228, 185, 176)']

with L3_col1:
    if v_annee == 2018:
        l_val = pa.get_contrib_par_pays(df_2018_dx)
    elif v_annee == 2019:
        l_val = pa.get_contrib_par_pays(df_2019_dx)
    elif v_annee == 2020:
        l_val = pa.get_contrib_par_pays(df_2020_dx)
    elif v_annee == 2021:
        l_val = pa.get_contrib_par_pays(df_2021_dx)
    elif v_annee == 2022:
        l_val = pa.get_contrib_par_pays(df_2022_dx)
    elif v_annee == 2023:
        l_val = pa.get_contrib_par_pays(df_2023_dx)
    elif v_annee == 2024:
        l_val = pa.get_contrib_par_pays(df_2024_dx)

    fig = ch.chart_pie(all_pays[:-1], l_val, BC_colors, m_hole=.3, m_size_font=16,  m_titre='Contribution des banques au financement des PME présentée des banques sises dans les Etats dans le  ' + str(v_annee))
    st.plotly_chart(fig, width='stretch')


with L3_col2:

    data_sel = 0
    if v_annee == 2018:
        data_sel = df_2018_dx.loc[df_2018_dx['Libelle Pays'] == m_pays]

    elif v_annee == 2019:
        data_sel = df_2019_dx.loc[df_2019_dx['Libelle Pays'] == m_pays]

    elif v_annee == 2020:
        data_sel = df_2020_dx.loc[df_2020_dx['Libelle Pays'] == m_pays]

    elif v_annee == 2021:
        data_sel = df_2021_dx.loc[df_2021_dx['Libelle Pays'] == m_pays]

    elif v_annee == 2022:
        data_sel = df_2022_dx.loc[df_2022_dx['Libelle Pays'] == m_pays]

    elif v_annee == 2023:
        data_sel = df_2023_dx.loc[df_2023_dx['Libelle Pays'] == m_pays]
    
    elif v_annee == 2024:
        data_sel = df_2024_dx.loc[df_2024_dx['Libelle Pays'] == m_pays]
    

    l_bank = data_sel['Sigle Assujetti'].unique()
    l_resul = []

    for i in l_bank:
        f_pays = data_sel.loc[data_sel['Sigle Assujetti'] == i]
        val = round(f_pays['Valeurn'].sum()/1000,2)
        l_resul.append(val)


    df_bank = pd.DataFrame({
        'valeur': l_resul,
        'Bank': l_bank
    }) #l_resul
    vf = df_bank.sort_values(by="valeur", ascending=False)[:7]

    

    fig = ch.bar_vertical(vf['Bank'].values, vf['valeur'].values, "Classement des banques en "+ str(v_annee) +" "+mot +" "+m_pays, "Milliards FCFA","30%", 'rgb(228, 185, 176)')
    st.plotly_chart(fig, width='stretch')
# ------------------------------------------------------------------------------------------------------------------------------------
# LIGNE Recap
# -------------------------------------------------------------------------------------------------------------------------------------
st.divider()
st.markdown('#### <u>Récap.</u>', unsafe_allow_html=True)
L4_col1, L4_col2 = st.columns(2, gap='small')

with L4_col1:
    st.info("""
        **POINTS FORTS**
            

        - 20% de fonds investi
        - Montant croissant
        - nombre important de banques
        """)


with L4_col2:
    st.error("**"+"POINTS FAIBLES"+"**")

st.divider()
st.markdown('#### <u>Données</u>', unsafe_allow_html=True)
L4_col1, L4_col2 = st.columns(2, gap='small')