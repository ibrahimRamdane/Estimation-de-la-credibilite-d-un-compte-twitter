import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt


def fig_cred(tab):
    """ Cette fonction prend en argument une dataFrame qui
        recense 100 tweets d'un utilisateur et leur crédibilité 
        retourne une figure pyplot représentant la proportion de
        tweets crédible d'un utilisateur
    """
    cred = list(tab.values[:, 1])
    # nb tweet credible, nb weet pas credible
    nb_cred = [len([v for v in cred if v]), len([v for v in cred if not v])]
    names_part = ['Crédible', 'Pas crédible']

    fig = px.pie(values=nb_cred, names=names_part, color=names_part,
                 color_discrete_map={'Crédible': 'Green', 'Pas crédible': 'Red'})
    return fig


def fig_cred2(tab):
    """ Cette fonction prend en argument une dataFrame qui
        recense 100 tweets d'un utilisateur et leur crédibilité 
        retourne une figure pyplot représentant la proportion de
        tweets crédible d'un utilisateur
    """
    cred = list(tab.values[:, 1])
    # nb tweet credible, nb weet pas credible
    nb_cred = [len([v for v in cred if v]), len([v for v in cred if not v])]
    names_part = ['Crédible', 'Pas crédible']

    fig = plt.pie(nb_cred, labels=names_part, colors=[
                  'green', 'red'], autopct="%0.2f%%")
    plt.savefig("figure.png", dpi=300)
    return fig


def fig_CredSent(tab):
    """ Cette fonction prend en argument une dataFrame qui recense 
        des tweets d'un utilisateur, leur crédibilité et leur sentimentet 
        qui retourne une figure pyplot représentant la repartition des 
        tweets selon leur crédibilité et sentiment """
    cred = list(tab.values[:, 1])
    sent = list(tab.values[:, 2])
    df = pd.DataFrame({
        "Sentiment": ["Positif", "Neutre", "Négatif", "Positif", "Neutre", "Négatif"],
        "Nombre": [len([i for i in range(len(cred)) if cred[i] and sent[i] > 0.33]),
                   len([i for i in range(len(cred)) if cred[i]
                       and -0.33 < sent[i] < 0.33]),
                   len([i for i in range(len(cred)) if cred[i] and sent[i] < -0.33]),
                   len([i for i in range(len(cred))
                       if not cred[i] and sent[i] > 0.33]),
                   len([i for i in range(len(cred)) if not cred[i]
                       and -0.33 < sent[i] < 0.33]),
                   len([i for i in range(len(cred)) if not cred[i] and sent[i] < -0.33])],
        "Credibilité": ["Credible", "Credible", "Credible", "Pas Credible", "Pas Credible", "Pas Credible"]
    })
    fig = px.bar(df, x="Sentiment", y="Nombre",
                 color="Credibilité", barmode="group")
    return fig
