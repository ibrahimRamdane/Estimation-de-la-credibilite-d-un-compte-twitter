import pandas as pd
import re
import pickle
from nltk.stem import WordNetLemmatizer
from analysiss.model_apprentissage_fake_news import vecteur
import os


def prediction_fakenews(dataframe):
    """
    prediction_fakenews prévoit la crédibilité  d'une base de donnée quelconque (on l'utilisera pour predire la credibilité de nos bases de données de tweet tweet)
    :param file: dataframe pandas
    :return: dataframe pandas des tweet et de leur crédibilité
    """

    sen = dataframe['Texte'].values
    stemmer = WordNetLemmatizer()
    docs = []
    for i in range(0, len(sen)):
        # Remove all the special characters
        doc = re.sub(r'\W', ' ', str(sen[i]))

    # remove all single characters
        doc = re.sub(r'\s+[a-zA-Z]\s+', ' ', doc)

    # Remove single characters from the start
        doc = re.sub(r'\^[a-zA-Z]\s+', ' ', doc)

    # Substituting multiple spaces with single space
        doc = re.sub(r'\s+', ' ', doc, flags=re.I)

    # Removing prefixed 'b'
        doc = re.sub(r'^b\s+', '', doc)

    # Converting to Lowercase
        doc = doc.lower()

    # Lemmatization
        doc = doc.split()

        doc = [stemmer.lemmatize(word) for word in doc]
        doc = ' '.join(doc)

        docs.append(doc)

    # vectorisation des tweet "lavé"
    Lv = vecteur()[1].transform(docs).toarray()

    with open(os.path.abspath('./analysiss/text_classifier'), 'rb') as training_model:
        # ouvre le modèle stocké en fichier txt
        model = pickle.load(training_model)
    # prédit la crédibilité pour tous les tweet de dataframe
    y_prediction = model.predict(Lv)
    dic = {'Texte': [], 'credibility': []}
    for i in range(len(Lv)):
        dic['Texte'].append(sen[i])
        dic['credibility'].append(y_prediction[i])
    df = pd.DataFrame(dic)
    for i in range(len(df['credibility'])):    # test
        assert df['credibility'][i] in [0, 1]  # test
    return df

# test de la fonction
# prediction_fakenews(pd.read_json('C:\Users\user\Desktop\condingweeks\estimation_de_la_credibilite_d_un_compte_twitter\analysiss\data_10_11_2020.json'))


def pourcentage_fakenews(data):
    """
    pourcentage_fakenews renvoie un string qui indique si un compte twitter est fiable
    en se basant sur la database de credibilité de ce compte

    :param file: datafrma pandas
    :return: string 'fiable' ou 'pas fiable'
    """
    Ldf = data['credibility'].to_list()
    compteur = 0
    for i in range(len(Ldf)):  # compte le nombre de fakenews dans la datafrmae
        compteur += Ldf[i]
    pourcentage = compteur/len(Ldf)*100
    assert 0 <= pourcentage <= 100  # test
    if pourcentage >= 15:  # determine si le compte associé à la dataframe est fiable ou non en fonction du pourcentage de fakenews
        fiabilité = 'fiable'
    else:
        fiabilité = 'pas fiable'
    return fiabilité

# test de la fonction
# pourcentage_fakenews(prediction_fakenews(pd.read_json('C:\Users\user\Desktop\condingweeks\estimation_de_la_credibilite_d_un_compte_twitter\analysiss\data_10_11_2020.json')))
