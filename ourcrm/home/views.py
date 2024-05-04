
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from django.contrib import messages
from django.contrib.auth import login , logout ,authenticate
from django.core.mail import send_mail , EmailMultiAlternatives
from cryptography.fernet import Fernet
import requests
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

# partsklik brand pending to save in masterproduct

indiamart_api='https://mapi.indiamart.com/wservce/crm/crmListing/v2/?glusr_crm_key=mRyyE7lk4njHTPev5HGC7lqHq1TGmw==' 


@login_required(login_url='/login')
def index_view(request):
    return render(request,'index.html')


def login_view(request):
    if request.method=="POST":
        email=request.POST.get('user-email')
        password=request.POST.get('user-password')
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            print('user login kar diya gaya')
            messages.success(request,'Welcome to PatsKlik')
            return redirect('/')
        else:
            messages.error(request,'Wrong Crediential')
            return redirect('/login')
        
    return render(request,'Authentication/login.html')

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    messages.success(request,'Loged Out')
    return redirect('/')

@login_required(login_url='/login')
def addUser(request):

    if request.method =="POST":
        if not request.user.is_superuser:
            messages.error(request,'You r not able to do this')
            return redirect('/add-user')
        user_name=request.POST.get('user-name')
        user_role=request.POST.get('user-role')
        user_email=request.POST.get('user-email')
        user_password=request.POST.get('user-password')
        confirm_password=request.POST.get('confirm-password')
        user_check=CustomUser.objects.filter(email=user_email)
        if len(user_check) >0:
            messages.error(request,'Email Already Registerd')
            return redirect('/add-user')
        elif confirm_password !=user_password:
            messages.error(request,'password not matched')
            return redirect('/add-user')
        if user_role == "Admin":
            user_data=CustomUser(email=user_email,first_name=user_name,user_role=user_role,visible_password=user_password,is_superuser=True,is_staff=True)
            user_data.set_password(user_password)
            user_data.save()
            messages.success(request,'User Created Successfully')
            return redirect('/add-user')
        else:

            user_data=CustomUser(email=user_email,first_name=user_name,user_role=user_role,visible_password=user_password)
            user_data.set_password(user_password)
            user_data.save()
            messages.success(request,'User Created Successfully')
            return redirect('/add-user')
    roles=roleList.objects.all()
    all_users = CustomUser.objects.all()
    return render(request,'AdminPanel/adduser.html',{"roles":roles,"all_users":all_users,})


def forgotpassword_view(request):
    if request.method=="POST":
        try:
            user_email=request.POST.get('user-email')
            user_check=CustomUser.objects.filter(email=user_email)
            if len(user_check) ==0:
                messages.error(request,'Email not Registerd')
                return redirect('/forgot-password')
                
            subject,from_email,to='to reset your password','bilalahmad876923@gmail.com',user_email
            key = 'hS0YPnI9VEPgp63uPwopOvl5tages6t1PeL4iAuA4jk='
            cipher_suite = Fernet(key)
            encrypted_mail=cipher_suite.encrypt(user_email.encode())
            print(encrypted_mail,'befor encryption')
            decrypted_mail=cipher_suite.decrypt(encrypted_mail.decode())
            print(decrypted_mail,'after decryption')
            text_content="hello from crm"
            html_content=f"<h1>hi you can reset your password using this email click to reset</h1><br><h1><a href='http://127.0.0.1:8000/reset-password/{encrypted_mail}'>Click Here</a></h1>"
            messages.success(request,'Email Sent Successfully')
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('/forgot-password')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong')
            return redirect('/forgot-password')


    return render(request,'authentication/forgot.html')

@login_required(login_url='/login')
def profile_view(request):
    return render(request,'Authentication/profile.html')


# --------------------------------Leads Management Start --------------------------

@login_required(login_url='/login')
def indiamartleads_view(request):
    all_leads=indiamartLead.objects.all().order_by('-id')
    return render(request,'LeadManagement/indiamart.html',{'all_leads':all_leads})

@login_required(login_url='/login')
def refreshleads_view(request):
    current_time=datetime.datetime.strptime(str(datetime.datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
    last_res=last_query.objects.get(id=1)
    last_hit=datetime.datetime.strptime(last_res.last_request,"%Y-%m-%d %H:%M:%S.%f")
    last_diffrece= current_time -last_hit
    last_diffrece = round(last_diffrece.total_seconds() / 60)
    print(last_diffrece,'was diffrence')
    if  last_diffrece <= 7 :
        messages.error(request,f'Please try after {(7-last_diffrece)+1} minutes' )
        return redirect('/indiamart-leads')
    im_response=requests.get(indiamart_api)
    query_save=last_query.objects.get(id=1)
    query_save.last_request=str(current_time)
    query_save.save()
    if im_response.status_code==200:
        api_data=im_response.json()
        print(api_data,' was api data')
        response=api_data["RESPONSE"]
        if len(response)>0:
            try:

                for i in response:
                    address=f'{i["SENDER_ADDRESS"]} , {i["SENDER_CITY"]} , {i["SENDER_STATE"]} , {i["SENDER_PINCODE"]}'
                    msg=i["QUERY_MESSAGE"]
                    msg=msg.replace("<br>"," ")
                    data=indiamartLead(query_id=i["UNIQUE_QUERY_ID"],lead_name=i["SENDER_NAME"],contact=i["SENDER_MOBILE"],email=i["SENDER_EMAIL"],subject=i["SUBJECT"],address=address,product=i["QUERY_PRODUCT_NAME"],message=msg,enquery_time=i["QUERY_TIME"],query_type=i["QUERY_TYPE"],company=i["SENDER_COMPANY"])
                    data.save()
                messages.success(request,'Refreshed ')
                return redirect('/indiamart-leads')
            except Exception as e:
                print(e)
                messages.error(request,'Something Wrong While Saving')
                return redirect('/indiamart-leads')
        else:
            messages.error(request,'No enquiry at the moment')
            return redirect('/indiamart-leads')
    else:
        messages.error(request,'Something Went Wrong in api')
        return redirect('/indiamart-leads')

def update_data(request):
    data='2024-05-01 11:23:59'
    query=last_query.objects.get(id=1)
    query.last_request=data
    query.save()
    messages.success(request,'updated successfully')
    return redirect('/indiamart-leads')

# --------------------------------Leads Management End --------------------------



# --------------------------------Master Products Start --------------------------

@login_required(login_url='/login')
def masterproduct_view(request):
    all_products=masterProduct.objects.all()
    return render(request,'Products/masterproducts.html',{"all_products":all_products})

@login_required(login_url='/login')
def addproduct_view(request):
    if request.method=="POST":
        product_sku=request.POST.get('product_sku')
        product_name=request.POST.get('product_name')
        brand=request.POST.get('brand')
        brand=productBrand.objects.get(product_brand=brand)
        product_type=request.POST.get('product_type')
        product_type=productType.objects.get(product_type=product_type)
        oem_number=request.POST.get('oem_number')
        part_number=request.POST.get('part_number')
        length=request.POST.get('length')
        breadth=request.POST.get('breadth')
        height=request.POST.get('height')
        weight=request.POST.get('weight')
        mrp=request.POST.get('mrp')
        if mrp =='':
            mrp=0
        price=request.POST.get('price')
        if price=='':
            price=0
        description=request.POST.get('description')
        in_stock=request.POST.get('in_stock')
        if in_stock=='':
            in_stock=0
        color=request.POST.get('color')
        material=request.POST.get('material')
        partsklik_brand=request.POST.get('partsklik_brand')
        hsn_code=request.POST.get('hsn_code')
        gst_percent=request.POST.get('gst_percent')
        sku_check=masterProduct.objects.filter(product_sku=product_sku)
        if len(sku_check) >0:
            messages.error(request,'Product Already Exist')
            return redirect('/add-product')
        try:
            product_save=masterProduct(product_sku=product_sku,product_name=product_name,brand=brand,product_type=product_type,oem_number=oem_number,part_number=part_number,length=length,breadth=breadth,height=height,weight=weight,mrp=mrp,price=price,description=description,in_stock=in_stock,color=color,material=material,partsklik_brand=partsklik_brand,hsn_code=hsn_code,gst_percent=gst_percent)
            product_save.save()
            messages.success(request,'Product Added')
            return redirect('/master-products')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong')
            return redirect('/master-products')
    
    all_brands=productBrand.objects.all()
    all_type=productType.objects.all()
    return render(request,'Products/addproduct.html',{"all_brands":all_brands,"all_type":all_type})

@login_required(login_url='/login')
def detailproduct_view(request,sku):
    try:
        product=masterProduct.objects.get(product_sku=sku)
        return render(request,'Products/productdetails.html',{"product":product})
    except Exception as e:
        print(e)
        messages.error(request,'Something Went Wrong')

@login_required(login_url='/login')
def importproduct_view(request):
    return render(request,'Products/importproduct.html')


@csrf_exempt  # This decorator allows POST requests without CSRF token (for demo purposes only)
def upload_product_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:

            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                product_sku = row['sku']
                product_name = row['product_name']
                product_type = row['product_type']
                type_check=productType.objects.filter(product_type=product_type)
                if len(type_check)>0:
                    product_type=productType.objects.get(product_type=product_type)
                else:
                    product_type=productType.objects.get(product_type="None")
                product_brand=row['product_type']
                brand_check=productBrand.objects.filter(product_brand=product_brand)
                if len(brand_check) > 0:
                    product_brand=productBrand.objects.get(product_brand=product_brand)
                else:
                    product_brand=productBrand.objects.get(product_brand="None")
                 
                part_number=row['part_number']
                oem_number=row['oem_number']
                product_price=row['product_price']
                if pd.isna(product_price):
                    product_price=0
                website_price=row['website_price']
                if pd.isna(website_price):
                    website_price=0
                product_stock=row['product_stock']
                if pd.isna(product_stock):
                    product_stock=0
                length=row['length']
                breadth=row['breadth']
                height=row['height']
                weight=row['weight']
                product_color=row['product_color']
                product_material=row['product_material']
                partsklik_brand=row['partsklik_brand']
                hsn_code=row['hsn_code']
                if pd.isna(hsn_code):
                    hsn_code=''
                gst_percent=row['gst_percent']
                if pd.isnan(gst_percent):
                    gst_percent=''
                desc=''
                # print('this was data',product_sku,product_name,product_type,product_brand,part_number,oem_number,product_price,website_price)
                sku_check=masterProduct.objects.filter(product_sku=product_sku)
                if len(sku_check) > 0:
                    continue
                else:
                    product_save=masterProduct(product_sku=product_sku,product_name=product_name,brand=product_brand,product_type=product_type,oem_number=oem_number,part_number=part_number,length=length,breadth=breadth,height=height,weight=weight,mrp=product_price,price=website_price,in_stock=product_stock,color=product_color,material=product_material,partsklik_brand=partsklik_brand,hsn_code=hsn_code,gst_percent=gst_percent,description=desc)
                    product_save.save()
            return JsonResponse({'message': 'File uploaded successfully!'})
        except Exception as e:
            print(e)
            messages.error(request,'Try Again')
            return redirect('/import-product')
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method.'}, status=400)

# chenging


@login_required(login_url='/login')
def edit_product_view(request,id):
    if request.method=="POST":
        sku=request.POST.get('product_sku')
        product_to_update=masterProduct.objects.get(product_slu=sku)
        # product_to_update.
        messages.error(request,'Working on Functionality')
        return redirect('/master-prodcut')
    try:
        product=masterProduct.objects.get(id=id)
        all_brands=productBrand.objects.all()
        all_type=productType.objects.all()
        return render(request,'Products/editproduct.html',{"product":product,'all_brands':all_brands,'all_type':all_type})
    except Exception as e:
        messages.error(request,'Something Went Wrong')
        return redirect('/master-products')

# --------------------------------Master Products End --------------------------







# --------------------------------Online Orders Start --------------------------
@login_required(login_url='/login')
def onlineorders_view(request):
    return render(request,'Orders/orders.html')


@login_required(login_url='/login')
def detailorders_view(request):
    return render(request,'Orders/orderdetails.html')

@login_required(login_url='/login')
def manualorder_view(request):
    return render(request,'Orders/manualorder.html')
    




# --------------------------------Inventory Management Start --------------------------
@login_required(login_url='/login')
def inventorydash_view(request):
    products=masterProduct.objects.all()
    all_inventroy=Inventory.objects.all()
    send_data=[]
    for j in products:
        print(j)
        inv=Inventory.objects.filter(product=j)
        if len(inv)==1:
            inv=Inventory.objects.get(product=j)
            if inv.product.product_sku ==j.product_sku:
                inv1=Inventory.objects.get(product=j)
                send_data.append({
                    "product_sku":j.product_sku,
                    "product_name":j.product_name,
                    "part_number":j.part_number,
                    "ware_house":inv1.ware_house.ware_house,
                    "rack_number":inv1.rack.rack_number,
                    "quantity":inv1.quantity
                })
        else:
                send_data.append({
                "product_sku":j.product_sku,
                "product_name":j.product_name,
                "part_number":j.part_number,
                "ware_house":'-',
                "rack_number":'-',
                "quantity":'-'
            })

    return render(request,'Inventory/inven_dashboard.html',{"send_data":send_data})


@login_required(login_url='/login')
def edit_inventorydash_view(request,skk):
    if request.method=="POST":
        try:

            pr_sku=request.POST.get('pr_sku')
            pr_sku=masterProduct.objects.get(product_sku=pr_sku)
            house=request.POST.get('warehouse')
            house=WareHouses.objects.get(ware_house=house)
            rack=request.POST.get('rack')
            rack=Racks.objects.get(rack_number=rack)
            quantity=request.POST.get('quantity')
            edit_check=Inventory.objects.filter(product=pr_sku)
            if len(edit_check)>0:
                edit_save=Inventory.objects.get(product=pr_sku)
                edit_save.ware_house=house
                edit_save.product=pr_sku
                edit_save.rack=rack
                edit_save.quantity=quantity
                edit_save.save()
                messages.success(request,'Inventory Updated Successfully')
                return redirect('/inven-dashboard')
            quantity_save=Inventory(ware_house=house,product=pr_sku,rack=rack,quantity=quantity)
            quantity_save.save()
            messages.success(request,'Inventory Updated Successfully')
            return redirect('/inven-dashboard')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong')
            return redirect('/inven-dashboard')
    try:
        product=masterProduct.objects.get(product_sku=skk)
        quan=Inventory.objects.filter(product=product)
        if len(quan)>0:
            quan=quan[0]
        warehouse=WareHouses.objects.all()
        blocks=Racks.objects.all()
        return render(request,'Inventory/editinventory.html',{"product":product,"warehouse":warehouse,"blocks":blocks,"quan":quan})
    except Exception as e:
        print(e)
        messages.error(request,'Product Not Found')
        return redirect('/inven-dashboard')


@login_required(login_url='/login')
def dispatchdashboard_view(request):

    return render(request,'Inventory/DispatchArea/dispatch_inven_dashboard.html')