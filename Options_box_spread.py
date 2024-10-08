#!/usr/bin/env python
# coding: utf-8


import requests



def web_scrapper(stock,date):
    headers = {
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.nasdaq.com/',
    'referer': 'https://www.nasdaq.com/',
    'accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

    data = requests.get('https://api.nasdaq.com/api/quote/'+stock+'/option-chain?assetclass=stocks&date='+date+'&money=all', headers=headers).json()
    if (data != None):
        if (data["data"] != None):
            if (data["data"]["table"] != None):
                if (data["data"]["table"]["rows"] != None):
                    table = data["data"]["table"]["rows"]
                else:
                    table = "NULL"
            else:
                table = "NULL"
        else:
            table = "NULL"
    else:
        table = "NULL"

    return table



def list_return(table):
    call_bid = call_ask = strike = put_bid = put_ask = call_Bid = call_Ask = Strike = put_Bid = put_Ask = []
    for i in table:
        call_bid.append(i["c_Bid"])
        call_ask.append(i["c_Ask"])
        put_bid.append(i["p_Bid"])
        put_ask.append(i["p_Ask"])
        strike.append(i['strike'])
    call_bid.pop(0),call_ask.pop(0),put_bid.pop(0),put_ask.pop(0),strike.pop(0)
    for i in call_bid:
        try:
            call_Bid.append(round(float(i),3))
        except ValueError:
            call_Bid.append(0.010)
    for i in call_ask:
        try:
            call_Ask.append(round(float(i),3))
        except ValueError:
            call_Ask.append(0.010)
    for i in put_bid:
        try:
            put_Bid.append(round(float(i),3))
        except ValueError:
            put_Bid.append(0.010)
    for i in put_ask:
        try:
            put_Ask.append(round(float(i),3))
        except ValueError:
            put_Ask.append(0.010)
    for i in strike:
        try:
            Strike.append(round(float(i),3))
        except ValueError:
            Strike.append(0.010)
            
    return call_Bid,call_Ask,put_Bid,put_Ask,Strike


def debit_spread_calculator(call_Bid,call_Ask,put_Bid,put_Ask,Strike):
    debit_spr_buy = []
    debit_spr_sell = []
    for i in range(0,len(Strike)-2):
        if round((call_Ask[i]-call_Bid[i+1]+put_Ask[i+1]-put_Bid[i]),3) > 2*(Strike[i+1]-Strike[i]):
            debit_spr_sell.append(Strike[i])
    for i in range(0,len(Strike)-2):
        if round((call_Ask[i]-call_Bid[i+1]+put_Ask[i+1]-put_Bid[i]),3) < 0.5*(Strike[i+1]-Strike[i]):
            debit_spr_buy.append(Strike[i])
    
    return debit_spr_buy,debit_spr_sell


while(True):
    stock = input("Enter the stock ticker (Ex. AAPL): ")
    date = input("Enter the Expiration date (Ex. 2024-09-30): ")
    table = web_scrapper(stock,date)
    if table != "NULL":
        call_Bid,call_Ask,put_Bid,put_Ask,Strike = list_return(table)
        debit_spr_buy,debit_spr_sell = debit_spread_calculator(call_Bid,call_Ask,put_Bid,put_Ask,Strike)

        print("For the Given Stock Ticker {} Debit Spread Arbitrage is Calculated and The List of opportunities:".format(stock))
        for i in debit_spr_buy:
            print(" BUY The Debit Spread of Option of Contract Strike of {0} and {1}".format(i,Strike[(Strike.index(i)+1)]))
        for i in debit_spr_sell:
            print(" SELL The Debit Spread of Option of Contract Strike of {0} and {1}".format(i,Strike[(Strike.index(i)+1)]))
    else:
        print("Try New stock")



