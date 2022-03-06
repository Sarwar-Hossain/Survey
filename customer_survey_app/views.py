from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from customer_survey_app.models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password


# Create your views here.

def login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = ShopUser.objects.get(email=email)
            if user:
                flag = check_password(password, user.password)
                if flag:
                    request.session['shop_user'] = user.user_name
                    messages.success(request, 'Login Successful!')
                    return render(request, 'customer_survey_app/user-form.html')
                else:
                    messages.error(request, 'User Credential Didn\'t Match!')
                    return render(request, 'customer_survey_app/log-in.html')
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
        if request.method == 'POST':
            user_name = request.POST.get('user_name').strip()
            mobile_no = request.POST.get('mobile_no').strip()
            email = request.POST.get('email').strip()
            password = request.POST.get('password').strip()
            shop_name = request.POST.get('shop_name').strip()
            shop_id = request.POST.get('shop_id').strip()

            if mobile_no != '' and not mobile_no.startswith('+88'):
                number = '+88' + mobile_no
            else:
                number = mobile_no

            hash_password = make_password(password)
            is_success = ShopUser.objects.create(user_name=user_name,
                                                 email=email,
                                                 password=hash_password,
                                                 is_user_active=True,
                                                 shop_id=shop_id,
                                                 shop_name=shop_name,
                                                 mobile_no=number)
            messages.success(request, 'User Created Successfully!')
            if is_success:
                return render(request, 'customer_survey_app/user-form.html')
            else:
                return redirect('create_shop_user')

        return render(request, 'customer_survey_app/user-form.html')
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

