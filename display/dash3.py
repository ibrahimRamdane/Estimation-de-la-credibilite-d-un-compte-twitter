# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from collect.scraping_V2 import get_last_tweets, get_last_tweets_by_subject
from analysiss.prediction_fakenews import prediction_fakenews, pourcentage_fakenews
from analysiss.Graphiques import fig_cred, fig_CredSent, fig_cred2
from analysiss.prediction_sentiment import prediction_sentiment
from dash.exceptions import PreventUpdate
import plotly.express as px

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app = Dash(__name__)


pie = px.pie()
pie.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


bar = px.bar()
bar.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[

    html.H1(children='Projet FAKE NEWS',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }

            ),

    html.H3(children='Application développée par Ibrahim RAMDANE, Adam BEN ATTIA, Ayoub EL KBADA, Alain LUONG', style={
        'textAlign': 'center',
        'color': colors['text']
    }
    ),





    html.Div(
        children=[
            html.Div([

                html.H4('Veuillez entrez un identifiant twitter',
                        style={

                            'color': colors['text']
                        }),

                dcc.Input(id='input-1-state', type='text', value='@'),

                html.Button('submit', id='submit-button-state'),



                dcc.Graph(id='fig', figure=pie),




            ], style={'display': 'inline-block', 'width': '49%'}),


            html.Div([
                html.H4('Veuillez entrez un thème twitter à analyser',
                        style={

                            'color': colors['text']
                        }),


                dcc.Input(id='input-2-state', type='text'),

                html.Button('submit', id='submit-button-state2'),

                dcc.Graph(id='fig2', figure=pie)

            ], style={'display': 'inline-block', 'width': '49%'})
        ]),

    html.Div(id='body-div', style={
                'color': colors['text']
    }),



    html.Div([

        dcc.Graph(id='fig3', figure=bar)
    ])


])


@app.callback(
    Output('fig', 'figure'),
    Output('fig3', 'figure'),
    Output(component_id='body-div', component_property='children'),

    Input('submit-button-state', 'n_clicks'),

    State('input-1-state', 'value'))
def update_output(n_clicks, input1):
    if n_clicks is None:
        raise PreventUpdate

    else:

        data_tweet_id = get_last_tweets(input1, 100)

        data_fakenews_id = prediction_fakenews(data_tweet_id)

        data_sentiment_id = prediction_sentiment(data_fakenews_id)

        figu1 = fig_cred(data_fakenews_id)

        figu1.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title="taux de fake news de l'utilisateur"
        )

        figu3 = fig_CredSent(data_sentiment_id)

        figu3.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title='Influence du sentiment sur le taux de fake news'
        )

        return figu1, figu3, str(input1)+' est un compte '+str(pourcentage_fakenews(data_fakenews_id))


@app.callback(

    Output('fig2', 'figure'),

    Input('submit-button-state2', 'n_clicks'),
    State('input-2-state', 'value'))
def update_outpout(n_clicks, input2):
    if n_clicks is None:
        raise PreventUpdate

    else:
        data_tweet_subject = get_last_tweets_by_subject(
            input2, 300, result_type_='recent')
        data_fakenews_subject = prediction_fakenews(data_tweet_subject)
        data_sentiment_subject = prediction_sentiment(data_fakenews_subject)
        figu2 = fig_cred(data_fakenews_subject)

        figu2.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            title="taux de fake news du sujet"
        )

        return figu2


if __name__ == '__main__':
    app.run_server(debug=True)
