from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import yfinance
import nltk 
from nltk.probability import FreqDist


#url setup 
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#method that handles retrieving the stock from the user. 
def get_stock(): 
    global stock_symbol 
    stock_symbol = input("Enter the stock: ")

    if check_ticker(stock_symbol):
        type_analysis = input("How do you want to Analyze: ")

        if type_analysis == "google" :
            make_google_url(stock_symbol) 

        if type_analysis == "yahoo" :
            make_yahoo_url(stock_symbol) 

    else :
        print("Invalid Ticker!\n\n")
        get_stock()

    


#using the yfinance library to check if the user input ticker is valid. 
def check_ticker(stock_symbol):
    try:
        stock = yfinance.Ticker(stock_symbol)
        info = stock.info
        return True
    except:
        return False 

#makes the google URL 
def make_google_url(stock_symbol):
    url = f"https://www.google.com/search?q={stock_symbol}&tbm=nws"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)} please try again: ")
        get_stock() 

    google_analyze(response)

#makes the yahoo URL 
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

#analyzes the yahoo information. 
def yahoo_analyze(response_content): 
    soup = BeautifulSoup(response_content, 'html.parser')
    articles = soup.find_all('h3')
    news_text = [article.text for article in articles]
    text = ' '.join(news_text)
    polarity = TextBlob(text).sentiment.polarity
    print(polarity)

#analyzes the google information (headlines)
def google_analyze(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('div')
    headlines_text = [headline.get_text() for headline in headlines]

    headlines_joined = ' '.join(headlines_text)

    #converting all of the google headlines to lowercase
    headlines_joined = headlines_joined.lower() 

    #splits into a list. 
    headlines_list = headlines_joined.split()

    #calculating word frequencies:
    fdist = FreqDist(headlines_list)
    flist = fdist.most_common(400)

    jstring = ' '.join(item[0] for item in flist)
    print(jstring)

    polarity = TextBlob(jstring).sentiment.polarity
    print(polarity)






def main():
    get_stock()

main()







