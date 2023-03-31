# estimation_de_la_crédibilité_d_un_compte_twitter



## Name
Fakeniouz

## Description
Fakeniouz is an application that quantifies the credibility of a Twitter user, and it tells if the Twitter user is reliable or not. It also has a comparative feature that shows if a user is lying more when tweeting positive tweet or negative tweet. It finally allows to quantify the credibility of several tweets on a given subject. All of this is represented within an organized and elegant dashboard.


## Installation

The Code is written in Python 3.10.7 . If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip. You will have to install the dependencies :

```
pip install -r packages.txt
```
You then have to create and fill a file named credentials.py in the folder "collect", your consumer keys and authentification tokens, that can be found in your Twitter Developper Portal. It should look like this :

```
CONSUMER_KEY='' 
CONSUMER_SECRET=''
ACCESS_TOKEN=''
ACCESS_SECRET=''
```
## Run the project

There are two ways to run the application. You can directly run the dash3 dashboard to interact with it more naturally with the following command written in the terminal :

```
python -m display.dash3
```

Or either it is possible to run it from the main with the following line command :

``` 
python -m display.main
```



## Authors and acknowledgment
Ayoub EL KBADI
Ibrahim RAMDANE
Mohammed Adam BENATTIA
Alain LUONG

## License
This project is licensed under Creative Commons : Attribution-NonCommercial-ShareAlike 4.0 International


