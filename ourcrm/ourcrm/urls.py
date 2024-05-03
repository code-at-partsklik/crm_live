from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index_view),
    path('add-user/',addUser),
    path('login/',login_view),
    path('master-products/',masterproduct_view),
    path('indiamart-leads/',indiamartleads_view),
    path('logout/',logout_view),
    path('forgot-password/',forgotpassword_view),
    path('my-profile/',profile_view),
    path('refresh-leads/',refreshleads_view),
    path('update-data/',update_data),
    path('add-product/',addproduct_view),
    path('product-detail/<sku>/',detailproduct_view),
    path('import-product/',importproduct_view),
    path('online-orders/',onlineorders_view),
    path('upload-product/',handle_excel_upload)
]
