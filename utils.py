import pandas as pd
import plotly.express as px
from io import BytesIO
import xlsxwriter


# =====================================================
# 1. Charger les données
# =====================================================

def charger_donnees(fichier_excel):
    """
    Lit le fichier Excel chargé par l'utilisateur.

    Paramètre :fichier_excel

    Retour :DataFrame Pandas
    """

    return pd.read_excel(fichier_excel)


# =====================================================
# 2. Créer un graphique
# =====================================================

def creer_graphique(
    df,
    type_graphique,
    titre,
    variable_x,
    variable_y=None
):
    """
    Crée un graphique selon le type choisi.

    Paramètres :
        df : DataFrame
        type_graphique : type de graphique
        titre : titre du graphique
        variable_x : variable principale
        variable_y : variable secondaire
                     (uniquement pour diagramme linéaire)

    Retour : Figure Plotly
    """

    # -------------------------
    # Camembert
    # -------------------------

    if type_graphique == "Camembert":

        effectifs = (
            df[variable_x]
            .value_counts(dropna=False)
            .reset_index()
        )

        effectifs.columns = [variable_x, "Effectif"]

        fig = px.pie(
            effectifs,
            names=variable_x,
            values="Effectif",
            title=titre
        )

    # -------------------------
    # Diagramme en bâtons
    # -------------------------

    elif type_graphique == "Diagramme en bâtons":

        effectifs = (
            df[variable_x]
            .value_counts(dropna=False)
            .reset_index()
        )

        effectifs.columns = [variable_x, "Effectif"]

        fig = px.bar(
            effectifs,
            x=variable_x,
            y="Effectif",
            title=titre
        )

    # -------------------------
    # Histogramme
    # -------------------------

    elif type_graphique == "Histogramme":

        fig = px.histogram(
            df,
            x=variable_x,
            title=titre
        )

    # -------------------------
    # Diagramme linéaire
    # -------------------------

    elif type_graphique == "Diagramme linéaire":

        fig = px.line(
            df,
            x=variable_x,
            y=variable_y,
            title=titre,
            markers=True
        )

    else:

        raise ValueError(
            "Type de graphique non reconnu."
        )

    fig.update_layout(
        title_x=0.5
    )

    return fig


# =====================================================
# 3. Convertir un graphique en image
# =====================================================

def graphique_vers_image(fig):
    """
    Convertit un graphique Plotly
    en image PNG.
    """

    image = fig.to_image(
        format="png",
        width=1200,
        height=700
    )

    return BytesIO(image)


# =====================================================
# 4. Construire le fichier Excel
# =====================================================

def exporter_excel(liste_graphiques):
    """
    Paramètre :

        liste_graphiques =

        [
            ("Titre 1", fig1),
            ("Titre 2", fig2)
        ]

    Retour : Fichier Excel en mémoire.
    """

    output = BytesIO()

    workbook = xlsxwriter.Workbook(
        output,
        {"in_memory": True}
    )

    for i, (titre, fig) in enumerate(
        liste_graphiques,
        start=1
    ):

        feuille = workbook.add_worksheet(
            f"Graphique_{i}"
        )

        feuille.write(
            "A1",
            titre
        )

        image_buffer = graphique_vers_image(fig)

        feuille.insert_image(
            "A3",
            f"graphique_{i}.png",
            {
                "image_data": image_buffer
            }
        )

    workbook.close()

    output.seek(0)

    return output