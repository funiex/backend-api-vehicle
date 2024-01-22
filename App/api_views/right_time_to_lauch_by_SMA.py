import pandas as pd
import json
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH
from rest_framework.decorators import api_view

@api_view(['GET'])
# Right Time to Launch Car Analysis by SIMPLE MOVING AVERAGE
def right_time_to_launch_by_SMA(request, option):
    if request.method == 'GET':
        df = pd.read_csv(CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH)
        df.rename(columns={'Unnamed: 0': 'Brand', 'Unnamed: 1': 'Segment',
                           }, inplace=True)
        df = df.drop(labels=[0], axis=0, index=None, columns=None,
                     level=None, inplace=False, errors='raise')
        # calculating average sales of 2019 and 2020 (if data of more years provided, also include them.)
        df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric)
        df['Jan'] = df['2019'] * .5 + df['2020'] * .5
        df['Feb'] = df['2019.1'] * .5 + df['2020.1'] * .5
        df['Mar'] = df['2019.2'] * .5 + df['2020.2'] * .5
        df['Apr'] = df['2019.3'] * .5 + df['2020.3'] * .5
        df['May'] = df['2019.4'] * .5 + df['2020.4'] * .5
        df['Jun'] = df['2019.5'] * .5 + df['2020.5'] * .5
        df['Jul'] = df['2019.6'] * .5 + df['2020.6'] * .5
        df['Aug'] = df['2019.7'] * .5 + df['2020.7'] * .5
        df['Sep'] = df['2019.8'] * .5 + df['2020.8'] * .5
        df['Oct'] = df['2019.8']
        df['Nov'] = df['2019.8']
        df['Dec'] = df['2019.8']
        # ensuring data is in int format
        convert_dict = {'Jan': int,
                        'Feb': int,
                        'Mar': int,
                        'Apr': int,
                        'May': int,
                        'Jun': int,
                        'Jul': int,
                        'Aug': int,
                        'Sep': int,
                        }

        df = df.astype(convert_dict)
        # taking month wise sum
        jan = df.groupby(by=['Segment'])['Jan'].sum()
        feb = df.groupby(by=['Segment'])['Feb'].sum()
        mar = df.groupby(by=['Segment'])['Mar'].sum()
        apr = df.groupby(by=['Segment'])['Apr'].sum()
        may = df.groupby(by=['Segment'])['May'].sum()
        jun = df.groupby(by=['Segment'])['Jun'].sum()
        jul = df.groupby(by=['Segment'])['Jul'].sum()
        aug = df.groupby(by=['Segment'])['Aug'].sum()
        sep = df.groupby(by=['Segment'])['Sep'].sum()
        oct = df.groupby(by=['Segment'])['Oct'].sum()
        nov = df.groupby(by=['Segment'])['Nov'].sum()
        dec = df.groupby(by=['Segment'])['Dec'].sum()
        frames = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        result = pd.concat(frames, axis=1)
        result = result.T
        # calculating moving average
        result['EconomySMA'] = result['Economy'].rolling(2).mean()
        result['LuxurySMA'] = result['Luxury'].rolling(2).mean()
        result['MidRangeSMA'] = result['Mid-Range'].rolling(2).mean()
        result['UltraLuxurySMA'] = result['Ultra Luxury'].rolling(2).mean()
        # calculing diff from MA of data values
        result['EconomyDiff'] = result['Economy']-result['EconomySMA']
        result['LuxuryDiff'] = result['Luxury']-result['LuxurySMA']
        result['MidRangeDiff'] = result['Mid-Range']-result['MidRangeSMA']
        result['UltraLuxuryDiff'] = result['Ultra Luxury'] - \
            result['UltraLuxurySMA']
        # predicting months
        bestUltraLuxury = result.loc[result['UltraLuxurySMA'] < result['Ultra Luxury']].sort_values(
            by='UltraLuxuryDiff', ascending=False).head(3).iloc[0:3, 0:0]
        bestMidRange = result.loc[result['MidRangeSMA'] < result['Mid-Range']].sort_values(by='MidRangeDiff',
                                                                                           ascending=False).head(
            3).iloc[0:3, 0:0]
        bestEconomy = result.loc[result['EconomySMA'] < result['Economy']].sort_values(by='EconomyDiff',
                                                                                       ascending=False).head(3).iloc[
            0:3, 0:0]
        bestLuxury = result.loc[result['LuxurySMA'] < result['Luxury']].sort_values(by='LuxuryDiff',
                                                                                    ascending=False).head(3).iloc[0:3,
                                                                                                                         0:0]
        framesBestMonths = [bestEconomy, bestLuxury,
                            bestMidRange, bestUltraLuxury]
        # concating prediction data
        bestMonths = pd.concat(framesBestMonths, axis=0)
        # converting data frame to python list
        bestMonthsList = list(bestMonths.index.values)
        result = result.T
        result = result.round(0)
        if(option == 1):
            # sending chart data
            jsonData = result.to_json(orient='records')
        elif(option == 2):
            # sending predictions
            jsonData = json.dumps(bestMonthsList)
        else:
            return  HttpResponse("<h1>Wrong URL</h1>")

        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
