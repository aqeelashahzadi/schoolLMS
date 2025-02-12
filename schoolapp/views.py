from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from  .models import coursesdb
from .models import contact_db
from django.shortcuts import render
from .models import payment_db
from .models import subjectdb
from .models import carts_db
from .models import comment_db
from django.db.models import Q
# from .models import cartitems_db 
from django.contrib.auth import get_user_model   
# Create your views here..


def index(request):
    return render(request,'schoolapp/index.html')

def courses(request):
    context = {}
    courses = coursesdb.objects.all()  # Get all courses as a queryset
    user = request.user

    # Create an empty list to store course data with button information
    course_data_with_buttons = []

    for course in courses:
        # Check if the course is present in the user's cart (carts_db)
        in_cart = carts_db.objects.filter(Q(proname=course) & Q(userss=user)).exists()

        # Create a dictionary to hold course data and button information
        if in_cart:
            course_data = {
                'course': course,
                'in_cart': in_cart,
            }
        else:
            course_data = {
                'course': course,
            }
        context['courses2'] = course_data_with_buttons
        # Append the dictionary to the list
        course_data_with_buttons.append(course_data)
        if request.method == 'POST':
            idofproduct = request.POST.get('idOfProductToSendBack', 'default')
            idofclass=request.POST.get('idOfProductToSendBack2',"default")
            if idofproduct !='default':
                context = {"context": idofproduct}
                return render(request, 'schoolapp/payment.html', context)
            if idofclass !="default":
                # context = {"context": idofclass}
                # return render(request, 'schoolapp/subjects.html', context)
                request.session['idoclass']=idofclass
                return redirect('subjectn')
           
    return render(request, 'schoolapp/courses.html', context)

@login_required(login_url='login_n')
def classes(request):
    return render(request,'schoolapp/class.html')
@login_required(login_url='login_n')
def contact(request):
    if request.method == "POST":
        firstname=(request.POST.get('FirstName','default'))
        Email=(request.POST.get('Email','default'))
        phoneno=(request.POST.get('PhoneNumber','default'))
        question=(request.POST.get('questions','default'))
        contact_db.objects.create(name=firstname,email=Email,phoneno=phoneno,question=question)
        return render(request,'schoolapp/contact.html')
    return render(request,'schoolapp/contact.html')

@login_required(login_url='login_n')
def result(request):
    return render(request,'schoolapp/results.html')

def register(request):
    context={}
    if request.method == "POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        # creating user
        # Check for duplicate usernames using filter
        userfilter = User.objects.filter(username=username)
        if userfilter.exists():
            context["error"]="Username already present"
            return render(request, 'schoolapp/register.html', context) 
        emailfilter=User.objects.filter(email=email)
        if emailfilter.exists():
            context["error2"]="Email already exists"
            return render(request, 'schoolapp/register.html', context) 
        myuser=User.objects.create_user(username,email,password)
        myuser.fname=fname
        myuser.lname=lname
        myuser.save()
        return redirect("login_n")  
    return render(request,'schoolapp/register.html')

def login_logic(request):
    if request.method == "POST":
        username_login=request.POST.get('usernamelogin')
        password_login=request.POST.get('passwordlogin')
        user = authenticate(username=username_login, password=password_login)
        context={}
        if user is not None:
            login(request,user)
            context["success"]= "Successfully logged in"
            return render(request,'schoolapp/index.html',context)
            # return redirect('homen',context)
        else:
            context["fail"]="Invalid email or password"
            return render(request,'schoolapp/login.html',context)
    return render(request,'schoolapp/login.html')

def logout_logic(request):
    logout(request)
    messages.success(request, "loged out") 
    return redirect('homen') 

def student_teacher(request):
    return render(request,'schoolapp/student-teacher.html')

def subject(request):
    idodcls=request.session.get('idoclass','default value')
    listall = subjectdb.objects.filter(classname=idodcls)
    return render(request,'schoolapp/subjects.html',{'lis': listall})

@login_required(login_url='login_n')
def teacherhome(request):
    return render(request,'schoolapp/teacherhome.html')

def teacherclasses(request):
    return render(request,'schoolapp/teachersclasses.html')
#csrf_exempt decoraters na sirf is function ko allow karay ga k 3rd party is ma changes kar sakay csrf token ki functionality ko change kar day gan thora sa
@csrf_exempt
def handlederequest(request):
    # paytm will send you post requst here
    pass

@login_required(login_url='login_n')
def payment(request):
    context={}
    if request.method == "POST":
        emailp=(request.POST.get('emailpayment','default'))
        cardnop=(request.POST.get('cardnopayment','default'))
        nameoncardp=(request.POST.get('nameoncardpayment','default'))
        secpasswordp=(request.POST.get('secpasswordpayment','default'))
        exdatep=(request.POST.get('exdatepayment','default'))
        option=(request.POST.get('selectopt','Null'))
        idfrompaymentpage=(request.POST.get('idfromcoursesandpaymentpage','default'))
        
        payment_db.objects.create(email_pay=emailp,cardnos_pay=cardnop,cardname_pay=nameoncardp,seccode_pay=secpasswordp,exdate_pay=exdatep,selected_option=option)
        # cartitems_db.objects.create()
        # print("*************************")
        # print(idfrompaymentpage)
        # product=coursesdb.objects.get(id=idfrompaymentpage)
        # user=request.user
        # cart,_=cart_db.objects.get_or_create(user=user)
        # cart_item=cartitems_db.objects.create(cart=cart,item=product)
        # cart_item.save()

        # return render(request,'schoolapp/mycourses.html')

        users=request.user
        productname=coursesdb.objects.get(id=idfrompaymentpage)
        product=coursesdb.objects.filter(id=idfrompaymentpage)
        for p in product:
            img=p.image
            name=p.name
            detail=p.detail
            carts_db.objects.create(imges=img,name=name,detail=detail,userss=users,proname=productname)
        return redirect('mycoursesn')

        
    return render(request,'schoolapp/payment.html')

@login_required(login_url='login_n')
def mycourses(request):
    # user = get_user_model().objects.get(username=request.user.username)
    # cart_items = cartitems_db.objects.filter(cart__user=user)
    # print("^^^^^^^^^^^^^^^^^^6")
    # print(cart_items)
    # context={"list": cart_items}
    print("$$@@@@@@@@@@@@@@@@@@@@srsers")
    user = request.user 
    print(user)
    # try:
    #     cart = cart_db.objects.get(user=request.user)
    #     print(cart.user.username)
    # except cart_db.DoesNotExist:
    #     print("User does not have a cart.")
    # Get the current user
    # cart = cart_db.objects.get(user=user)  # Get the user's cart
    # cart_items = cartitems_db.objects.filter(cart=cart)  # Get the cart items

    # context = {'cart_items': cart_items}
    print("&&&&&&&&&&&&&&&&&&&&&&&&*")

    # print(context['cart_items'])
    productcart=carts_db.objects.filter(userss=user)
    context = {
        'latest_productcart': productcart
    }
    return render(request,'schoolapp/mycourses.html',context)

def postcomment(request):
    user= request.user
    comment= request.POST.get("comment",'default')
    commSno=request.POST.get("commsno")
    subjectname=subjectdb.objects.get(id=commSno)
    savetodb=comment_db(comment=comment,user=user,subjectname=subjectname)
    savetodb.save()
    return redirect('/')
# filter saray ,get 1 lata ha 
    
