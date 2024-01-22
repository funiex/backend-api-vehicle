import pandas as pd
import json
import numpy as np
from django.http import HttpResponse, JsonResponse
from statsmodels.tsa.stattools import adfuller
from rest_framework.exceptions import APIException
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
# Ignoring python warnings
import warnings
warnings.filterwarnings("ignore")
# Dickey Fuller Test utility for Time series analysis (Checks whether the series is stationary or not)
def test_stationarity(timeseries):
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4],
                         index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    return dfoutput
# forecast api does not need any authorization token.
# @csrf_exempt
@api_view(['POST', 'OPTIONS'])
def forecast_sales(request, option, p=1, q=1, steps=5):
    try:
        if request.method == 'POST':
            df = pd.read_csv(request.data['file_url'])
            # Selecting first two columns from uploaded dataset
            df = df.iloc[:, 0:2]
            # inferring datetime
            df.iloc[:, 0] = pd.to_datetime(
                df.iloc[:, 0], infer_datetime_format=True, errors='coerce')
            # rename first col as datetime and second as sales
            df.columns = ['datetime', 'sales']
            # # indexing by datetime column
            indexedDataset = df.set_index('datetime')
            # # perform dickey-fuller test for indexedDataset(tell whether series is stationary or not)
            dfoutput = test_stationarity(indexedDataset['sales'])
            # stationary series conditions using testing of Hypothesis
            isStationary = dfoutput['Test Statistic'] < dfoutput[
                'Critical Value (10%)'] and dfoutput['p-value'] <= 0.1
            # # indexedDataset_logScale
            temp = indexedDataset
            temp['sales'] = np.log(temp['sales'])
            indexedDataset_logScale = temp
            # perform df test for logScale indexeddataset
            test_stationarity(indexedDataset_logScale['sales'])
            dfoutputlog = test_stationarity(indexedDataset_logScale['sales'])
            isStationary = isStationary or (
                dfoutputlog['Test Statistic'] < dfoutputlog['Critical Value (10%)'] and dfoutputlog['p-value'] <= 0.1)
            # shifting
            datasetLogDiffShifting = indexedDataset_logScale - indexedDataset_logScale.shift()
            datasetLogDiffShifting.dropna(inplace=True)
            # building arima model
            model = ARIMA(indexedDataset_logScale['sales'], order=(p, 1, q))
            results_ARIMA = model.fit()
            # p value -> partial autocorrelation, d value -> autocorrlation
            # # RSA Value
            RSA_VALUE = sum(
                results_ARIMA.fittedvalues[1:]-datasetLogDiffShifting['sales'])**2
            RSA_VALUE = round(RSA_VALUE)
            # predictions + data transformation
            # # ignoring first record
            # predicted values
            predictions = np.exp(results_ARIMA.predict())[1:]
            # actual values
            actual = np.exp(indexedDataset['sales'])[1:]
            # rounding values
            predictions = predictions.round()
            actual = actual.round()
            # # error calculation
            # root mean squared error
            rmse = np.sqrt(mean_squared_error(actual, predictions))
            rmse = round(rmse)
            # converting mean absolute error to percentage
            mape = mean_absolute_percentage_error(actual, predictions)
            mape *= 100
            mape = round(mape)
            # #sales forecast
            forecast = np.exp(results_ARIMA.forecast(steps=steps))
            forecast = forecast.round()
            # converting bool to str
            isStationaryStr = str(isStationary)
            # Combined data divided into 3 parts : Performance Improved
            # dataDict = {
            #     "RSS": RSA_VALUE,
            #     "RMSE": rmse,
            #     "MAPE": mape,
            #     "FORECAST": forecast.to_json(),
            #     "IS_STATIONARY": isStationaryStr,
            #     "ACTUAL": actual.to_json(),
            #     "PREDICTED": predictions.to_json(),
            # }
            # sending data in parts based on options received
            # Model Accuracy chart data
            if(option==1):
                dataDict = {
                    "ACTUAL": actual.to_json(),
                    "PREDICTED": predictions.to_json(),
                }
            # Model Accuracy details
            if(option==2):
                dataDict ={
                    "RSS": RSA_VALUE,
                    "RMSE": rmse,
                    "MAPE": mape,
                    "IS_STATIONARY": isStationaryStr,
                }
            # Forecast data
            if(option==3):
                dataDict = {
                    "FORECAST": forecast.to_json(),
                }

            jsonData = json.dumps(dataDict)
            return JsonResponse(jsonData, safe=False, status=status.HTTP_308_PERMANENT_REDIRECT)

        else:
            html = "<html><body>USE POST METHOD TO USE FORECAST API</body></html>"
            return HttpResponse(html)
    except:
        raise APIException("There was a problem!")
