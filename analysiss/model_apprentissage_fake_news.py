import pandas as pd
#import numpy as np
import re
import nltk
from sklearn.datasets import load_files
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os


def dataframe(fichier):
    """
    dataframe renvoie 2 listes, la 1ère constituée des tweet issue de la base de donnée en argument
    et la deuxième contenant des 1 ou 0 en fonction de la crédibilité du tweet (issu de la base de donnée donnée en argument)

    :param file: csv file
    :return: en premier une liste de string(texte du tweet) et en second une liste de chiffre (1 ou 0 en fonction de la credibilité du tweet
    """
    data = pd.read_csv(fichier)
    x, y = data['text'].to_list(), data['target'].to_list()
    return x, y


def cleaning(x):
    """
    cleaning renvoie une liste contenant tous les tweet apres avoir été "lavé" (enlevé les stopword,...)

    :param file: liste contenant pour chaque indice un tweet
    :return: liste contenant les tweet "lavé"
    """
    documents = []
    stemmer = WordNetLemmatizer()
    for sen in range(0, len(x)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(x[sen]))

    # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Converting to Lowercase
        document = document.lower()

    # Lemmatization
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)

        documents.append(document)
    return documents


def vectorisation(documents):
    """
    vectorisation renvoie une liste qui contient la liste de tweet après vectorisation
    et renvoie egalement l'outil de vectorisation (outil qui stock la frequence de chaque mot du tweet)

    :param file: liste de chaine de character (tweet "lavé")
    :return: -liste vectorisé des chaines de charcatere (tweet "lavé")
             -outil de vectorisation (fonction qui compte la fréquence de chaque mot sous forme de tableau) 
    """

    vectorizer = CountVectorizer(
        max_df=0.7, stop_words=stopwords.words('english'))  # compte la fréquence de chaque mot en enlevant les mots qui apparaissent dans plus de 70% du tweet, pour supprimer les stopwords (seulement en anglais)
    # vectorisation de X et mise sous forme d'array
    X = vectorizer.fit_transform(documents).toarray()
    tfidfconverter = TfidfTransformer()
    # vectorisation de X en donant un poids à chaque mot en prenant compte du nombre d'apparition de chaque mot dans les autres tweets
    X = tfidfconverter.fit_transform(X).toarray()
    return X, vectorizer


def vecteur():
    a = vectorisation(cleaning(dataframe(
        os.path.abspath('./analysiss/train.csv'))[0]))
    # for i in range(len(a[0])):  # test
    #    for j in range(len(a[0][i])):  # test
    #        assert 0 <= a[0][i][j] <= 1  # test
    return a
# vecteur est un appelle de la fonction vectorisation pour notre base de donnée de tweet
# cela permet d'éviter d'avoir à écrire tout qu'il y a dans le return à chaque fois"
# et test de la fonction vectorisation trop long donc mis en commentaire


def separation_data(X, y):
    """"
    separation_data sépare la liste des tweet vectorisé et la liste de crédibilité (déja vectorisé) en une liste
    d'entrainement et de test (vectorisés) pour chacune des 2 listes d'entrées. Ces listes seront utilisés par la suite
    pour tester et entrainer notre modèle.

    :param file: - liste de chaine de charactère vectorisé (tweet vectorisé)
                 - liste d'entier (crédibilité : 0 ou 1)
    :return: -liste d'entier representant la liste d'entrainement des tweet vectorisé
             -liste d'entier representant la liste de test des tweet vectorisé
             -liste d'entier representant la liste d'entrainement de la crédibilité du tweet 
             -liste d'entier representant la liste de test de la crédibilité du tweet
    """

    # divise la data en 80% d'entrainement et 20% de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)
    # on fixe la data qui sera train et celle qui sera testé dans un état chosi au hasard mais qui sera toujours le meme (radom_state=0)
    return X_train, X_test, y_train, y_test


def data_séparé():
    X_train, X_test, y_train, y_test = separation_data(
        vecteur()[0], dataframe(os.path.abspath('./analysiss/train.csv'))[1])
    return X_train, X_test, y_train, y_test
# data_séparé est un appelle de la fonction séparation_data pour notre base de donnée de donnée
# cela permet d'éviter d'avoir à écrire tout qu'il y a dans le return à chaque fois"


def creation_model(X_train, y_train):
    """creation model entraine le modèle et l'enrengistre dans un fichier txt pour ne plus avoir à réentrainer le model
    :param file: 2 listes d'entiers représentant les 2 listes d'entrainement vectorisé (tweet et crédibilité)"""
    classifier = RandomForestClassifier(
        n_estimators=100, random_state=0)  # definition du modèle pret à etre entrainé
    # n_estimators : nombre d'arbre de décision pour entrainer le modèle pour n_estimator >100 on trouve quasiment la meme accuracy
    # entrainement du modele a partir des abses d'entrainement
    classifier.fit(X_train, y_train)
    # enrengistrement du modèle dans n fichier texte
    with open(os.path.abspath('./analysiss/text_classifier'), 'wb') as picklefile:
        pickle.dump(classifier, picklefile)


# à run jusque la, la premiere fois (modele enrengistré)


# run juste la suite le reste du temps
# -----------
def accuracyy(X_test, y_test):
    """
    accuracy print la précision du modèle apres test du modèle sur la base de donnée test
    pour gagner du temps on ouvre le modèle enrengistré sous format texte et on le réutilise
    :param file: 2 listes d'entiers représentant les 2 listes de test vectorisé (tweet et crédibilité)
    :return: renvoie la précision du modèle
    """

    with open(os.path.abspath('./analysis/text_classifier'), 'rb') as training_model:
        model = pickle.load(training_model)

    y_pred2 = model.predict(X_test)

    # indique la précision de la prédiction des 0 et des 1 séparement
    print(classification_report(y_test, y_pred2))
    print(accuracy_score(y_test, y_pred2))
    return accuracy_score(y_test, y_pred2)
# -----------


if __name__ == "__main__":
    #accuracyy(data_séparé()[1], data_séparé()[3])
    assert 0.5 <= accuracyy(data_séparé()[1], data_séparé()[
                            3]) <= 1  # test sur la précision du model
