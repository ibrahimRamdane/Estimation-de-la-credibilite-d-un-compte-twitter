from collect.scraping_V2 import get_last_tweets, get_last_tweets_by_subject
from analysiss.prediction_fakenews import prediction_fakenews, pourcentage_fakenews
from analysiss.Graphiques import fig_cred, fig_CredSent, fig_cred2
from analysiss.prediction_sentiment import prediction_sentiment
#import matplotlib.pyplot as plt
#from PIL import Image

if __name__ == "__main__":
    name = input("@ : ")  # prend un nom en entrée
    subject = str(input("subject : "))  # prend un sujet en entrée
    # crée une dataframe à partir des 100 derniers tweet du compte pris en input
    data_tweet_id = get_last_tweets(name, 100)
    data_tweet_subject = get_last_tweets_by_subject(
        subject, 100, result_type_='recent')  # crée une dataframe à partir de 1000 tweets chosi au hasard sur un sujet donné
    # crée une dataframe qui donne la crédibilité des 100 derniers tweets de l'utilisateur en input
    data_fakenews_id = prediction_fakenews(data_tweet_id)
    # crée une dataframe qui donne la crédibilité de 1000 tweets du sujet choisi en input en input
    data_fakenews_subject = prediction_fakenews(data_tweet_subject)
    # crée une dataframe qui donne le sentiment des 100 derniers tweets de l'utilisateur en input
    data_sentiment_id = prediction_sentiment(data_fakenews_id)
    print('@' + str(name) + ' est un compte ' +
          str(pourcentage_fakenews(data_fakenews_id)))  # ecris si le compte en input est fiable
    #data_sentiment_subject = prediction_sentiment(data_fakenews_subject)
    # crée un diagramme circulaire du pourcentage de fakenews sur les 100 derniers tweet du compte en input
    fig1 = fig_cred(data_fakenews_id)
    fig1.show()
    # affiche un diagramme circulaire du pourcentage de fakenews sur les 1000 tweets du sujet choisi en input
    fig2 = fig_cred(data_fakenews_subject)
    #fig2_saving = fig_cred2(data_fakenews_subject)
    # open method used to open different extension image file
    # fig2 = Image.open(
    #   r"figure.png")
    fig2.show()
    # affiche un diagramme en barre du nombre de fakenews en fonction de la crédibilité des 100 derniers tweet du compte en input
    fig3 = fig_CredSent(data_sentiment_id)
    fig3.show()
