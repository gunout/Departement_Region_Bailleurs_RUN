import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Bailleurs Sociaux - Île de la Réunion",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #2E7D32, #0288D1, #FF9800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        color: #1976D2;
        border-bottom: 2px solid #FF9800;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0288D1;
        margin: 0.5rem 0;
    }
    .bailleur-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #FF9800;
        background-color: #f8f9fa;
    }
    .performance-high { background-color: #d4edda; border-left: 4px solid #28a745; }
    .performance-medium { background-color: #fff3cd; border-left: 4px solid #ffc107; }
    .performance-low { background-color: #f8d7da; border-left: 4px solid #dc3545; }
    .performance-excellent { background-color: #d1ecf1; border-left: 4px solid #17a2b8; }
    .microregion-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        color: white;
    }
    .nord { background-color: #0288D1; }
    .sud { background-color: #2E7D32; }
    .ouest { background-color: #FF9800; color: black; }
    .est { background-color: #7B1FA2; }
    .cirques { background-color: #5D4037; }
    .status-high { color: #28a745; font-weight: bold; }
    .status-medium { color: #ffc107; font-weight: bold; }
    .status-low { color: #dc3545; font-weight: bold; }
    .type-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
    }
    .social { background-color: #2196F3; }
    .intermediaire { background-color: #4CAF50; }
    .accession { background-color: #FF9800; }
    .renovation { background-color: #9C27B0; }
</style>
""", unsafe_allow_html=True)

class BailleursSociauxDashboard:
    def __init__(self):
        self.bailleurs_data = self.define_bailleurs_data()
        self.parc_data = self.initialize_parc_data()
        self.historical_data = self.initialize_historical_data()
        self.projets_data = self.initialize_projets_data()
        self.demande_data = self.initialize_demande_data()
        self.financement_data = self.initialize_financement_data()
        
    def define_bailleurs_data(self):
        """Définit les données des bailleurs sociaux de La Réunion"""
        return [
            {
                'nom': 'GRH - Groupe Réunionnaise pour l\'Habitat',
                'type': 'Groupe',
                'statut': 'Principal bailleur',
                'annee_creation': 2015,
                'parc_total': 24850,
                'logements_gestion': 24850,
                'logements_construction_an': 850,
                'chiffre_affaires': 145.2,
                'effectifs': 420,
                'taux_rotation': 8.2,
                'taux_impayes': 2.1,
                'dette_par_logement': 38500,
                'investissement_annuel': 68.5,
                'performance_gestion': 'Excellente',
                'quartiers_prioritaires': 45,
                'taux_renovation_energetique': 35,
                'lat': -20.8789,
                'lon': 55.4481,
                'siege': 'Saint-Denis',
                'description': 'Principal bailleur social, fusion de plusieurs organismes'
            },
            {
                'nom': 'SIDR - Société Immobilière Départementale',
                'type': 'SEM',
                'statut': 'Bailleur départemental',
                'annee_creation': 1975,
                'parc_total': 4850,
                'logements_gestion': 4850,
                'logements_construction_an': 220,
                'chiffre_affaires': 42.8,
                'effectifs': 95,
                'taux_rotation': 7.8,
                'taux_impayes': 1.8,
                'dette_par_logement': 32500,
                'investissement_annuel': 25.3,
                'performance_gestion': 'Élevée',
                'quartiers_prioritaires': 18,
                'taux_renovation_energetique': 42,
                'lat': -20.8820,
                'lon': 55.4501,
                'siege': 'Saint-Denis',
                'description': 'SEM départementale, parc diversifié'
            },
            {
                'nom': 'SEMADER',
                'type': 'SEM',
                'statut': 'Aménageur-constructeur',
                'annee_creation': 1980,
                'parc_total': 3200,
                'logements_gestion': 3200,
                'logements_construction_an': 180,
                'chiffre_affaires': 28.5,
                'effectifs': 65,
                'taux_rotation': 9.1,
                'taux_impayes': 2.8,
                'dette_par_logement': 35800,
                'investissement_annuel': 18.7,
                'performance_gestion': 'Moyenne',
                'quartiers_prioritaires': 12,
                'taux_renovation_energetique': 28,
                'lat': -21.3393,
                'lon': 55.4781,
                'siege': 'Saint-Pierre',
                'description': 'Spécialiste Sud et Ouest, forte croissance'
            },
            {
                'nom': 'Bat\'Promotion',
                'type': 'Promoteur',
                'statut': 'Constructeur social',
                'annee_creation': 1995,
                'parc_total': 1850,
                'logements_gestion': 1850,
                'logements_construction_an': 150,
                'chiffre_affaires': 22.1,
                'effectifs': 48,
                'taux_rotation': 6.5,
                'taux_impayes': 1.5,
                'dette_par_logement': 29800,
                'investissement_annuel': 15.2,
                'performance_gestion': 'Élevée',
                'quartiers_prioritaires': 8,
                'taux_renovation_energetique': 38,
                'lat': -20.8850,
                'lon': 55.4520,
                'siege': 'Saint-Denis',
                'description': 'Promoteur spécialisé en logement social'
            },
            {
                'nom': 'SEMAFOR',
                'type': 'SEM',
                'statut': 'Aménageur régional',
                'annee_creation': 1982,
                'parc_total': 2750,
                'logements_gestion': 2750,
                'logements_construction_an': 120,
                'chiffre_affaires': 19.8,
                'effectifs': 52,
                'taux_rotation': 8.5,
                'taux_impayes': 2.4,
                'dette_par_logement': 34200,
                'investissement_annuel': 12.5,
                'performance_gestion': 'Moyenne',
                'quartiers_prioritaires': 10,
                'taux_renovation_energetique': 31,
                'lat': -21.0097,
                'lon': 55.2697,
                'siege': 'Saint-Paul',
                'description': 'Développement territorial Ouest et Sud'
            },
            {
                'nom': 'Foyer Réunionnais',
                'type': 'Association',
                'statut': 'Logement d\'urgence',
                'annee_creation': 1978,
                'parc_total': 850,
                'logements_gestion': 850,
                'logements_construction_an': 30,
                'chiffre_affaires': 8.2,
                'effectifs': 28,
                'taux_rotation': 15.2,
                'taux_impayes': 4.2,
                'dette_par_logement': 18500,
                'investissement_annuel': 6.8,
                'performance_gestion': 'Faible',
                'quartiers_prioritaires': 22,
                'taux_renovation_energetique': 18,
                'lat': -20.8900,
                'lon': 55.4550,
                'siege': 'Saint-Denis',
                'description': 'Spécialiste hébergement social et urgence'
            },
            {
                'nom': 'SHLMR Réunion',
                'type': 'HLM',
                'statut': 'Historique',
                'annee_creation': 1960,
                'parc_total': 4200,
                'logements_gestion': 4200,
                'logements_construction_an': 80,
                'chiffre_affaires': 25.4,
                'effectifs': 78,
                'taux_rotation': 7.2,
                'taux_impayes': 1.9,
                'dette_par_logement': 41200,
                'investissement_annuel': 14.3,
                'performance_gestion': 'Élevée',
                'quartiers_prioritaires': 15,
                'taux_renovation_energetique': 45,
                'lat': -20.8750,
                'lon': 55.4460,
                'siege': 'Saint-Denis',
                'description': 'Bailleur historique, parc ancien rénové'
            }
        ]
    
    def initialize_parc_data(self):
        """Initialise les données détaillées du parc par bailleur"""
        data = []
        types_logement = ['PLAI', 'PLUS', 'PLS', 'Intermediaire', 'Accession', 'Etudiant', 'Senior']
        
        for bailleur in self.bailleurs_data:
            # Répartition aléatoire mais cohérente des types de logement
            np.random.seed(hash(bailleur['nom']) % 10000)
            
            for type_log in types_logement:
                proportion = np.random.uniform(5, 30)
                nombre = int(bailleur['parc_total'] * proportion / 100)
                loyer_moyen = np.random.uniform(150, 450)
                vacance = np.random.uniform(1, 8)
                
                data.append({
                    'bailleur': bailleur['nom'],
                    'type_logement': type_log,
                    'nombre_logements': nombre,
                    'proportion': proportion,
                    'loyer_moyen': loyer_moyen,
                    'taux_vacance': vacance
                })
        
        return pd.DataFrame(data)
    
    def initialize_historical_data(self):
        """Initialise les données historiques"""
        dates = pd.date_range('2015-01-01', datetime.now(), freq='Y')
        data = []
        
        for date in dates:
            for bailleur in self.bailleurs_data:
                years_passed = date.year - 2015
                trend_factor = 1 + (years_passed * 0.03)
                
                data.append({
                    'date': date,
                    'bailleur': bailleur['nom'],
                    'parc_total': bailleur['parc_total'] * 0.8 * trend_factor,
                    'logements_construits': bailleur['logements_construction_an'] * 0.9 * trend_factor,
                    'taux_impayes': bailleur['taux_impayes'] * (1 + np.random.normal(0, 0.1)),
                    'investissement': bailleur['investissement_annuel'] * 0.8 * trend_factor
                })
        
        return pd.DataFrame(data)
    
    def initialize_projets_data(self):
        """Initialise les données des projets en cours"""
        projets = []
        microregions = ['Nord', 'Sud', 'Ouest', 'Est']
        types_projet = ['Neuf', 'Rénovation', 'Réhabilitation', 'ANRU', 'Démolition-Reconstruction']
        
        for i in range(50):  # 50 projets simulés
            bailleur = np.random.choice([b['nom'] for b in self.bailleurs_data])
            microregion = np.random.choice(microregions)
            type_projet = np.random.choice(types_projet)
            
            projets.append({
                'nom_projet': f"Projet {i+1} - {microregion}",
                'bailleur': bailleur,
                'micro_region': microregion,
                'type_projet': type_projet,
                'logements_prevus': np.random.randint(20, 200),
                'investissement': np.random.uniform(5, 50),
                'date_debut': datetime.now() - timedelta(days=np.random.randint(0, 365)),
                'date_fin_prevue': datetime.now() + timedelta(days=np.random.randint(180, 720)),
                'avancement': np.random.uniform(10, 95),
                'statut': np.random.choice(['En étude', 'En travaux', 'En livraison', 'Terminé'])
            })
        
        return pd.DataFrame(projets)
    
    def initialize_demande_data(self):
        """Initialise les données de demande de logement social"""
        communes = ['Saint-Denis', 'Saint-Paul', 'Saint-Pierre', 'Le Tampon', 'Saint-Louis', 
                   'Saint-André', 'Saint-Benoît', 'Saint-Joseph', 'Sainte-Marie', 'Le Port']
        
        data = []
        for commune in communes:
            data.append({
                'commune': commune,
                'demande_totale': np.random.randint(800, 3500),
                'attente_moyenne_mois': np.random.uniform(18, 48),
                'taux_satisfaction': np.random.uniform(15, 40),
                'demande_urgence': np.random.randint(50, 300),
                'revenu_moyen_demandeur': np.random.uniform(1200, 2200)
            })
        
        return pd.DataFrame(data)
    
    def initialize_financement_data(self):
        """Initialise les données de financement"""
        financeurs = ['État', 'Région', 'Département', 'ANRU', 'Europe', 'Action Logement', 'CDC']
        data = []
        
        for financeur in financeurs:
            data.append({
                'financeur': financeur,
                'montant_annuel': np.random.uniform(10, 100),
                'type_aide': np.random.choice(['Subvention', 'Prêt', 'Avance', 'Garantie']),
                'taux_intervention': np.random.uniform(10, 40),
                'projets_soutenus': np.random.randint(5, 30)
            })
        
        return pd.DataFrame(data)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🏘️ Dashboard Bailleurs Sociaux - Île de la Réunion</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**Analyse stratégique du parc social réunionnais - Données 2024**")
        
        current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés du parc social"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DU PARC SOCIAL</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques globales
        parc_total = sum([b['parc_total'] for b in self.bailleurs_data])
        construction_annuelle = sum([b['logements_construction_an'] for b in self.bailleurs_data])
        demande_totale = self.demande_data['demande_totale'].sum()
        investissement_total = sum([b['investissement_annuel'] for b in self.bailleurs_data])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Parc social total",
                f"{parc_total:,} logements",
                f"+{np.random.uniform(2, 4):.1f}% vs 2023"
            )
        
        with col2:
            st.metric(
                "Construction annuelle",
                f"{construction_annuelle:,} logements/an",
                f"+{np.random.uniform(3, 6):.1f}%"
            )
        
        with col3:
            st.metric(
                "Demande en attente",
                f"{demande_totale:,} ménages",
                f"{np.random.uniform(-2, 2):.1f}%"
            )
        
        with col4:
            st.metric(
                "Investissement annuel",
                f"{investissement_total:.1f} M€",
                f"+{np.random.uniform(5, 8):.1f}%"
            )
    
    def create_bailleurs_overview(self):
        """Vue d'ensemble des bailleurs sociaux"""
        st.markdown('<h3 class="section-header">🏢 VUE D\'ENSEMBLE DES BAILLEURS SOCIAUX</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Carte Interactive", "Performance Financière", "Répartition du Parc", "Indicateurs de Gestion"])
        
        with tab1:
            # Carte interactive des bailleurs
            st.subheader("Implantation des bailleurs sociaux")
            
            m = folium.Map(location=[-21.115, 55.536], zoom_start=10)
            
            for bailleur in self.bailleurs_data:
                # Couleur selon la performance
                if bailleur['performance_gestion'] == 'Excellente':
                    color = 'green'
                elif bailleur['performance_gestion'] == 'Élevée':
                    color = 'blue'
                elif bailleur['performance_gestion'] == 'Moyenne':
                    color = 'orange'
                else:
                    color = 'red'
                
                popup_text = f"""
                <b>{bailleur['nom']}</b><br>
                Siège: {bailleur['siege']}<br>
                Parc: {bailleur['parc_total']:,} logements<br>
                Performance: {bailleur['performance_gestion']}<br>
                Construction: {bailleur['logements_construction_an']}/an<br>
                CA: {bailleur['chiffre_affaires']} M€
                """
                
                folium.Marker(
                    [bailleur['lat'], bailleur['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"{bailleur['nom']} - {bailleur['parc_total']:,} logements",
                    icon=folium.Icon(color=color, icon='home', prefix='fa')
                ).add_to(m)
            
            folium_static(m, width=1000, height=500)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Chiffre d'affaires par bailleur
                df_bailleurs = pd.DataFrame(self.bailleurs_data)
                fig = px.bar(df_bailleurs, 
                            x='nom', 
                            y='chiffre_affaires',
                            title='Chiffre d\'affaires par bailleur (M€)',
                            color='performance_gestion',
                            color_discrete_map={
                                'Excellente': '#28a745',
                                'Élevée': '#17a2b8',
                                'Moyenne': '#ffc107',
                                'Faible': '#dc3545'
                            })
                fig.update_layout(xaxis_title="Bailleur", yaxis_title="Chiffre d'affaires (M€)")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Investissement par logement
                df_bailleurs['investissement_par_logement'] = df_bailleurs['investissement_annuel'] * 1000000 / df_bailleurs['parc_total']
                fig = px.bar(df_bailleurs, 
                            x='nom', 
                            y='investissement_par_logement',
                            title='Investissement annuel par logement (€)',
                            color='performance_gestion',
                            color_discrete_map={
                                'Excellente': '#28a745',
                                'Élevée': '#17a2b8',
                                'Moyenne': '#ffc107',
                                'Faible': '#dc3545'
                            })
                fig.update_layout(xaxis_title="Bailleur", yaxis_title="Investissement par logement (€)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition du parc par bailleur
                fig = px.pie(pd.DataFrame(self.bailleurs_data), 
                            values='parc_total', 
                            names='nom',
                            title='Répartition du parc social par bailleur')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Production annuelle par bailleur
                fig = px.bar(pd.DataFrame(self.bailleurs_data), 
                            x='nom', 
                            y='logements_construction_an',
                            title='Production annuelle de logements par bailleur',
                            color='type',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(xaxis_title="Bailleur", yaxis_title="Logements construits/an")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                # Taux d'impayés
                fig = px.bar(pd.DataFrame(self.bailleurs_data), 
                            x='nom', 
                            y='taux_impayes',
                            title='Taux d\'impayés par bailleur (%)',
                            color='taux_impayes',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Taux de rotation
                fig = px.bar(pd.DataFrame(self.bailleurs_data), 
                            x='nom', 
                            y='taux_rotation',
                            title='Taux de rotation du parc (%)',
                            color='taux_rotation',
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
    
    def create_parc_analysis(self):
        """Analyse détaillée du parc social"""
        st.markdown('<h3 class="section-header">🏠 ANALYSE DU PARC SOCIAL</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Typologie des Logements", "Performance Locative", "Rénovation Énergétique"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition par type de logement
                type_agg = self.parc_data.groupby('type_logement')['nombre_logements'].sum().reset_index()
                fig = px.pie(type_agg, 
                            values='nombre_logements', 
                            names='type_logement',
                            title='Répartition du parc par type de logement')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Loyer moyen par type
                loyer_agg = self.parc_data.groupby('type_logement')['loyer_moyen'].mean().reset_index()
                fig = px.bar(loyer_agg, 
                            x='type_logement', 
                            y='loyer_moyen',
                            title='Loyer moyen par type de logement (€)',
                            color='loyer_moyen',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Taux de vacance par bailleur
                vacance_agg = self.parc_data.groupby('bailleur')['taux_vacance'].mean().reset_index()
                fig = px.bar(vacance_agg, 
                            x='bailleur', 
                            y='taux_vacance',
                            title='Taux de vacance moyen par bailleur (%)',
                            color='taux_vacance',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance locative par type
                fig = px.box(self.parc_data, 
                            x='type_logement', 
                            y='taux_vacance',
                            title='Distribution des taux de vacance par type de logement')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Taux de rénovation énergétique
                df_bailleurs = pd.DataFrame(self.bailleurs_data)
                fig = px.bar(df_bailleurs, 
                            x='nom', 
                            y='taux_renovation_energetique',
                            title='Taux de rénovation énergétique par bailleur (%)',
                            color='taux_renovation_energetique',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Relation rénovation/performance
                fig = px.scatter(df_bailleurs, 
                               x='taux_renovation_energetique', 
                               y='performance_gestion',
                               size='parc_total',
                               title='Relation rénovation énergétique et performance',
                               hover_name='nom',
                               size_max=30)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_projets_analysis(self):
        """Analyse des projets en cours"""
        st.markdown('<h3 class="section-header">🏗️ PROJETS ET INVESTISSEMENTS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Carte des Projets", "Avancement", "Financements"])
        
        with tab1:
            # Carte des projets
            st.subheader("Carte des projets de construction et rénovation")
            
            m = folium.Map(location=[-21.115, 55.536], zoom_start=10)
            
            # Coordonnées approximatives par micro-région
            microregion_coords = {
                'Nord': [-20.8789, 55.4481],
                'Sud': [-21.3393, 55.4781],
                'Ouest': [-21.0097, 55.2697],
                'Est': [-21.0339, 55.7147]
            }
            
            for microregion, coords in microregion_coords.items():
                projets_region = self.projets_data[self.projets_data['micro_region'] == microregion]
                
                for _, projet in projets_region.iterrows():
                    # Légère variation des coordonnées pour éviter superposition
                    lat = coords[0] + np.random.uniform(-0.05, 0.05)
                    lon = coords[1] + np.random.uniform(-0.05, 0.05)
                    
                    # Couleur selon l'avancement
                    if projet['avancement'] > 75:
                        color = 'green'
                    elif projet['avancement'] > 50:
                        color = 'orange'
                    elif projet['avancement'] > 25:
                        color = 'blue'
                    else:
                        color = 'red'
                    
                    popup_text = f"""
                    <b>{projet['nom_projet']}</b><br>
                    Bailleur: {projet['bailleur']}<br>
                    Logements: {projet['logements_prevus']}<br>
                    Investissement: {projet['investissement']:.1f} M€<br>
                    Avancement: {projet['avancement']:.0f}%<br>
                    Statut: {projet['statut']}
                    """
                    
                    folium.Marker(
                        [lat, lon],
                        popup=folium.Popup(popup_text, max_width=300),
                        tooltip=projet['nom_projet'],
                        icon=folium.Icon(color=color, icon='wrench', prefix='fa')
                    ).add_to(m)
            
            folium_static(m, width=1000, height=500)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Avancement des projets par bailleur
                fig = px.box(self.projets_data, 
                            x='bailleur', 
                            y='avancement',
                            title='Avancement des projets par bailleur',
                            color='bailleur')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Répartition des types de projets
                type_agg = self.projets_data.groupby('type_projet').agg({
                    'logements_prevus': 'sum',
                    'investissement': 'sum'
                }).reset_index()
                
                fig = px.bar(type_agg, 
                            x='type_projet', 
                            y='logements_prevus',
                            title='Logements prévus par type de projet',
                            color='investissement',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Financeurs
                fig = px.pie(self.financement_data, 
                            values='montant_annuel', 
                            names='financeur',
                            title='Répartition des financements par organisme')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Types d'aides
                fig = px.bar(self.financement_data, 
                            x='financeur', 
                            y='montant_annuel',
                            color='type_aide',
                            title='Montants par financeur et type d\'aide',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_demande_analysis(self):
        """Analyse de la demande de logement social"""
        st.markdown('<h3 class="section-header">📈 ANALYSE DE LA DEMANDE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Démographie de la Demande", "Cartographie Territoriale", "Adéquation Offre-Demande"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Demande par commune
                fig = px.bar(self.demande_data, 
                            x='commune', 
                            y='demande_totale',
                            title='Demande de logement social par commune',
                            color='demande_totale',
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Temps d'attente
                fig = px.bar(self.demande_data, 
                            x='commune', 
                            y='attente_moyenne_mois',
                            title='Délai d\'attente moyen par commune (mois)',
                            color='attente_moyenne_mois',
                            color_continuous_scale='Oranges')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Taux de satisfaction
                fig = px.bar(self.demande_data, 
                            x='commune', 
                            y='taux_satisfaction',
                            title='Taux de satisfaction des demandes par commune (%)',
                            color='taux_satisfaction',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenu des demandeurs
                fig = px.scatter(self.demande_data, 
                               x='revenu_moyen_demandeur', 
                               y='taux_satisfaction',
                               size='demande_totale',
                               title='Relation revenu moyen et taux de satisfaction',
                               hover_name='commune',
                               size_max=30)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse d'adéquation
            st.subheader("Adéquation entre l'offre et la demande")
            
            # Calcul de l'adéquation (simulé)
            offre_totale = sum([b['parc_total'] for b in self.bailleurs_data])
            demande_totale = self.demande_data['demande_totale'].sum()
            taux_couverture = (offre_totale / demande_totale) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Offre totale", f"{offre_totale:,} logements")
            with col2:
                st.metric("Demande totale", f"{demande_totale:,} ménages")
            with col3:
                st.metric("Taux de couverture", f"{taux_couverture:.1f}%")
            
            # Graphique d'adéquation
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Offre', x=['Total'], y=[offre_totale], marker_color='blue'))
            fig.add_trace(go.Bar(name='Demande', x=['Total'], y=[demande_totale], marker_color='red'))
            fig.update_layout(title='Adéquation Offre/Demande de logements sociaux')
            st.plotly_chart(fig, use_container_width=True)
    
    def create_strategic_analysis(self):
        """Analyse stratégique et recommandations"""
        st.markdown('<h3 class="section-header">🎯 ANALYSE STRATÉGIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["SWOT", "Recommandations", "Indicateurs de Performance"])
        
        with tab1:
            st.subheader("Analyse SWOT du parc social réunionnais")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                #### 💪 FORCES
                - Parc important et diversifié
                - Bailleurs expérimentés
                - Soutien institutionnel fort
                - Connaissance fine du territoire
                - Compétences techniques développées
                """)
            
            with col2:
                st.markdown("""
                #### 👎 FAIBLESSES
                - Dette importante par logement
                - Parc vieillissant
                - Délais de construction longs
                - Gestion des impayés
                - Complexité administrative
                """)
            
            with col3:
                st.markdown("""
                #### 🚀 OPPORTUNITÉS
                - Fonds européens disponibles
                - Transition énergétique
                - Innovations constructives
                - Nouveaux modèles de financement
                - Croissance démographique maîtrisée
                """)
            
            with col4:
                st.markdown("""
                #### ⚠️ MENACES
                - Contraintes foncières croissantes
                - Hausse des coûts de construction
                - Évolution réglementaire
                - Pressions spéculatives
                - Changement climatique
                """)
        
        with tab2:
            st.subheader("Recommandations Stratégiques")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🏗️ Court terme (2024-2026)
                
                **Actions prioritaires:**
                - Accélérer la rénovation énergétique
                - Développer l'offre intermédiaire
                - Optimiser la gestion locative
                - Renforcer la lutte contre les impayés
                
                **Objectifs:**
                - 40% de rénovation énergétique
                - Réduction de 15% des délais
                - Taux d'impayés < 2%
                - 5 000 logements neufs/an
                """)
            
            with col2:
                st.markdown("""
                ### 🏘️ Moyen terme (2027-2030)
                
                **Actions structurantes:**
                - Massifier la construction durable
                - Développer les éco-quartiers
                - Digitaliser les services
                - Renforcer les partenariats
                
                **Cibles:**
                - 60% de rénovation énergétique
                - Parc neutre en carbone d'ici 2030
                - Satisfaction locataire > 80%
                - Dette maîtrisée
                """)
            
            st.markdown("""
            ### 🌍 Long terme (2031-2040)
            
            **Vision stratégique:**
            - Parc social 100% durable
            - Mixité sociale renforcée
            - Services innovants aux habitants
            - Modèle économique pérenne
            
            **Indicateurs cibles:**
            - Zéro artificialisation nette
            - 100% de rénovation énergétique
            - Délais d'attente < 12 mois
            - Excellence de service
            """)
        
        with tab3:
            st.subheader("Tableau de Bord Stratégique")
            
            # Indicateurs de performance
            indicateurs = [
                {'nom': 'Taux de rotation', 'valeur': 8.2, 'cible': 7.0, 'unite': '%', 'tendance': 'stable'},
                {'nom': 'Taux d\'impayés', 'valeur': 2.1, 'cible': 1.5, 'unite': '%', 'tendance': 'baisse'},
                {'nom': 'Satisfaction locataires', 'valeur': 72, 'cible': 80, 'unite': '%', 'tendance': 'hausse'},
                {'nom': 'Délai de construction', 'valeur': 28, 'cible': 24, 'unite': 'mois', 'tendance': 'stable'},
                {'nom': 'Coût de construction', 'valeur': 2150, 'cible': 2000, 'unite': '€/m²', 'tendance': 'hausse'},
                {'nom': 'Taux vacance', 'valeur': 4.2, 'cible': 3.0, 'unite': '%', 'tendance': 'baisse'},
            ]
            
            for indicateur in indicateurs:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{indicateur['nom']}**")
                with col2:
                    st.write(f"{indicateur['valeur']} {indicateur['unite']}")
                with col3:
                    st.write(f"Cible: {indicateur['cible']} {indicateur['unite']}")
                with col4:
                    if indicateur['tendance'] == 'hausse':
                        st.write("📈")
                    elif indicateur['tendance'] == 'baisse':
                        st.write("📉")
                    else:
                        st.write("➡️")
                
                # Barre de progression
                progression = (indicateur['valeur'] / indicateur['cible']) * 100
                st.progress(min(progression / 100, 1.0))
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres temporels
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime.now() - timedelta(days=365*3))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Filtres bailleurs
        st.sidebar.markdown("### 🏢 Sélection des bailleurs")
        bailleurs_selectionnes = st.sidebar.multiselect(
            "Bailleurs à afficher:",
            [b['nom'] for b in self.bailleurs_data],
            default=[b['nom'] for b in self.bailleurs_data][:3]
        )
        
        # Types de logement
        st.sidebar.markdown("### 🏠 Types de logement")
        types_logement = st.sidebar.multiselect(
            "Types de logement:",
            ['PLAI', 'PLUS', 'PLS', 'Intermediaire', 'Accession', 'Etudiant', 'Senior'],
            default=['PLAI', 'PLUS', 'PLS']
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        show_details = st.sidebar.checkbox("Afficher détails techniques", value=True)
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=False)
        
        if st.sidebar.button("🔄 Rafraîchir les données"):
            st.rerun()
        
        # Indicateurs marché
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 INDICES RÉGIONAUX")
        
        indices = {
            'Prix immobilier moyen': {'valeur': '3 250 €/m²', 'variation': 4.2},
            'Loyer moyen secteur libre': {'valeur': '12,5 €/m²', 'variation': 2.8},
            'Taux de pauvreté': {'valeur': '38%', 'variation': -0.5},
            'Croissance démographique': {'valeur': '1,2%', 'variation': 0.1}
        }
        
        for indice, data in indices.items():
            st.sidebar.metric(
                indice,
                f"{data['valeur']}",
                f"{data['variation']:+.1f}%"
            )
        
        return {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'bailleurs_selectionnes': bailleurs_selectionnes,
            'types_logement': types_logement,
            'show_details': show_details,
            'auto_refresh': auto_refresh
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📈 Vue d'ensemble", 
            "🏢 Bailleurs", 
            "🏠 Parc Social", 
            "🏗️ Projets",
            "📈 Demande", 
            "🎯 Stratégie",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_bailleurs_overview()
        
        with tab2:
            self.create_bailleurs_analysis()
        
        with tab3:
            self.create_parc_analysis()
        
        with tab4:
            self.create_projets_analysis()
        
        with tab5:
            self.create_demande_analysis()
        
        with tab6:
            self.create_strategic_analysis()
        
        with tab7:
            st.markdown("## 📋 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse stratégique complète du parc social à La Réunion.
            
            **Sources des données:**
            - Observatoire des Bailleurs Sociaux de La Réunion
            - INSEE - Recensement et statistiques
            - DREAL Réunion
            - Conseil Départemental
            - Rapports annuels des bailleurs
            
            **Période couverte:**
            - Données historiques: 2015-2024
            - Données courantes: 2024
            - Projections: 2025-2040
            
            **Méthodologie:**
            - Agrégation des données bailleurs
            - Analyse comparative de performance
            - Modélisation prospective
            - Benchmark territorial
            
            **⚠️ Avertissement:** 
            Les données présentées sont des agrégats et peuvent contenir des estimations.
            Ce dashboard est un outil d'aide à la décision.
            
            **🔒 Confidentialité:** 
            Toutes les données sensibles sont anonymisées.
            """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Contact:**
            - Observatoire du Logement Social de La Réunion
            - Site web: www.logement-social-reunion.gouv.fr
            - Email: observatoire.logement@reunion.gouv.fr
            """)

    def create_bailleurs_analysis(self):
        """Analyse détaillée par bailleur"""
        st.markdown('<h3 class="section-header">🏢 ANALYSE PAR BAILLEUR</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Comparaison Bailleurs", "Performance Détail", "Fiche Bailleur"])
        
        with tab1:
            # Filtres pour les bailleurs
            col1, col2, col3 = st.columns(3)
            with col1:
                type_filtre = st.selectbox("Type de structure:", 
                                         ['Tous', 'Groupe', 'SEM', 'HLM', 'Promoteur', 'Association'])
            with col2:
                performance_filtre = st.selectbox("Performance:", 
                                                ['Tous', 'Excellente', 'Élevée', 'Moyenne', 'Faible'])
            with col3:
                tri_filtre = st.selectbox("Trier par:", 
                                        ['Parc total', 'CA', 'Investissement', 'Performance'])
            
            # Application des filtres
            bailleurs_filtres = pd.DataFrame(self.bailleurs_data)
            if type_filtre != 'Tous':
                bailleurs_filtres = bailleurs_filtres[bailleurs_filtres['type'] == type_filtre]
            if performance_filtre != 'Tous':
                bailleurs_filtres = bailleurs_filtres[bailleurs_filtres['performance_gestion'] == performance_filtre]
            
            # Tri
            if tri_filtre == 'Parc total':
                bailleurs_filtres = bailleurs_filtres.sort_values('parc_total', ascending=False)
            elif tri_filtre == 'CA':
                bailleurs_filtres = bailleurs_filtres.sort_values('chiffre_affaires', ascending=False)
            elif tri_filtre == 'Investissement':
                bailleurs_filtres = bailleurs_filtres.sort_values('investissement_annuel', ascending=False)
            elif tri_filtre == 'Performance':
                order = {'Excellente': 4, 'Élevée': 3, 'Moyenne': 2, 'Faible': 1}
                bailleurs_filtres['performance_order'] = bailleurs_filtres['performance_gestion'].map(order)
                bailleurs_filtres = bailleurs_filtres.sort_values('performance_order', ascending=False)
            
            # Affichage des bailleurs
            for _, bailleur in bailleurs_filtres.iterrows():
                if bailleur['performance_gestion'] == 'Excellente':
                    css_class = "performance-excellent"
                elif bailleur['performance_gestion'] == 'Élevée':
                    css_class = "performance-high"
                elif bailleur['performance_gestion'] == 'Moyenne':
                    css_class = "performance-medium"
                else:
                    css_class = "performance-low"
                
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    st.markdown(f"**{bailleur['nom']}**")
                    st.markdown(f"*{bailleur['description']}*")
                    st.markdown(f"Siège: {bailleur['siege']} • Création: {bailleur['annee_creation']}")
                with col2:
                    st.markdown(f"**{bailleur['parc_total']:,}** logements")
                    st.markdown(f"Construction: {bailleur['logements_construction_an']}/an")
                with col3:
                    st.markdown(f"**{bailleur['chiffre_affaires']} M€**")
                    st.markdown(f"Investissement: {bailleur['investissement_annuel']} M€")
                with col4:
                    st.markdown(f"**{bailleur['performance_gestion']}**")
                    st.markdown(f"Impayés: {bailleur['taux_impayes']}%")
                with col5:
                    st.markdown(f"<div class='{css_class}'>Performance: {bailleur['performance_gestion']}</div>", 
                               unsafe_allow_html=True)
                    st.markdown(f"Rotation: {bailleur['taux_rotation']}%")
                
                st.markdown("---")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Top des bailleurs par parc
                top_parc = pd.DataFrame(self.bailleurs_data).nlargest(10, 'parc_total')
                fig = px.bar(top_parc, 
                            x='parc_total', 
                            y='nom',
                            orientation='h',
                            title='Top 10 des bailleurs par taille de parc',
                            color='parc_total',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top des bailleurs par investissement
                top_invest = pd.DataFrame(self.bailleurs_data).nlargest(10, 'investissement_annuel')
                fig = px.bar(top_invest, 
                            x='investissement_annuel', 
                            y='nom',
                            orientation='h',
                            title='Top 10 des bailleurs par investissement annuel (M€)',
                            color='investissement_annuel',
                            color_continuous_scale='Oranges')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Détails pour un bailleur sélectionné
            bailleur_selectionne = st.selectbox("Sélectionnez un bailleur:", 
                                              [b['nom'] for b in self.bailleurs_data])
            
            if bailleur_selectionne:
                bailleur_data = next(b for b in self.bailleurs_data if b['nom'] == bailleur_selectionne)
                historique_bailleur = self.historical_data[self.historical_data['bailleur'] == bailleur_selectionne]
                parc_bailleur = self.parc_data[self.parc_data['bailleur'] == bailleur_selectionne]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"Fiche bailleur: {bailleur_selectionne}")
                    
                    st.metric("Type de structure", bailleur_data['type'])
                    st.metric("Statut", bailleur_data['statut'])
                    st.metric("Année de création", bailleur_data['annee_creation'])
                    st.metric("Siège social", bailleur_data['siege'])
                    st.metric("Parc total", f"{bailleur_data['parc_total']:,} logements")
                    st.metric("Logements construits/an", bailleur_data['logements_construction_an'])
                    st.metric("Chiffre d'affaires", f"{bailleur_data['chiffre_affaires']} M€")
                    st.metric("Effectifs", bailleur_data['effectifs'])
                    st.metric("Taux de rotation", f"{bailleur_data['taux_rotation']}%")
                    st.metric("Taux d'impayés", f"{bailleur_data['taux_impayes']}%")
                    st.metric("Dette par logement", f"{bailleur_data['dette_par_logement']:,.0f} €")
                    st.metric("Investissement annuel", f"{bailleur_data['investissement_annuel']} M€")
                    st.metric("Performance gestion", bailleur_data['performance_gestion'])
                    st.metric("Quartiers prioritaires", bailleur_data['quartiers_prioritaires'])
                    st.metric("Taux rénovation énergétique", f"{bailleur_data['taux_renovation_energetique']}%")
                
                with col2:
                    # Graphique d'évolution du parc
                    fig = px.line(historique_bailleur, 
                                 x='date', 
                                 y='parc_total',
                                 title=f'Évolution du parc - {bailleur_selectionne}',
                                 color_discrete_sequence=['#0288D1'])
                    fig.update_layout(yaxis_title="Nombre de logements")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Graphique d'évolution des investissements
                    fig = px.line(historique_bailleur, 
                                 x='date', 
                                 y='investissement',
                                 title=f'Évolution des investissements - {bailleur_selectionne}',
                                 color_discrete_sequence=['#FF9800'])
                    fig.update_layout(yaxis_title="Investissement (M€)")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Répartition des types de logement
                    fig = px.pie(parc_bailleur, 
                                values='nombre_logements', 
                                names='type_logement',
                                title=f'Répartition du parc par type de logement')
                    st.plotly_chart(fig, use_container_width=True)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = BailleursSociauxDashboard()
    dashboard.run_dashboard()