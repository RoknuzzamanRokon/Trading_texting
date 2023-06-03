import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "QRE9A28VEFPWGNVZ"
NEWS_API_KEY = "6ad9106ad1d94782a3c680495800d8e6"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
last_day_data_list = data_list[0]
last_closing_stock_price = last_day_data_list['4. close']
print(last_closing_stock_price)

#TODO 2. - Get the day before yesterday's closing stock price
yesterday_data_list = data_list[1]
yesterday_closing_stock_price = yesterday_data_list['4. close']
print(yesterday_closing_stock_price)


#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(last_closing_stock_price) - float(yesterday_closing_stock_price))
print(difference)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = (difference / float(yesterday_closing_stock_price)) * 100
print(percentage_difference)
#
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if percentage_difference < 5:
    # TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME,
    }
    new_response = requests.get(url=NEWS_ENDPOINT,params=news_params)
    new_response_data = new_response.json()


    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

    #TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    articles = new_response_data['articles'][:3]
    three_articles = articles[:3]

    #TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formate_articles = [f"Headline:{articles['title']} \n\n Brief:{articles['description']}" for articles in three_articles]


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

    # TODO 9. - Send each article as a separate message via Twilio.
    twilio_account_sid = "AC970466a3e4666ce524b8a1287bc3249a"
    twilio_auth_token = "7c5d331e1ae26929dfe76ab512cebd9e"

    client = Client(twilio_account_sid, twilio_auth_token)

    # send message opthion.
    for arti_cles in formate_articles:
        message = client.messages.create(
            body=arti_cles,
            from_='+13203825930',
            to='01739933258'
        )

        print(message.sid)

#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

