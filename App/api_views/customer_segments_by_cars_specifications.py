import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH, MPG_DATASET_ABSOLUTE_PATH, CARS_DATA_ABSOLUTE_PATH, SALES_DATASET_ABSOLUTE_PATH

from rest_framework.decorators import api_view


@api_view(['GET'])
def customer_segments_by_cars_specifications(request, option):
    if request.method == 'GET':
        if(option == 0):
            # get percentages of customers with cars grouped by drive train
            #  assuming no. of Models as sales data, as no sales data is available
            #  we can easily use 'sales' columns instead if sales data provided
            df = pd.read_csv(CARS_DATA_ABSOLUTE_PATH)
            df = df.groupby(['Drivetrain'])['Model'].count()
        elif(option == 1):
            # get percentages of customers with cars grouped by Transmission
            #  assuming no. of cars as sales data, as no sales data is available
            #  we can easily use 'sales' columns instead if sales data provided
            df = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
            df = df.groupby(['Transmission'])['Name'].count()
        elif(option == 2):
            # get percentages of customers with cars grouped by economy, luxury, mid range, ultra luxury
            # get percentages of cars grouped by class of vehicles
            # for this classification, we have sale data. so, using it to cal. percentages of customers
            df = pd.read_csv(CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH)
            df.rename(columns={'Unnamed: 0': 'Brand', 'Unnamed: 1': 'Segment',
                               }, inplace=True)
            df = df.drop(labels=[0], axis=0, index=None, columns=None,
                         level=None, inplace=False, errors='raise')
            df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric)
            df['Sales'] = df.iloc[:, 0:].sum(axis=1)
            df = df.groupby(by='Segment')['Sales'].sum()
        elif(option == 3):
            # get percentages of customers with cars grouped by brand
            df = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
            # for this classification, we have sale data. so, using it to cal. percentages of customers
            df['Sales'] = df.iloc[:, 3:].sum(axis=1)
            df = df.groupby(by='Brand')['Sales'].sum()
            # converting string to int type
            # selecting only top 8 brands
            df = df.astype('int32').head(8)
        elif(option == 4):
            # get percentages of customers with cars grouped by economy, luxury, mid range, ultra luxury
            #  assuming no. of cars as sales data, as no sales data is available
            #  we can easily use 'sales' columns instead if sales data provided
            df = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
            df = df.groupby(['Fuel_Type'])['Name'].count()
        elif(option == 5):
            # get percentages of customers with cars grouped by body type
            #  assuming no. of cars as sales data, as no sales data is available
            #  we can easily use 'sales' columns instead if sales data provided
            df = pd.read_csv(CARS_DATA_ABSOLUTE_PATH)
            df = df.groupby(by="Body_Type")['Unnamed: 0'].count(
            ).sort_values(ascending=False)[0:9]
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        # rounding values up to 1 decimal places
        # converting frequency to percentages
        df = (100. * df / df.sum()).round(1)
        jsonData = df.to_json(orient="columns")
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
