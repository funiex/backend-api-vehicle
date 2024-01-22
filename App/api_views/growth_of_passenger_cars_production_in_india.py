import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import PRODUCTION_OF_VEHICLES_DATA_ABSOLUTE_PATH
from rest_framework.decorators import api_view

@api_view(['GET'])
def growth_of_passenger_cars_production_in_india(request):
    if request.method == 'GET':
        df = pd.read_csv(PRODUCTION_OF_VEHICLES_DATA_ABSOLUTE_PATH)
        # extracting only passenger cars production data
        df = df.loc[df['Indicators'] ==
                    'Production of Passenger Cars (PV)'].sort_values('Year')
        # calculating percentage change in production from previous year
        pct_change_df = df['Value'].pct_change() * 100
        df = pd.concat([df, pct_change_df], axis=1)
        df.columns.values[3] = "Percent Change"
        df = df.round(1)
        df.drop("Indicators", axis=1, inplace=True)
        df.dropna(inplace=True)
        jsonData = df.to_json(orient="records")
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
