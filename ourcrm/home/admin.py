from django.contrib import admin

from home.models import *

class AdminroleList(admin.ModelAdmin):
    list_display=('id','role_name')

admin.site.register(roleList,AdminroleList)
admin.site.register(CustomUser)

class AdminindiaMart(admin.ModelAdmin):
    list_display=('id','query_id','lead_name','contact','email','subject','address','product','message','enquery_time','query_type','company')

admin.site.register(indiamartLead,AdminindiaMart)
class AdminLastQuery(admin.ModelAdmin):
    list_display=('id','last_request')
admin.site.register(last_query,AdminLastQuery)

class AdminMasterProduct(admin.ModelAdmin):
    list_display=('id','product_sku','product_name','brand','product_type','oem_number','part_number','length','breadth','height','weight','mrp','price','description','in_stock','color','material','partsklik_brand')
admin.site.register(masterProduct,AdminMasterProduct)

class AdminProductBrand(admin.ModelAdmin):
    list_display=('id','product_brand')
admin.site.register(productBrand,AdminProductBrand)

class AdminProductType(admin.ModelAdmin):
    list_display=('id','product_type')
admin.site.register(productType,AdminProductType)