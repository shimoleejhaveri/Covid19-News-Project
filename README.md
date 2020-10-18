# Covid19-News-Project
# <img src="https://github.com/shimoleejhaveri/Covid19-News-Project/blob/master/covidNews/searchNews/static/news/img/img2.jpg" width="80%" alt="CovidNews">
# Sentiment Analysis of Covid-19 News

## Deployment
http://covid19news.com/

## Table of contents
* [Tech Stack](#tech-stack)
* [APIs](#api)
* [Features](#features)
* [Roadmap](#future)
* [Installation](#installation)
## <a name="tech-stack"></a>Technologies
* Python
* Django
* Elasticsearch
* ML libraries
** Pandas
** numpy
** sklearn
** imblearn
* JavaScript
* HTML
* CSS
* Bootstrap
* jQuery
## <a name="api"></a>APIs
* News API
* Diffbot Article API

## <a name="features"></a>Features

#### Covid News Statistics

#### Covid News

## <a name="future"></a>Roadmap

## <a name="installation"></a>Installation
:bulb: To run CovidNews on your own machine:
* Clone this repository: 
```
https://github.com/shimoleejhaveri/Covid19-News-Project.git
```
* Create and activate a virtual environment inside your Covid19-News-Project directory:
```
virtualenv env
source env/bin/activate
```

* Install the dependencies:
```
pip install -r requirements.txt
```

* Sign up to use the [News API](https://newsapi.org/)

* Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:
```
export API_KEY="YOUR_KEY_HERE"
```

* Install Elasticsearch (URL to shimolee article)

* Save your IP address in the <kbd>secrets.sh</kbd> file using this format:
```
export IP="YOUR_IP_HERE"
```
* Source your key and IP@ from your secrets.sh file into your virtual environment:
```
source secrets.sh
```
* Run Elasticsearch on your Machine
```
machine:~ machine$ Elasticsearch
```
* Back to vagrant: change the current working directory to searchNews:
```
(env) vagrant@vagrant:~/src/Covid19-News-Project$ cd covidNews
(env) vagrant@vagrant:~/src/Covid19-News-Project$ cd searchNews
```
* Populate initial database with a month's worth of news articles: run the file main.py
```
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews/searchNews$ python3 main.py
```
* Navigate to the directory that contains the manage.py file (the Covid19-News-Project directory). Then, start the web server by running following command:
```
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews$ python3 manage.py runserver 0:8080
```
:boom: If you are on Windows and you get UnicodeDecodeError, use this command instead: :boom:
```
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews$ python manage.py runserver 0:8000
```
* Now the server is running. Open your browser (Firefox, Chrome, Safari, Internet Explorer or whatever you use) and enter the following address to visit the website:
```
http://localhost:8080/
```
:boom: If the server runs on the prort 8000, then enter the following address 
```
http://127.0.0.1:8000/
```
:earth_americas: **Congrats your app is running** :+1:





