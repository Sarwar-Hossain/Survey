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
                decoded = AESCipher().decrypt(decoded_pass)
                if password == decoded and user.email == 'admin@gmail.com':
                    if user.is_user_active:
                        request.session['user_name'] = user.user_name
                        messages.success(request, 'Login Successful!')
                        return redirect('customer_survey_report')
                    else:
                        messages.error(request, 'User isn\'t active!')
                        return render(request, 'customer_survey_app/log-in.html')
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
        return render(request, 'customer_survey_app/log-in.html')
    except KeyError as e:
        print(e)
        return redirect('login')
    except Exception as e:
        print(e)
        return render(request, 'customer_survey_app/log-in.html')


def customer_survey_report(request):
    try:
        return render(request, 'customer_survey_app/customer-survey-report.html')
    except KeyError as e:
        print(e)
        return redirect('customer_survey_report')
    except Exception as e:
        print(e)
        return redirect('customer_survey_report')


def create_shop_user(request):
    try:
        super_admin = request.session['user_name']
        shop_users = ShopUser.objects.all().order_by('user_name')

        if request.method == 'POST':
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
    except KeyError as e:
        print(e)
        return redirect('create_shop_user')
    except Exception as e:
        print(e)
        return redirect('create_shop_user')


def loylity_membership(request):
    try:
        return render(request, 'customer_survey_app/loyalty-membership-form.html')
    except KeyError as e:
        print(e)
        return redirect('loylity_membership')
    except Exception as e:
        print(e)
        return redirect('loylity_membership')


def customer_feedback(request):
    try:
        return render(request, 'customer_survey_app/customer-feedback-form.html')
    except KeyError as e:
        print(e)
        return redirect('customer_feedback')
    except Exception as e:
        print(e)
        return redirect('customer_feedback')


def thank_you(request):
    try:
        return render(request, 'customer_survey_app/thank-you.html')
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


