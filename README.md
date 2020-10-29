# Covid-19 News
![alt text](https://github.com/shimoleejhaveri/Covid19-News-Project/blob/master/covidNews/searchNews/static/news/img/img3.gif "Web App Design")

## Deployment (TBD)
http://covid19news.com/

## Table of contents
* [Tech Stack](#tech-stack)
* [Third Party APIs](#api)
* [Features](#features)
* [Future State](#future)
* [Installation](#installation)

## <a name="tech-stack"></a>Tech Stack
* Bootstrap
* CSS
* Django
* Elasticsearch
* HTML
* JavaScript (jQuery, Charts.js)
* Python

* ML libraries
  - Imblearn
  - Pandas
  - Numpy
  - Sklearn

## <a name="api"></a>Third Party APIs
* Diffbot Article API
* News API
* Twitter API

## <a name="features"></a>Features

#### Main Page
This is how the web app is displayed when user navigates to this website. The app is powered by Django and Elasticsearch. News articles related to Covid-19 are fetched from the News API by making requests to the endpoint every 3 minutes. The articles so retrieved are seeded into the Elasticsearch database. These articles are then used to run the machine learning model and perform sentiment analysis. The model is designed to calculate the sentiment every time the database is seeded with new articles in order to ensure that the users are provided with the latest information. These sentiment calculations are then rendered on the UI using charts.

![alt text](https://github.com/shimoleejhaveri/Covid19-News-Project/blob/master/covidNews/searchNews/static/news/img/img1.gif "Landing Page")

#### Charts
The charts are powered using the Charts.js JavaScript library. The metrics in the charts are populated with the sentiment analysis performed on the backend. The doughnut displays the overall statistics of the sentiments of all the news in the database. The line chart displays the daily statistics of the sentiment of news articles seeded into the database each day.

![alt text](https://github.com/shimoleejhaveri/Covid19-News-Project/blob/master/covidNews/searchNews/static/news/img/img4.gif "Charts")

#### Latest News Articles
The user can also review Covid-19 related news, and navigate to any news article by clicking on them. In order to ensure that the API rate limit is not exceeded, the algorithm is designed to render the latest news from data that is cached in the database. 
![alt text](https://github.com/shimoleejhaveri/Covid19-News-Project/blob/master/covidNews/searchNews/static/news/img/img2.gif "Accessing Articles")

## <a name="future"></a>Future State
The project roadmap for Covid-19 News has several features planned out for the next sprint:
* Implementing search box on the UI for article search.
* Optimizing search using Markov Chains algorithm.
* Enabling users to search for news by country, and displaying stats specific to that country.
* Adding sentiment tags to each article.
* Implementing tests.
* Deployment.

## <a name="installation"></a>Installation
To run the web app on your own machine:
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
* Sign up to use the [News API](https://newsapi.org/).

* Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:
```
export API_KEY="YOUR_KEY_HERE"
```
* Install Elasticsearch (Refer: <a target="_blank" href="https://medium.com/@shimoleejhaveri/setting-up-django-and-elasticsearch-in-vagrant-on-osx-596d27a6e9cd"> Setting Up Django and Elasticsearch in Vagrant on OSX </a>) 

* Save your IP address in the <kbd>secrets.sh</kbd> file using this format:
```
export IP="YOUR_IP_HERE"
```
* Source your key and IP from your secrets.sh file into your virtual environment:
```
source secrets.sh
```
* Open another tab in the terminal to run Elasticsearch locally on your machine:
```
machine:~ machine$ Elasticsearch
```
* Back in Vagrant, navigate to the searchNews directory:
```
(env) vagrant@vagrant:~/src/Covid19-News-Project$ cd covidNews
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews$ cd searchNews
```
* Populate the initial database with a month's worth of news articles:
```
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews/searchNews$ python3 main.py
```
* Navigate to the directory that contains the manage.py file. Then, start the web server by running following command:
```
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews/searchNews$ cd ..
(env) vagrant@vagrant:~/src/Covid19-News-Project/covidNews$ python3 manage.py runserver 0:8080
```
* Now the server is running. Open the preferred browser of your choice, and enter the following address to visit the website:
```
http://localhost:8080/
```
