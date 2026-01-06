import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import analyse as al
import charts as ch
from pathlib import Path

st.set_page_config(page_title="Bank Dashboard", page_icon="🏦", layout="wide")

BASE_DIR = Path(__file__).parent
st.markdown("<h2 style='text-align: left; font-size: 40px;  font-weight: bold;'>Tableau de bord du secteur bancaire</h2>", unsafe_allow_html=True)
st.image("./pays_uemoa_png.png", caption="", width='content')
st.markdown("_DABFA-SFE v0.0.1_")

#graphs will use css
theme_plotly = None

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

@st.cache_data
def load_data(path):
    return pd.read_excel(path)

df_data = load_data("./Data_python.xlsx")
v = df_data.sort_values(ascending=True, by='Arrete')
v = v.set_index(['Arrete'])

v["Libelle Poste"] = v["Libelle Poste"].replace("Titres de placement et titres de l activité de portefeuille", "Titres de placement et Autres")



all_pays = ['Bénin',"Burkina Faso","Côte d'Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo","UEMOA"]

all_years = ['2018','2019','2021','2022','2023','2024']

all_period = ['Mensuel','Trimestriel','Semestriel','Annuel']

m_post = ['Crédits nets','Crédits à long terme','Crédits à moyen terme', 'Crédits à court terme',
          'Affacturage', 'Crédits nets en souffrance','Crédit de location-financement',"Créances restructurées"]

m_instru = [ 'Crédits à long terme', 
        'Crédits à moyen terme',
        'Crédits à court terme',
        'Crédits de campagne',
        'Crédit de location-financement', 'Affacturage',
        'Titres de transaction',
        'Titres d investissement', 'Titres de placement et Autres'
        ]
m_bank = v['Sigle Assujetti'].unique()
#######################################
# SIDEBAR
#######################################

with st.sidebar:
    m_pays = st.selectbox('Pays (All charts)', all_pays, 0)
    v_annee = st.slider("Années (All charts)", 2018, 2024, 2022)
    v_instru = st.multiselect('Select instrument (Donut)', m_instru, ["Crédits à long terme", "Crédits à moyen terme", "Crédits à court terme"])
    v_periode = st.selectbox('Périodes (Tendances charts)', all_period)
    v_bank = st.selectbox('Banques (Etab. Crédit charts)', m_bank)
    un_instru = st.selectbox('Select unique instrument', m_instru )
     
v_depot, depot_delta = al.get_indicateur(v,'Dépots et emprunts',m_pays, v_annee)
v_treso, treso_delta = al.get_indicateur(v,'Operations de tresorerie et inetbancaires',m_pays, v_annee)
v_affact, affact_delta = al.get_indicateur(v,'Affacturage',m_pays, v_annee)
v_campagne, campagne_delta = al.get_indicateur(v,'Crédits de campagne',m_pays, v_annee)

st.markdown('### FINANCEMENT DES ACTEURS')
with st.expander("STATISTIQUES UEMOA"):

    valeur1, valeur2, valeur3, valeur4 = st.columns(4, gap='small')

    with valeur1:
        st.metric(label="Dépots et emprunts (Mds FCFA)", value=f"{v_depot: ,.0f}", delta=f"{depot_delta:.2f}%")

    with valeur2:
        st.metric(label="Operations de tresorerie (Mds FCFA)", value=f"{v_treso: ,.0f}", delta=f"{treso_delta:.2f}%" )

    with valeur3:
        st.metric(label="Affacturage (Mds FCFA)", value=f"{v_affact: ,.0f}", delta=f"{affact_delta:.2f}%")

    with valeur4:
        st.metric(label="Crédits de campagne (Mds FCFA)", value=f"{v_campagne: ,.0f}", delta=f"{campagne_delta:.2f}%" )

    m_interpr = al.conclusionStat(v_annee, m_pays, v_depot, depot_delta, v_treso, treso_delta, v_affact, affact_delta, v_campagne, campagne_delta)
    st.info("*_"+ m_interpr +"_*")


################################################# PAYS LIGNE 1###########################################################################
st.markdown('#### Instruments financiers présentés par Pays')
col1_1, col1_2, col1_3 = st.columns(3, gap='small')

with col1_1:
    v_post_1 = st.selectbox('Postes (Graphe 1)', m_post, 1)
    new_data_y_1 = al.get_autres_postes(v, v_annee, v_post_1)

    m_fig = ch.bar_vertical(['Bénin',"Burkina Faso","Côte d'Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"],
                            new_data_y_1, 'Evolution ' + v_post_1+ " en " + str(v_annee), 'Milliards (FCFA)',
                            "10%")
    
    st.plotly_chart(m_fig, width='stretch')
    

with col1_2:
    v_post_2 = st.selectbox('Postes (Graphe 2)', m_post, 2)
    new_data_y_2 = al.get_autres_postes(v, v_annee, v_post_2)

    m_fig = ch.bar_vertical(['Bénin',"Burkina Faso","Côte d'Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"],
                            new_data_y_2, 'Evolution ' + v_post_2 + " en " + str(v_annee), 'Milliards (FCFA)',
                            "30%", 'rgb(105, 46, 34)')
    
    st.plotly_chart(m_fig, width='stretch')

with col1_3:
    v_post_3 = st.selectbox('Postes (Graphe 3)', m_post, 3)
    new_data_y_3 = al.get_autres_postes(v, v_annee, v_post_3)

    m_fig = ch.bar_vertical(['Bénin',"Burkina Faso","Côte d'Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"],
                            new_data_y_3, 'Evolution ' + v_post_3 + " en " + str(v_annee), 'Milliards (FCFA)',
                            "60%", 'rgb(228, 185, 176)')
    
    st.plotly_chart(m_fig, width='stretch')


################################################# COUNTRY CHART LINE 2 ###########################################################################

col2_2, col2_1  = st.columns(2, gap='small')

res_vf = al.get_pourcentage_credit(v, m_pays, v_annee, v_instru)

with col2_1:
    BC_colors = ['rgb(133, 32, 12)', 'rgb(194, 72, 48)', 'rgb(228, 185, 176)']

    m_fig = ch.chart_pie(v_instru, res_vf, BC_colors, m_hole=.3, m_size_font=16,
                         m_titre='Part des instruments financiers en ' + str(v_annee))

    st.plotly_chart(m_fig, width='stretch')

vf_instru = al.get_classement_Instrument(v, m_pays, v_annee)

with col2_2:

    m_fig = ch.bar_horizontal(vf_instru.values, vf_instru.index, 'Instruments financiers les plus utilisés ' + str(v_annee),
                              x_titre='Milliards (FCFA)', y_titre="Instruments Fin.",m_corner="60%", m_color="rgb(228, 185, 176)")

    st.plotly_chart(m_fig, width='stretch')


x_value_LT, y_value_LT = al.get_credit(v,m_pays, 'Crédits à long terme',v_annee, v_periode )
x_value_MT, y_value_MT = al.get_credit(v, m_pays, 'Crédits à moyen terme',v_annee, v_periode )
x_value_CT, y_value_CT = al.get_credit(v, m_pays, 'Crédits à court terme',v_annee, v_periode )

res_date = al.get_Instrument_by_year(v, m_pays, un_instru)
m_conclu = al.conclusionStat_2lign(df_data, m_pays, v_annee, y_value_CT.sum(), y_value_MT.sum())
st.info("*_"+ m_conclu +"_*")

st.divider()

st.markdown('#### Tendances')
col1, col2 = st.columns(2, gap='small')

#####################################################"""""TENDANCES"""""###############################################TENDANCES###########

with col1:
    
    m_fig_1 = ch.scatterChart(m_x1=x_value_LT, m_x2=x_value_MT, m_x3=x_value_CT,
                            m_y1=y_value_LT, m_y2=y_value_MT, m_y3=y_value_CT,
                            grd_titre='Evolution du crédit à long, moyen et court terme en ' + str(v_annee),
                            y_title="Milliards FCFA",
                            m_col1="rgb(133, 32, 12)", m_col2="rgb(194, 72, 48)", m_col3='rgb(228, 185, 176)')
    
    st.plotly_chart(m_fig_1, width='stretch')

    ################################## CHART EN DESSOUS #####################


with col2:
    m_fig_2 = ch.bar_vertical(['2018','2019','2020','2021','2022','2023','2024'],
                            res_date, 'Montant '+ un_instru + " de 2018 à 2024", 'Milliards (FCFA)',
                            "10%", 'rgb(228, 185, 176)')
    
    st.plotly_chart(m_fig_2, width='stretch')

comp1, comp2 = st.columns(2, gap='small')

with comp1:
    v_post_2 = st.selectbox('Libellé Postes', m_instru, 2)
    x_value_MT, y_value_MT = al.get_credit(v, m_pays, v_post_2 ,v_annee, v_periode )
    

    m_fig_1 = ch.bar_vertical(x_value_MT,
                            y_value_MT,'Evolution ' + v_post_2 + str(v_annee), 'Milliards (FCFA)',
                            "30%", 'rgb(194, 72, 48)')
    
    st.plotly_chart(m_fig_1, width='stretch')

    ################################## CHART EN DESSOUS #####################
    

with comp2:
    v_post_3 = st.selectbox('Libellé Postes', m_instru, 3)
    x_value_CT, y_value_CT = al.get_credit(v, m_pays, v_post_3,v_annee, v_periode )

    m_fig_2 = ch.bar_vertical(x_value_CT,
                            y_value_CT,'Evolution '+ v_post_3 + str(v_annee), 'Milliards (FCFA)',
                            "40%", 'rgb(228, 185, 176)')
    st.plotly_chart(m_fig_2, width='stretch')

st.success("Commentaire Chart")

#####################################################"""""ETABLISSEMENT"""""###############################################ETABLISSEMENT###########
st.divider()
st.markdown('#### Etablissement de crédit')


top_bank, top_bank_value = al.top_ranking_bank(v, v_annee, un_instru)
flop_bank, flop_bank_value, flop_max, nbr_flop_max = al.flop_ranking_bank(v, v_annee, un_instru)
#print(len(flop_max))

col1_1, col1_2 = st.columns(2, gap='small')
with col1_1:

    m_fig_1 = ch.bar_vertical(top_bank,
                            top_bank_value,'Top 5 des banques (montant '+ un_instru + " en " +str(v_annee)+")", 'Milliards (FCFA)',
                            "25%", 'rgb(194, 72, 48)')
    st.plotly_chart(m_fig_1, width='stretch')


with col1_2:
    m_fig_2 = ch.bar_vertical(flop_bank,
                            flop_bank_value,'Flop 5 des banques (montant '+ un_instru + " en " +str(v_annee)+")", 'Milliards (FCFA)',
                            "25%", 'rgb(188, 92, 48)')
    st.plotly_chart(m_fig_2, width='stretch')

    if len(flop_max)>=4:
        st.info("Nombre de banques ayant un montant de "+ un_instru +" avoisinant zéro: **"+ str(nbr_flop_max) +"**. Quelques noms de banques : " +flop_max[0]+", "+flop_max[1]+", "+flop_max[2]+", "+flop_max[3]+'.')
    elif len(flop_max)== 1:
        st.info("Nombre de banques ayant un montant de "+ un_instru +" avoisinant zéro: **"+ str(nbr_flop_max) +"**. Le nom de la banque :" +flop_max[0]+".")
    elif len(flop_max)== 0:
        st.info("_pas de banques ayant un montant de "+ un_instru +" avoisinant zéro._")

top_instru, top_value = al.get_instru_banks(v, v_bank, v_annee)
top_instru = al.get_transform_colonne(top_instru)
# print(v)

col1, col2 = st.columns(2, gap='small')
with col1:

    m_fig_1 = ch.bar_vertical(top_instru,
                            top_value,'Classement des instruments (en mds FCFA) utilisés par '+ v_bank + " en " +str(v_annee), 'Milliards (FCFA)',
                            "25%", 'rgb(228, 185, 176)')
    st.plotly_chart(m_fig_1, width='stretch')

ress_list, emp_list = al.get_ress_empl(v, v_bank)
with col2: 
    ms_dates = ["2018","2019","2020","2021","2022","2023","2024"]
    m_fig = ch.doubleBar(ms_dates, ress_list, emp_list, 'Ressources & Emploi de '+ v_bank,'Milliards FCFA',
                         legend_1='Total Ressource', legend_2='Total Emploi', m_color1='rgb(228, 185, 176)', m_color2='rgb(194, 72, 48)')
    
    st.plotly_chart(m_fig, width='stretch')

b_col1, b_col2 = st.columns(2, gap='small')

l_ress_emploi = al.struct_emp_ressource(v, v_bank, v_annee)
# print(l_ress_emploi)
l_radar = al.get_radar_data(v, v_annee, v_bank)

with b_col1:

    
    labels = [
    "Répartition",
    "Emplois", "Ressources",
    "Crédit", "Portefeuille Titres", "Autres emplois",
    "F Propres", "Emprunts & Depot"
    ]

    parents = [
        "",          # Total
        "Répartition", "Répartition",
        "Emplois", "Emplois", "Emplois",
        "Ressources", "Ressources"
    ]
    values = [
    100,         # Total
    60, 40,      # Partie A / Partie B
    20, 25, 15,  # A1 / A2 / A3
    10, 30   # B1 / B2 / B3
]
    m_values = l_ress_emploi 

    fig = ch.m_SunBurts(labels, parents, m_values, "Emplois vs Ressources "+v_bank+" (en mds FCFA)")

    st.plotly_chart(fig, width='stretch')

with b_col2:
    fig = ch.m_polarChart(l_radar[0],l_radar[1],l_radar[2],l_radar[3],l_radar[4],l_radar[5],
                          l_radar[6],l_radar[7],l_radar[8],l_radar[9], v_bank)
    st.plotly_chart(fig, width='stretch')

#####################################################"""""RATIOS"""""###############################################RATIOS###########
st.divider()
st.markdown('#### Ratios')

st.markdown('##### _*Solidité*_')
#Taux net de dégradation du portefeuille
#Taux de provisionnement
#Ratio de solvabilité
col1_1, col1_2, col1_3 = st.columns(3, gap='small')
l_solvabilite_globale, l_fonds_propres = al.get_solidite_ratio(v, v_bank)
 
l_liquidity_imm, l_empl_ress = al.get_liquidite_ratio(v, v_bank)
l_creance_souff, l_creance_dout, l_couv_creance = al.get_qualityPF(v, v_bank)

with col1_1:
    fig = ch.scatterRatios(['2018','2019','2021','2022','2023','2024'], l_solvabilite_globale, l_fonds_propres,
                           "Ratios de solvabilité & Fonds propres de <u>"+v_bank +"</u>","Pourcentage (%)", "Solvabilité Globale","R. de Fonds Prop.")
    st.plotly_chart(fig, width='stretch')

with col1_2:
    fig = ch.scatterRatios(['2018','2019','2021','2022','2023','2024'], l_liquidity_imm, l_empl_ress,
                           "Ratios de liquidité immédiate & Emplois-Ressources de <u>"+v_bank +"</u>","Pourcentage (%)","Liq. immédiate","emplois/ressources")
    st.plotly_chart(fig, width='stretch')

with col1_3:
    fig = ch.scatter_3_Ratios(['2018','2019','2021','2022','2023','2024'], l_creance_souff, l_creance_dout, l_couv_creance,
                              "Taux de créances en souffrance, créances douteuses et <br>de couv. des créances de <u>"+v_bank +"</u>","Pourcentage (%)",
                              "créances en souffrance","Créances douteuse","Couv. des créances douteuses")
    st.plotly_chart(fig, width='stretch')

st.markdown('##### _*Structure du Bilan & Rentabilité*_')

l_ROA, l_ROE = al.get_rentability(v, v_bank)

l_tx_interm, l_autonomie, l_depot_stab = al.get_structure(v, v_bank)

#####################################################"""""RECAP"""""###############################################RECAP###########
st.divider()
st.markdown('#### Récap.')

L4_col1, L4_col2 = st.columns(2, gap='small')

with L4_col1:
    st.info("""
        **POINTS FORTS**
            

        - xxx
        - xxx
        - xxx
        """)


with L4_col2:
    st.error("**"+"POINTS FAIBLES"+"**")

