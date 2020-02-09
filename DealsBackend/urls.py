from django.contrib import admin
from django.urls import path
from deals_api.views import DealViewSet


urlpatterns = [
    path('deals/get', DealViewSet.get_deals),
    path('deals/upload', DealViewSet.upload_csv_deals),
    path('admin/', admin.site.urls),

]
