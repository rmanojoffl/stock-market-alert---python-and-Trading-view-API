import requests
import smtplib
import html

news_api_key="1019391394c345e9b252fa6485b9b93f"
alphavantage_api_key="I2DLQ73TK6519QPT"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":alphavantage_api_key
}
response=requests.get(url=STOCK_ENDPOINT,params=stock_params)
stock_data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in stock_data.items()]
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
yesterday_closing_price=data_list[0]["4. close"]
day_before_closing_price=data_list[1]["4. close"]
difference=(float(yesterday_closing_price)-float(day_before_closing_price))
print(difference)
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 
difference_percent=(difference/float(yesterday_closing_price))*100
print(difference_percent)
up_down=0
if difference >0:
    up_down="^"
else:
    up_down="!!"

if abs(difference_percent) >0.15:
    ## STEP 2: Use https://newsapi.org/docs/endpoints/everything
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
    #HINT 1: Think about using the Python Slice Operator
    news_params={
    "apiKey":news_api_key,
    "qInTitle":COMPANY_NAME,
    }
    news_response=requests.get(url=NEWS_ENDPOINT,params=news_params)
    news_response.raise_for_status
    articles=news_response.json()["articles"]
    three_articles=html.unescape(articles[:3])
    
    

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number. 
    #HINT 1: Consider using a List Comprehension.

    formatted_articles=[f"Headline:{article['title']}{up_down}. \nBreif: {article['description' or 'content']}" for article in three_articles]
    for articless in formatted_articles:
        with smtplib.SMTP(host="smtp.gmail.com",port=587) as connection:
            articless=articless.encode("ascii","ignore")
            connection.starttls()
            connection.login(user="testingpython788@gmail.com",password="fccl bumh yxru wrnm")
            connection.sendmail(
                from_addr="testingpython788@gmail.com",
                to_addrs="manojkumarrmk007@gmail.com",
                msg=f"subject:Here is your stock news\n\n{articless}"
            )
        

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

