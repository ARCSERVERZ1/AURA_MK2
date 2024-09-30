from django.shortcuts import render

# Create your views here.
import yfinance as yf
from datetime import datetime, timedelta
from STOREC.models import *
from django.http import JsonResponse


def one_percent_analyser(requests):

    stockList = stock_list.objects.filter(state = True)
    print(stockList)
    decimal_points = 4
    analysed_stock_data = {}
    for stock in stockList:
        try:
            print(stock.stock_ticker)

            analysis_dates = 7
            end_date = datetime.now().date()
            delta = timedelta(days=analysis_dates)
            start_date = end_date - delta

            print(f'start time {start_date} and endtime {end_date} for stock {stock.stock_name}')
            df = yf.download(stock.stock_ticker, start=start_date, end=end_date)

            df['max_diff'] = df['High'] - df['Low']
            df['max_diff'] = df['High'] - df['Low']
            avg_stock_price = df['Open'].mean()
            df['max_diff_percent'] = (df['max_diff'] / avg_stock_price) * 100
            #
            analysed_stock_data[stock.stock_name] = {
                str(analysis_dates)+str("_Days_AHL") : [round(df['max_diff_percent'].mean() , decimal_points) , round(df['max_diff_percent'].max(),decimal_points) , round(df['max_diff_percent'].min(),decimal_points) ],
                "buy_call": [round(df['Low'].mean()),round(df['Low'].mean()+(df['max_diff'].mean() * 0.2 ),decimal_points  )],
                "sell_call":[ round(df['High'].mean()) , round(df['High'].mean()-(df['max_diff'].mean() * 0.2 ) ,decimal_points )]
            }
        except:
            pass
    context = {
        'analysed_stock_data':analysed_stock_data
    }
    return render(requests, 'storec_dashboard.html', context)

def file_uploader(request):
    print("file_uoloader")
    for file in request.FILES.getlist('file'):
        with open('xy.xlxs', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    return one_percent_analyser(request)





    # return JsonResponse(analysed_stock_data , safe = False)
