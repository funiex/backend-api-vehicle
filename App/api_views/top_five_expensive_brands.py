import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import SALES_DATASET_ABSOLUTE_PATH
from rest_framework.decorators import api_view

@api_view(['GET'])
# Top Expensive Brands
def top_five_expensive_brands(request):
    if request.method == 'GET':
        sale = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
        # sorting by avg price () and selection first 6 records
        jsonData = sale.sort_values(by=['Avg Price'], ascending=False)[
            ['Brand', 'Avg Price', 'Autogroup']].head(5).to_json(orient='records')
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
