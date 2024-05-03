
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
            request.session['form_data']={
                'name':user_name,
                'email':user_email
            }
            messages.error(request,'Email Already Registerd')
            return redirect('/add-user')
        if user_role=="-Select Role-":
            request.session['form_data']={
                'name':user_name,
                'email':user_email
            }
            messages.error(request,'Please Select User Role')
            return redirect('/add-user')
        elif confirm_password !=user_password:
            request.session['form_data']={
                'name':user_name,
                'email':user_email
            }
            messages.error(request,'password not matched')
            return redirect('/add-user')
        if user_role == "Admin":
            user_data=CustomUser(email=user_email,first_name=user_name,user_role=user_role,visible_password=user_password,is_superuser=True,is_staff=True)
            user_data.set_password(user_password)
            user_data.save()
            if 'form_data' in request.session:
                del request.session['form_data']
            messages.success(request,'User Created Successfully')
            return redirect('/add-user')
        else:

            user_data=CustomUser(email=user_email,first_name=user_name,user_role=user_role,visible_password=user_password)
            user_data.set_password(user_password)
            user_data.save()
            if 'form_data' in request.session:
                del request.session['form_data']
            messages.success(request,'User Created Successfully')
            return redirect('/add-user')
    roles=roleList.objects.all()
    all_users = CustomUser.objects.exclude(is_superuser=True)
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
        if brand=="--Select Brand--":
            brand=productBrand.objects.get(product_brand="None")
        else:
            brand=productBrand.objects.get(product_brand=brand)
        product_type=request.POST.get('product_type')
        if product_type=="--Select Type--":
            product_type=productType.objects.get(product_type="None")
        else:
            product_type=productType.objects.get(product_type=product_type)
        print(brand,'is brand and type',product_type)
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
        sku_check=masterProduct.objects.filter(product_sku=product_sku)
        if len(sku_check) >0:
            messages.error(request,'Product Already Exist')
            return redirect('/add-product')
        try:
            product_save=masterProduct(product_sku=product_sku,product_name=product_name,brand=brand,product_type=product_type,oem_number=oem_number,part_number=part_number,length=length,breadth=breadth,height=height,weight=weight,mrp=mrp,price=price,description=description,in_stock=in_stock,color=color,material=material)
            product_save.save()
            messages.success(request,'Product Added')
            return redirect('/master-products')
        except Exception as e:
            print(e)
            messages.error(request,'Something Went Wrong')
            return redirect('/add-product')
    
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

# --------------------------------Master Products End --------------------------

# --------------------------------Online Orders Start --------------------------
@login_required(login_url='/login')
def onlineorders_view(request):
    return render(request,'OnlineOrders/orders.html')


@csrf_exempt  # This decorator allows POST requests without CSRF token (for demo purposes only)
def handle_excel_upload(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        for index, row in df.iterrows():
            name = row['name']
            email = row['email']
            Contact.objects.create(name=name, email=email)
        return JsonResponse({'message': 'File uploaded successfully!'})
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method.'}, status=400)