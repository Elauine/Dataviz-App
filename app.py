import streamlit as st

from utils import (
    charger_donnees,
    creer_graphique
)

# =====================================================
# Configuration de la page
# =====================================================

st.set_page_config(
    page_title="Créateur de graphiques",
    layout="wide"
)

st.title("📊 Mon Créateur de Graphiques (MCG)")

st.write(
    "Importez vos données, créez plusieurs graphiques personnalisés "
    "et obtenez en quelques clics des visualisations prêtes à être partagées."
)

# =====================================================
# Chargement du fichier
# =====================================================

fichier = st.file_uploader(
    "Chargez votre fichier Excel",
    type=["xlsx"]
)

# =====================================================
# Si un fichier est chargé
# =====================================================

if fichier is not None:

    df = charger_donnees(fichier)

    st.markdown("#### Aperçu des données chargées")

    st.dataframe(df.head())

    colonnes = df.columns.tolist()

    # ===============================================
    # Nombre de graphiques
    # ===============================================

    nb_graphiques = st.number_input(
        "Indiquez le nombre de graphiques que vous voulez créer",
        min_value=1,
        max_value=20,
        value=1
    )

    liste_graphiques = []

    # ===============================================
    # Création des sections
    # ===============================================

    for i in range(nb_graphiques):

        st.markdown("---")

        st.subheader(f"Graphique {i+1}")

        type_graphique = st.selectbox(
            "Type de graphique",
            [
                "",
                "Camembert",
                "Diagramme en bâtons",
                "Histogramme",
                "Diagramme linéaire"
            ],
            key=f"type_{i}"
        )

        if type_graphique == "":
            continue

        # ===========================================
        # Cas diagramme linéaire
        # ===========================================

        if type_graphique == "Diagramme linéaire":

            variable_x = st.selectbox(
                "Variable X",
                [""] + colonnes,
                key=f"x_{i}"
            )

            variable_y = st.selectbox(
                "Variable Y",
                [""] + colonnes,
                key=f"y_{i}"
            )

            titre = st.text_input(
                "Titre du graphique",
                key=f"titre_{i}"
            )

            if variable_x == "" or variable_y == "":
                continue

            fig = creer_graphique(
                df=df,
                type_graphique=type_graphique,
                titre=titre,
                variable_x=variable_x,
                variable_y=variable_y
            )

        # ===========================================
        # Tous les autres graphiques
        # ===========================================

        else:

            variable_x = st.selectbox(
                "Variable",
                [""] + colonnes,
                key=f"var_{i}"
            )

            titre = st.text_input(
                "Titre du graphique",
                key=f"titre_{i}"
            )

            if variable_x == "":
                continue

            fig = creer_graphique(
                df=df,
                type_graphique=type_graphique,
                titre=titre,
                variable_x=variable_x
            )

        # ===========================================
        # Affichage du graphique
        # ===========================================

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        liste_graphiques.append(
            (
                titre if titre else f"Graphique_{i+1}",
                fig
            )
        )
