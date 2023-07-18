from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import yfinance
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import concurrent.futures


#headers for HTTP requests to "trick" websites into thinking
#that requests are not coming from a bot. 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

#makes sure that the stock is valid: 
def get_stock(stock_symbol):
    if check_ticker(stock_symbol):
        polarity = make_google_url(stock_symbol)
        return polarity 

    else:
        return "ERROR" 

# checks the ticker to see if it is valid. 
def check_ticker(stock_symbol):
    try:
        stock = yfinance.Ticker(stock_symbol)

        if stock.info:
            return True 
        
    except:
        return False


#makes the google URL. 
def make_google_url(stock_symbol):
    url = f"https://www.google.com/search?q=site%3Anews.google.com+%22{stock_symbol} stock%22"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        polarity = google_analyze(response.text)
        return polarity 
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)} please try again: "

#filtering only opinionated words 
def filter_opinionated_words(text):
    sia = SentimentIntensityAnalyzer()
    words = nltk.word_tokenize(text)
    opinionated_words = [word for word in words if sia.polarity_scores(word)['compound'] != 0]
    return opinionated_words


#formatting a yahoo URL 
def make_yahoo_url(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        get_stock()


#Yahoo_analyze takes the response content from a Yahoo HTTP response
#and conducts a sentiment analysis on it. 
def yahoo_analyze(response_content):
    soup = BeautifulSoup(response_content, 'html.parser')
    articles = soup.find_all('h3')
    news_text = [article.text for article in articles]
    text = ' '.join(news_text)
    text = " ".join(c for c in text if c.isalpha())
    polarity = TextBlob(text).sentiment.polarity
    return polarity



#google_analyze takes the text from the Google HTTP response 
# and analyzes it for the sentiment using nltk. (it is a private function)
def google_analyze(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    headlines = soup.find_all('div')
    headlines_text = [headline.get_text() for headline in headlines]
    headlines_joined = ' '.join(headlines_text)
    opinionated = filter_opinionated_words(headlines_joined)
    opinionated = set(opinionated)
    opstring = ' '.join(opinionated)
    polarity = TextBlob(opstring).sentiment.polarity


    arr = [opstring, polarity] 

    return arr

def get_average_sentiment():
    stocks = ["aapl", "msft", "goog", "amzn", "nvda", "tsla"]
    sentimentlist = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(make_google_url, stock) for stock in stocks]
        for future in concurrent.futures.as_completed(futures):
            response_text = future.result()
            polarity = google_analyze(response_text)
            sentimentlist.append(polarity)

    average = sum(sentimentlist) / len(sentimentlist)

