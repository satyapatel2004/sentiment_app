from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

#features to add (checking to make sure that the ticker is valid)


#url setup 
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#method that handles retrieving the stock from the user. 
def get_stock(): 
    global stock_symbol 
    stock_symbol = input("Enter the stock: ")
    
    type_analysis = input("How do you want to Analyze: ")
    if type_analysis == "google" :
        make_google_url(stock_symbol) 

    if type_analysis == "yahoo" :
        make_yahoo_url(stock_symbol) 


def make_google_url(stock_symbol):
    url = f"https://www.google.com/search?q={stock_symbol}&tbm=nws"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)} please try again: ")
        get_stock() 

    google_analyze(response)


def make_yahoo_url(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}" 
    #print(url)

    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)} please try again: ")
        get_stock()


    yahoo_analyze(response.content)

def yahoo_analyze(response_content): 
    soup = BeautifulSoup(response_content, 'html.parser')
    articles = soup.find_all('h3')
    news_text = [article.text for article in articles]
    text = ' '.join(news_text)
    polarity = TextBlob(text).sentiment.polarity
    print(polarity)

def google_analyze(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('div')
    headlines_text = [headline.get_text() for headline in headlines]

    headlines_joined = ' '.join(headlines_text)

    polarity = TextBlob(headlines_joined).sentiment.polarity
    print(polarity)

def main():
    get_stock()

main()







