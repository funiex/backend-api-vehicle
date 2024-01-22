import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import MPG_DATASET_ABSOLUTE_PATH
from rest_framework.decorators import api_view

@api_view(['GET'])
# Relation between Price and Mileage
def relation_between_price_and_mileage(request, option):
    if request.method == 'GET':
        autoMPG = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
        # sending only 200 data points to prevent data cluttering
        if option == 1:
            # selecting price and mileage columns of automatic transmission cars only
            jsonData = autoMPG[autoMPG['Transmission'] == 'Automatic'][[
                'Price', 'Mileage Km/L']].head(200).to_json(orient='columns')
        elif option == 2:
            # selecting price and mileage columns of manual transmission cars only
            jsonData = autoMPG[autoMPG['Transmission'] == 'Manual'][[
                'Price', 'Mileage Km/L']].head(200).to_json(orient='columns')
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
