from calendar import c
from re import template
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages, auth
from accounts.models import CustomAccount, UserProfile
from accounts.forms import RegisterForm
from carts.views import cart_id_session
from carts.models import Cart, CartItem

#Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from gems_shop import settings





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database 

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomAccount.objects.create_user(username=username, email=email, password=password)
            user.save()


            # save form in the memory not in database  
            #user = form.save(commit=False)  
            #user.is_active = False  
            #user.save() 

            # Create a user profile
            #profile = UserProfile()
            #profile.user_id = user.id
            #profile.save()

            # USER ACTIVATION
            # to get the domain of the current site 

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            template = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email= EmailMessage(mail_subject,template,settings.EMAIL_HOST_USER,[to_email])
            send_email.send()
            messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/login/?command=verification&email='+email)  
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', context={'form': form})




def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=cart_id_session(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    gem_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        gem_variation.append(list(variation))
        
                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)


                    for pr in gem_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            
            except:
                pass
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    else:
        return render(request, 'login.html')




@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomAccount._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email'] # email entre crochet correspond au name='email' dans le input 
        if CustomAccount.objects.filter(email=email).exists():
            user = CustomAccount.objects.get(email__exact=email) # __exact permet de vérifier une correspondance exact (sensible a la case ?) 
            
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            template = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email= EmailMessage(mail_subject,template,settings.EMAIL_HOST_USER,[to_email])
            send_email.send()

            messages.success(request, 'Password rest email has been sent to your email address.')
            return redirect('login')
        
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'forgotPassword.html')




def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomAccount._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']= uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomAccount.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password rest successful')
            return redirect('login')

        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'resetPassword.html')