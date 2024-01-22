import pandas as pd
from django.http import HttpResponse, JsonResponse

from ..datasets.datasets import TOP_COUNTRIES_DATA_ABSOLUTE_DATA
from rest_framework.decorators import api_view


@api_view(['GET'])
def top_five_countries_by_production_sales_exports(request, option):
    if request.method == 'GET':
        df = pd.read_csv(TOP_COUNTRIES_DATA_ABSOLUTE_DATA)
        if(option <= 2 and option >= 0):
            # selecting top 5 requested records
            # selecting desired columns (production/sales/exports)
            df = df.iloc[:5, [0, option + 1]]
            # sorting by (production/sales/exports) values
            df = df.sort_values(by=df.columns[1], ascending=False)
            jsonData = df.to_json(orient='columns')
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
