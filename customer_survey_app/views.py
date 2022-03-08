from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from customer_survey_app.models import *
from django.contrib import messages
from customer_survey_app.aes_cipher import AESCipher


def login(request):
    try:
        # clear all session
        request.session.flush()
        # Login
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = ShopUser.objects.get(email=email)
            decoded_pass = eval(user.password)

            if user:
                # admin login
                decoded = AESCipher().decrypt(decoded_pass)
                if password == decoded and user.email == 'admin@gmail.com':
                    if user.is_user_active:
                        request.session['user_name'] = user.user_name
                        messages.success(request, 'Login Successful!')
                        return redirect('customer_survey_report')
                    else:
                        messages.error(request, 'User isn\'t active!')
                        return render(request, 'customer_survey_app/log-in.html')
                # Shop user login
                elif password == decoded and user.email == email:
                    if user.is_user_active:
                        request.session['user_name'] = user.user_name
                        messages.success(request, 'Login Successful!')
                        return redirect('loylity_membership')
                    else:
                        messages.error(request, 'User isn\'t active!')
                        return render(request, 'customer_survey_app/log-in.html')
                else:
                    messages.error(request, 'User Credential Didn\'t Match!')
                    return render(request, 'customer_survey_app/log-in.html')
        else:
            return redirect('log-in')
    except KeyError as e:
        print(e)
        return redirect('login')
    except Exception as e:
        print(e)
        return render(request, 'customer_survey_app/log-in.html')


def customer_survey_report(request):
    try:
        if request.session.has_key('user_name'):
            demo = get_percentage(3, 5)
            print(demo)
            return render(request, 'customer_survey_app/customer-survey-report.html', {'demo': demo})
        else:
            return redirect('login')
    except KeyError as e:
        print(e)
        return redirect('customer_survey_report')
    except Exception as e:
        print(e)
        return redirect('customer_survey_report')


def create_shop_user(request):
    try:
        if request.session.has_key('user_name'):
            super_admin = request.session['user_name']
            shop_users = ShopUser.objects.all().order_by('user_name')

            if request.method == 'POST':
                # Create Shop User
                if 'button_submit' in request.POST:
                    user_name = request.POST.get('user_name').strip()
                    mobile_no = request.POST.get('mobile_no').strip()
                    email = request.POST.get('email').strip()
                    password = request.POST.get('password').strip()
                    shop_name = request.POST.get('shop_name').strip()
                    shop_id = request.POST.get('shop_id').strip()
                    encoded_password = AESCipher().encrypt(password)

                    if mobile_no != '' and not mobile_no.startswith('+88'):
                        number = '+88' + mobile_no
                    else:
                        number = mobile_no

                    is_success = ShopUser.objects.create(user_name=user_name,
                                                         email=email,
                                                         password=encoded_password,
                                                         is_user_active=True,
                                                         shop_id=shop_id,
                                                         shop_name=shop_name,
                                                         mobile_no=number,
                                                         created_by=super_admin,
                                                         created_time=datetime.now())
                    messages.success(request, 'User Created Successfully!')
                    if is_success:
                        return render(request, 'customer_survey_app/user-form.html', {'shop_users': shop_users})
                    else:
                        return redirect('create_shop_user')

                # Select Shop User
                elif 'button_select' in request.POST:
                    user_id = request.POST.get('user_id').strip()
                    single_user = ShopUser.objects.get(id=user_id)
                    password = eval(single_user.password)
                    decoded_password = AESCipher().decrypt(password)
                    messages.success(request, "User Selected!")
                    context = {
                        'single_user': single_user,
                        'shop_users': shop_users,
                        'password': decoded_password
                    }
                    return render(request, 'customer_survey_app/user-form.html', context)

                # Update Shop User
                elif 'button_update' in request.POST:
                    user_id = request.POST.get('user_id').strip()
                    user_name = request.POST.get('user_name').strip()
                    mobile_no = request.POST.get('mobile_no').strip()
                    email = request.POST.get('email').strip()
                    password = request.POST.get('password').strip()
                    shop_name = request.POST.get('shop_name').strip()
                    shop_id = request.POST.get('shop_id').strip()
                    encoded_password = AESCipher().encrypt(password)

                    user_update = ShopUser.objects.filter(id=user_id).update(user_name=user_name,
                                                                             email=email,
                                                                             password=encoded_password,
                                                                             shop_name=shop_name,
                                                                             mobile_no=mobile_no,
                                                                             shop_id=shop_id,
                                                                             updated_by=super_admin,
                                                                             updated_time=datetime.now())
                    messages.success(request, "User Updated!")
                    context = {
                        'shop_users': shop_users
                    }
                    return render(request, 'customer_survey_app/user-form.html', context)

                # Deactivate Shop User
                elif 'user_deactivate' in request.POST:
                    user_id = request.POST.get('user_deactivate').strip()
                    deactivate = ShopUser.objects.filter(id=user_id).update(
                        updated_by=super_admin,
                        is_user_active=False,
                        updated_time=datetime.now())
                    messages.success(request, "User Deactivated Successful!")
                    context = {
                        'shop_users': shop_users
                    }
                    return render(request, 'customer_survey_app/user-form.html', context)

                # Activate Shop User
                elif 'user_activate' in request.POST:
                    user_id = request.POST.get('user_activate').strip()
                    deactivate = ShopUser.objects.filter(id=user_id).update(
                        updated_by=super_admin,
                        is_user_active=True,
                        updated_time=datetime.now())
                    messages.success(request, "User Activated Successful!")
                    context = {
                        'shop_users': shop_users
                    }
                    return render(request, 'customer_survey_app/user-form.html', context)
            return render(request, 'customer_survey_app/user-form.html', {'shop_users': shop_users})
        else:
            return redirect('login')
    except KeyError as e:
        print(e)
        return redirect('create_shop_user')
    except Exception as e:
        print(e)
        return redirect('create_shop_user')


def loylity_membership(request):
    try:
        if request.session.has_key('user_name'):
            user_name = request.session['user_name']
            categories = Category.objects.all()
            if 'button_submit' in request.POST:
                membership_no = request.POST.get('membership_no')
                in_voice_no = request.POST.get('in_voice_no')
                category_id = request.POST.get('category_id')
                title = request.POST.get('title')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                contact_no = request.POST.get('contact_no')
                date_of_birth = request.POST.get('date_of_birth')
                marital_status = request.POST.get('marital_status')
                address = request.POST.get('address')

                if contact_no != '' and not contact_no.startswith('+88'):
                    number = '+88' + contact_no
                else:
                    number = contact_no

                create_member = Customer.objects.create(membership_no=membership_no,
                                                        in_voice_no=in_voice_no,
                                                        category_id=category_id,
                                                        title=title,
                                                        first_name=first_name,
                                                        last_name=last_name,
                                                        email=email,
                                                        contact_no=number,
                                                        date_of_birth=date_of_birth,
                                                        marital_status=marital_status,
                                                        address=address,
                                                        created_by=user_name,
                                                        created_time=datetime.now())
                messages.success(request, 'Form Submitted')
                return redirect('customer_feedback')
            else:
                return render(request, 'customer_survey_app/loyalty-membership-form.html', {'categories': categories})
        else:
            return redirect('login')
    except KeyError as e:
        print(e)
        return redirect('loylity_membership')
    except Exception as e:
        print(e)
        return redirect('loylity_membership')


def customer_feedback(request):
    try:
        if request.session.has_key('user_name'):
            user_name = request.session['user_name']
            if 'button_submit' in request.POST:
                question_1 = request.POST.get('question_1')
                question_2 = request.POST.get('question_2')
                question_3 = request.POST.get('question_3')
                question_4 = request.POST.get('question_4')
                question_5 = request.POST.get('question_5')
                question_6 = request.POST.get('question_6').strip().capitalize()
                question_7 = request.POST.get('question_7').strip().capitalize()
                question_8 = request.POST.get('question_8').strip().capitalize()
                address = request.POST.get('address').strip().capitalize()

                create_feedback = CustomerFeedback.objects.create(question_1=question_1,
                                                                  question_2=question_2,
                                                                  question_3=question_3,
                                                                  question_4=question_4,
                                                                  question_5=question_5,
                                                                  question_6=question_6,
                                                                  question_7=question_7,
                                                                  question_8=question_8,
                                                                  address=address,
                                                                  created_by=user_name,
                                                                  created_time=datetime.now())
                messages.success(request, 'Form Submitted')
                return redirect('thank_you')
            else:
                return render(request, 'customer_survey_app/customer-feedback-form.html')
        else:
            return redirect('login')
    except KeyError as e:
        print(e)
        return redirect('customer_feedback')
    except Exception as e:
        print(e)
        return redirect('customer_feedback')


def thank_you(request):
    try:
        if request.session.has_key('user_name'):
            return render(request, 'customer_survey_app/thank-you.html')
        else:
            return redirect('login')
    except KeyError as e:
        print(e)
        return redirect('thank_you')
    except Exception as e:
        print(e)
        return redirect('thank_you')


def logout(request):
    request.session.clear()
    return redirect('login')


# Delete User

def delete_user(request):
    user_id = request.GET.get('user_id')
    user_deleted = ShopUser.objects.filter(id=user_id).delete()
    context = {
        'toast_type': 'info',
        'toast_message': 'User Deleted Successfully!!',
    }
    return JsonResponse(context)


# Covert into Boolean Field
def str_to_bool(radio_button_value):
    if radio_button_value == 'True':
        return True
    elif radio_button_value is None:
        return False
    else:
        raise ValueError


# Get Percentage
def get_percentage(part, whole):
    percentage = 100 * float(part)/float(whole)
    return str(percentage) + '%'
