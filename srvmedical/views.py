from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from srvmedicals.models import User
from srvmedicals.backend import authenticate,login, logout
from django.core.mail import send_mail
from srvmedical.utility import send_otp
from srvmedicals.models import User,Product,Cart,Order,OrderItem


def homePage(request):
    products=Product.objects.all().values()
    for product in products:
        product['discounted_price'] = product['price'] - (product['price'] * product['discount']) / 100

    product_count=request.session.get('count')
    context = {
    'myproducts': products,'count':product_count
    }
    return render(request, "index.html",context)

def add_to_cart(request,product_id):
     # Retrieve the product object
    product = get_object_or_404(Product, id=product_id)
    product_count=0
    # Retrieve the list of product IDs from the session, or initialize it if it doesn't exist
    cart_products = request.session.get('cart_products', [])
    
    # Add the current product ID to the list
    cart_products.append(product_id)
    
    # Update the session with the modified list of product IDs
    request.session['cart_products'] = cart_products
    for items in cart_products:
        product_count=product_count+1

    request.session['count'] = product_count
    # Print the list of product IDs (for debugging purposes)
    print("Product IDs in cart:", request.session['cart_products'])
    
    if 'user' in request.session.keys():
        return redirect('user-index')
    else:
        # Redirect to the homepage
        return redirect('homepage')
    

def remove_from_cart(request, product_id):
    # Retrieve the product object
    product = get_object_or_404(Product, id=product_id)
    product_count=request.session.get('count')
    # Retrieve the list of product IDs from the session
    cart_products = request.session.get('cart_products', [])
    
    # Check if the product is in the cart
    if product_id in cart_products:
        # Remove the product ID from the cart list
        cart_products.remove(product_id)
        product_count=product_count-1
        # Update the session with the modified list of product IDs
        request.session['count'] = product_count
        request.session['cart_products'] = cart_products
    if 'user' in request.session.keys():
        return redirect('user-cart')
    else:
        return redirect('cart')
        # Redirect to the cart view
    

def cart(request):
    cart_products = request.session.get('cart_products', [])
    
    mrp_total=0
    shipping_charges=0
    total_discount=0
    # Use the list of product IDs to retrieve the corresponding products from the database
    cart_items = Product.objects.filter(id__in=cart_products).values()
    if cart_items :
        for product in cart_items:
            product['discounted_price'] = product['price'] - (product['price'] * product['discount']) / 100
            mrp_total=mrp_total+product['price']
            total_discount=total_discount+( product['price'] -product['discounted_price'])

        net_amount=mrp_total-total_discount
        if net_amount>500:
            shipping_charges=0
        else:
            shipping_charges=60

        product_count=request.session.get('count')
        payment_details={"mrp_total":mrp_total,"shipping_charges":shipping_charges,"total_discount":total_discount,"amount_to_pay":net_amount+shipping_charges,"count":product_count}
        context = {
        'items': cart_items,'payment_summary':payment_details,
        }
        return render(request, "cart.html",context)
    else:

        return render(request, "cart.html")


def product_search(request):
    product_count=request.session.get('count')
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        print(search_query[0])
        # Filter products based on search query
        products = Product.objects.filter(product_name__istartswith=search_query[0]).values()
       
        
        return render(request, 'products.html', {'products': products,'count':product_count})
    else:
        # Handle GET request or other cases
        return render(request, 'products.html',{'count':product_count})
    
def category_product(request,category):
    products=Product.objects.filter(category=category).values()
    print(products)
    return render(request,"category_products.html",{'products': products})
    

def createAccount(request):
    if 'email' in request.session.keys():
        if request.method=="POST":
            email=request.session['email']
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            mobile=request.POST.get('mobile')
            gender=request.POST.get('gender')
            user_otp=request.POST.get('otp')
            otp=request.session['otp']

            if user_otp==otp:
                try:
                    en=User(email=email,mobile_no=mobile,first_name=fname,last_name=lname,gender=gender)
                    en.save()
                    request.session['user']="True"
                    return redirect('user-index')
                    
                except:
                    return HttpResponse("oops! something went wrong")
            else:
                message={'message':'invalid otp you have entered'}
                return render(request,"create-account.html",message)
        return render(request, "create-account.html")
    else:
        return redirect('homepage')


def signup(request):
    product_count=request.session.get('count')
    if request.method=="POST":
        email=request.POST.get('email')
        request.session['email']=email
        print(email)
        
        try:
            user_exist= User.objects.filter(email=email).exists()
            if user_exist:
                otp=send_otp(request)
                send_mail(
                    "One-Time Password (OTP) for signin",
                    "Your one time otp for signin is: "+otp,
                    "rabsramii8010@gmail.com",
                    [email],
                    fail_silently=False,
                )
                return redirect('signin')
            else:
                otp=send_otp(request)
                send_mail(
                    "One-Time Password (OTP) for signup",
                    "Your one time otp for signup is: "+otp,
                    "rabsramii8010@gmail.com",
                    [email],
                    fail_silently=False,
                )
                return redirect('create-account')
        except:
            return HttpResponse("oops! something went wrong")
                   
    return render(request, "signup.html",{'count':product_count})


def signin(request):
    if 'email' in request.session.keys():
        if request.method=="POST":
            otp=request.session['otp']
            user_otp=request.POST.get('otp')
            if user_otp==otp:
                print("success")
                request.session['user']="True"
                return redirect('user-index')
            else:
                print("failed")
                return redirect("signup")

        return render(request, "signin.html")
    else:
        return redirect('homepage')

def userHomepage(request):
    if 'user' in request.session.keys():
        email=request.session['email']
        products=Product.objects.all().values()
        for product in products:
            product['discounted_price'] = product['price'] - (product['price'] * product['discount']) / 100

        product_count=request.session.get('count')
        
        try:
            user=User.objects.filter(email=email)
            print(user[0].first_name +" "+ user[0].last_name)
            name=user[0].first_name
            details={'name':name,'count':product_count}
            context = {
            'myproducts': products,'details':details
            }
        except:
            return HttpResponse("oops! something went wrong")
        return render(request, "user/index.html",context)
    else:
        return redirect('homepage')
   


def userCart(request):
    if 'user' in request.session.keys():
        cart_products = request.session.get('cart_products', [])
        email=request.session['email']
        product_count=request.session.get('count')
        mrp_total=0
        shipping_charges=0
        total_discount=0
        # Use the list of product IDs to retrieve the corresponding products from the database
        cart_items = Product.objects.filter(id__in=cart_products).values()
        if cart_items :
            for product in cart_items:
                product['discounted_price'] = product['price'] - (product['price'] * product['discount']) / 100
                mrp_total=mrp_total+product['price']
                total_discount=total_discount+( product['price'] -product['discounted_price'])
                # user = User.objects.get(email=email)
                # productobject = Product.objects.get(id=product['id'])
                # quantity = 1
                # en = Cart(user=user, product=productobject, quantity=quantity)
                # en.save()

            net_amount=mrp_total-total_discount
            if net_amount>500:
                shipping_charges=0
            else:
                shipping_charges=60
            
            try:
                user=User.objects.filter(email=email)
                
                name=user[0].first_name
                payment_details={
                    "mrp_total":float(mrp_total),
                    "shipping_charges":float(shipping_charges),
                    "total_discount":float(total_discount),
                    "amount_to_pay":float(net_amount+shipping_charges)
                    }
                request.session['payment_details']=payment_details
                details={'name':name,'count':product_count}
                context = {
                'items': cart_items,'payment_summary':payment_details,'details':details
                }
            except:
                return HttpResponse("oops! something went wrong")
            return render(request, "user/user-cart.html",context)
            
            # details={'name':name,'count':product_count}
            # payment_details={"mrp_total":mrp_total,"shipping_charges":shipping_charges,"total_discount":total_discount,"amount_to_pay":net_amount+shipping_charges}
            # context = {
            # 'items': cart_items,'payment_summary':payment_details,'details':details
            # }
            # return render(request, "user/user-cart.html",context)
        else:
            try:
                user=User.objects.filter(email=email)
                
                name=user[0].first_name
                print(name)
                details={'name':name,'count':product_count}
                context = {
                'details':details
                }
               
            except:
                return HttpResponse("oops! something went wrong")
            return render(request, "user/user-cart.html",context)
            
    else:
        return redirect('homepage')
    

def user_product_search(request):
    if 'user' in request.session.keys():
        product_count=request.session.get('count')
        email=request.session['email']
        if request.method == 'POST':
            search_query = request.POST.get('search', '')
            print(search_query[0])
            # Filter products based on search query
            products = Product.objects.filter(product_name__istartswith=search_query[0]).values()
            try:
                user=User.objects.filter(email=email)
                
                name=user[0].first_name
                details={'name':name,'count':product_count}
                context = {
                'products': products,'details':details
                }
            except:
                return HttpResponse("oops! something went wrong")
            return render(request, 'user/user-product.html',context)
        else:
            # Handle GET request or other cases
            try:
                user=User.objects.filter(email=email)           
                name=user[0].first_name
                details={'name':name,'count':product_count}
                context = {
                'details':details
                }
            except:
                return HttpResponse("oops! something went wrong")
            return render(request, "user/user-product.html",context)
    else:
        return redirect('homepage')

def attachPrescription(request):
    if 'user' in request.session.keys():
               
        product_count=request.session.get('count')
        email=request.session['email']
        if request.method=='POST':
            name=request.POST.get('name')
            mobile=request.POST.get('mobile')
            address=request.POST.get('address')
            city=request.POST.get('city')
            state=request.POST.get('state')
            pincode=request.POST.get('pincode')
            
            full_address=address+" "+city+" "+state+" "+pincode 
            order_summary={'name':name,'mobile':mobile,'address':full_address}
            request.session['order_summary']=order_summary
            return redirect('review-order')
        
        
        
        try:
            user=User.objects.filter(email=email)
            name=user[0].first_name
            details={'name':name,'count':product_count}
            context = {
            'details':details
            }
        except:
            return HttpResponse("oops! something went wrong")
        return render(request, "user/attach-prescription.html",context)
    else:
        return redirect('homepage')
    


def userProfile(request):
    if 'user' in request.session.keys():
        product_count=request.session.get('count')
        email=request.session['email']
        try:
            user=User.objects.filter(email=email)
            print(user[0].first_name +" "+ user[0].last_name)
            name=user[0].first_name
            details={'name':name,'count':product_count}
            context = {
            'details':details
            }
        except:
            return HttpResponse("oops! something went wrong")
        return render(request, "user/profile.html",context)
    else:
        return redirect('homepage')
    


def updateProfile(request):
    if 'user' in request.session.keys():
        product_count=request.session.get('count')
        email=request.session['email']
        try:
            user=User.objects.filter(email=email)
            print(user[0].first_name +" "+ user[0].last_name)
            name=user[0].first_name
            details={'name':name,'count':product_count}
            context = {
            'details':details
            }
        except:
            return HttpResponse("oops! something went wrong")
        return render(request, "user/update-profile.html",context)
    else:
        return redirect('homepage')
    


def reviewOrder(request):
    if 'user' in request.session.keys():
        cart_products = request.session.get('cart_products', [])
        product_count=request.session.get('count')
        email=request.session['email']
        order_summary=request.session['order_summary']
        payment_details=request.session.get('payment_details')
        if request.method=='POST':
            presc=request.FILES['prescription']
            payment_mode=request.POST.get('payment_method')
            print(payment_mode)
            print(presc)
            delivery_address = order_summary['name'] + ' ' + order_summary['mobile'] + ' ' + order_summary['address']
            try:
                order = Order.objects.create(
                    user=email,
                    amount=payment_details['mrp_total'],
                    prescription=presc,
                    quantity=1,
                    discount=payment_details['total_discount'],
                    payment_method=payment_mode,
                    delivery_address=delivery_address
                    )
                for product_id in cart_products:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=1)
                
                return redirect('placed_orders')
            except:
                return HttpResponse("oops! something went wrong")

        print(payment_details['mrp_total'])
        
        
        print(cart_products)
            
        
        try:
            user=User.objects.filter(email=email)
            print(user[0].first_name +" "+ user[0].last_name)
            name=user[0].first_name
            details={'name':name,'count':product_count}
            context = {
            'details':details,'payment_summary':payment_details,'order_summary':order_summary
            }
        except:
            return HttpResponse("oops! something went wrong")
        
        return render(request, "user/review-order.html",context)
    else:
        return redirect('homepage')
    

def placed_orders(request):
    if 'user' in request.session.keys():
        
        email=request.session['email']       
        try:
            send_mail(
                    "order placed",
                    "Your order has been placed successfully. You can check the details in your orders",
                    "rabsramii8010@gmail.com",
                    [email],
                    fail_silently=False,
                )
            user=User.objects.filter(email=email)
            print(user[0].first_name +" "+ user[0].last_name)
            name=user[0].first_name
            details={'name':name}
            del request.session['count']
            del request.session['cart_products']
            del request.session['order_summary']
            del request.session['payment_details']
            

            
            context = {
            'details':details
            }
        except:
            return HttpResponse("oops! something went wrong")
        
        return render(request, "user/placed-orders.html",context)
    else:
        return redirect('homepage')

def upload(request):
    if 'user' in request.session.keys():
        product_count=request.session.get('count')
        email=request.session['email']
        try:
            user=User.objects.filter(email=email)
            print(user[0].first_name +" "+ user[0].last_name)
            name=user[0].first_name
            details={'name':name,'count':product_count}
            context = {
            'details':details
            }
        except:
            return HttpResponse("oops! something went wrong")
        return render(request, "user/upload.html",context)
    else:
        return redirect('homepage')
    

def orders(request):
    if 'user' in request.session.keys():
        return render(request, "user/orders.html")
    else:
        return redirect('homepage')

def userLogout(request):
    logout(request)
    return redirect('homepage')  
