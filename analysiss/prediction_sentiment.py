from textblob import TextBlob
import pandas as pd


def prediction_sentiment(data):
    """
    prediction_sentiment prévoit le sentiment d'une base de donnée quelconque (on l'utilisera pour predire le sentiment des tweets de la dataframe des tweet avec les fakenews predis (prediction_fakenews))
    :param file: dataframe pandas
    :return: dataframe pandas aucquel on ajoute la colonne sentiment (contenant des 1 ou 0)
    """
    L = []
    datas = data.copy()
    x = datas['Texte'].to_list()
    for i in range(len(x)):
        v = TextBlob(x[i])
        y = v.sentiment.polarity  # estime le sentiment de chaque tweet
        L.append(y)
    datas['sentiment'] = L
    for i in range(len(datas['sentiment'])):  # test
        assert -1 <= datas['sentiment'][i] <= 1  # test
    return datas


# prediction_sentiment(pd.read_json('data_10_11_2020.json'))
# test de la fonction
