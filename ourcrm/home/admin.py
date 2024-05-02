from django.contrib import admin

from home.models import *

class AdminroleList(admin.ModelAdmin):
    list_display=('id','role_name')

admin.site.register(roleList,AdminroleList)
admin.site.register(CustomUser)

class AdminindiaMart(admin.ModelAdmin):
    list_display=('id','query_id','lead_name','contact','email','subject','address','product','message','enquery_time','query_type')

admin.site.register(indiamartLead,AdminindiaMart)
class AdminLastQuery(admin.ModelAdmin):
    list_display=('id','last_request')
admin.site.register(last_query,AdminLastQuery)