from django.urls import path
# Importing function based api views
from .api_views.forecast_sales import forecast_sales
from .api_views.relation_between_price_and_mileage import relation_between_price_and_mileage
from .api_views.top_five_expensive_brands import top_five_expensive_brands
from .api_views.filtererd_cars_auto_mpg_final_dataset import filtererd_cars_auto_mpg_final_dataset
from .api_views.sales_volume_comparison_of_top_10_brands import sales_volume_comparison_of_top_10_brands
from .api_views.top_five_best_and_worst_performers import top_five_best_and_worst_performers
from .api_views.top_five_countries_by_production_sales_exports import top_five_countries_by_production_sales_exports
from .api_views.customer_segments_by_cars_specifications import customer_segments_by_cars_specifications
from .api_views.right_time_to_lauch_by_SMA import right_time_to_launch_by_SMA
from .api_views.overview_sales_top_brands import overview_sales_top_brands
from .api_views.growth_of_passenger_cars_production_in_india import growth_of_passenger_cars_production_in_india
from .api_views.top_automakers_by_earnings_revenue_market_cap_employees import top_automakers_by_earnings_revenue_market_cap_employees
from .api_views.sales_variation_with_consumer_sentiment import sales_variation_with_consumer_sentiment

urlpatterns = [
    path('q1/<int:option>/', relation_between_price_and_mileage),
    path('q2/', top_five_expensive_brands),
   path('q3/', sales_volume_comparison_of_top_10_brands),
    path('q4/', top_five_best_and_worst_performers),
    path('q5/<int:option>', top_five_countries_by_production_sales_exports),
    path('q6/<int:option>', customer_segments_by_cars_specifications),
    path('q7/<int:option>', right_time_to_launch_by_SMA),
    path('q8/', growth_of_passenger_cars_production_in_india),
    path('q9/', sales_variation_with_consumer_sentiment),
    path('q10/<int:option>/', top_automakers_by_earnings_revenue_market_cap_employees),
    path('forecast/<int:p>/<int:q>/<int:steps>/<int:option>', forecast_sales),
    path('overview/', overview_sales_top_brands),
    path('cars/<slug:manufacturer>/<slug:fuelType>/<slug:transmission>/<slug:orderBy>/<int:year>/<int:mileageKML>/<int:engineCC>/<int:power>/<int:seats>/<int:price>/<int:numberOfRecords>/',
         filtererd_cars_auto_mpg_final_dataset),

]
