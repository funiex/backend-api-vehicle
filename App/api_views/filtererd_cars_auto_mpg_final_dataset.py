import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import MPG_DATASET_ABSOLUTE_PATH
from rest_framework.decorators import api_view


# API URL Format `http://127.0.0.1:8000/cars/${make}/${fuelType}/${transmission}/
# ${orderBy}/${year}/${mileageKML}/${engineCC}/${power}/${seats}/${price}/${noOfRecords/`
# responsible for providi
@api_view(['GET'])
def filtererd_cars_auto_mpg_final_dataset(request, manufacturer, fuelType, transmission, orderBy, year, mileageKML,
                                          engineCC, power, seats, price, numberOfRecords):
    if request.method == 'GET':
        autoMPG = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
        # removing records having null values
        autoMPG = autoMPG.dropna();
        # Adding AverageYearlySales Column to tell most popular car specification
        # Interquantile range calculated from sales data set to make random sales more relevant
        # iqr1 = df.quantile(0.25)
        # iqr2 = df.quantile(0.75)
        # iqr = iqr2 - iqr1
        #     => range = [iqr1,iqr]
        # adding sales column
        # iqr1 = 200000 approx and iqr = 800000
        # autoMPG['AverageYearlySales'] = np.random.randint(200000, 800000, autoMPG.shape[0])
        # using data set which has  already added random sales data for performance
        # # Removing Duplicates from CSV Data by NAME column
        # autoMPG = autoMPG.drop_duplicates(subset=['Name'], keep='first', inplace=False, ignore_index=False)
        # using data set which already added random sales data for performance
        # Manufacturer Filter
        if (manufacturer != 'All'):
            autoMPG = autoMPG[(autoMPG['Manufacturer'] == manufacturer)]
        # FuelType Filter
        if (fuelType != 'All'):
            autoMPG = autoMPG[(autoMPG['Fuel_Type'] == fuelType)]
        # Transmission Filter
        if (transmission != 'All'):
            autoMPG = autoMPG[(autoMPG['Transmission'] == transmission)]
        # OrderBy Filter
        if (orderBy == 'Mileage'):
            autoMPG = autoMPG.sort_values(by=['Mileage Km/L'], ascending=False)
        elif (orderBy == 'EngineCC'):
            autoMPG = autoMPG.sort_values(by=['Engine CC'], ascending=False)
        elif (orderBy != 'None'):
            autoMPG = autoMPG.sort_values(by=[orderBy], ascending=False)
        # Year >= filter
        if (year != 0):
            autoMPG = autoMPG[(autoMPG['Year'] >= year)]
        # MileageKML >= filter
        if (mileageKML != 0):
            autoMPG = autoMPG[(autoMPG['Mileage Km/L'] >= mileageKML)]
        # EngineCC >= filter
        if (engineCC != 0):
            autoMPG = autoMPG[(autoMPG['Engine CC'] >= engineCC)]
        # Power >= filter
        if (power != 0):
            autoMPG = autoMPG[(autoMPG['Power'] >= power)]
        # Seats >= filter
        if (seats != 0):
            autoMPG = autoMPG[(autoMPG['Seats'] >= seats)]
        # Price >= filter
        if (price != 0):
            autoMPG = autoMPG[(autoMPG['Price'] >= price)]
        # Price >= filter
        if (numberOfRecords != 0):
            autoMPG = autoMPG.head(numberOfRecords)
        # converting pandas dataframe to json row wise
        jsonData = autoMPG.to_json(orient='records')
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
