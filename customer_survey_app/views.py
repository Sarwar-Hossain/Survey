from django.http import JsonResponse
from django.shortcuts import redirect
from customer_survey_app.models import *
from django.contrib import messages
from customer_survey_app.aes_cipher import AESCipher
from django.db import connection
from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator

cursor = connection.cursor()


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

            # Question 1
            cursor.execute('''SELECT 
            sum(CASE WHEN csac.question_1 IS true THEN 1 ELSE 0 END) AS question_1_true_part,
            sum(CASE WHEN  csac.question_1 IS false THEN 1 ELSE 0 END) AS question_1_false_part,
            sum(CASE WHEN  csac.question_1 IS false THEN 1 ELSE 1 END) AS question_1_whole
            FROM customer_survey_app_customerfeedback csac;''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_1_true = get_percentage(data[0]['question_1_true_part'], data[0]['question_1_whole'])
            question_1_false = get_percentage(data[0]['question_1_false_part'], data[0]['question_1_whole'])

            # Question 2
            cursor.execute(''' SELECT 
            sum(CASE WHEN csac.question_2 = 'Friendly' THEN 1 ELSE 0 END) AS question_2_friendly_part,
            sum(CASE WHEN csac.question_2 = 'Knowledgeable' THEN 1 ELSE 0 END) AS question_2_knowledgeable_part,
            sum(CASE WHEN csac.question_2 = 'Helpful' THEN 1 ELSE 0 END) AS question_2_helpful_part,
            sum(CASE WHEN csac.question_2 = 'Helpful' THEN 1 ELSE 1 END) AS question_2_whole
            FROM customer_survey_app_customerfeedback csac; ''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_2_friendly = get_percentage(data[0]['question_2_friendly_part'], data[0]['question_2_whole'])
            question_2_knowledgeable = get_percentage(data[0]['question_2_knowledgeable_part'],
                                                      data[0]['question_2_whole'])
            question_2_helpful = get_percentage(data[0]['question_2_helpful_part'], data[0]['question_2_whole'])

            # Question 3
            cursor.execute(''' SELECT 
            sum(CASE WHEN csac.question_3 = 'Slightly' THEN 1 ELSE 0 END) AS question_3_slightly_part,
            sum(CASE WHEN csac.question_3 = 'Moderate' THEN 1 ELSE 0 END) AS question_3_moderate_part,
            sum(CASE WHEN csac.question_3 = 'Strongly' THEN 1 ELSE 0 END) AS question_3_strongly_part,
            sum(CASE WHEN csac.question_3 = 'Strongly' THEN 1 ELSE 1 END) AS question_3_whole
            FROM customer_survey_app_customerfeedback csac; ''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_3_slightly = get_percentage(data[0]['question_3_slightly_part'], data[0]['question_3_whole'])
            question_3_moderate = get_percentage(data[0]['question_3_moderate_part'], data[0]['question_3_whole'])
            question_3_strongly = get_percentage(data[0]['question_3_strongly_part'], data[0]['question_3_whole'])

            # Question 4
            cursor.execute(''' SELECT 
            sum(CASE WHEN csac.question_4 IS true THEN 1 ELSE 0 END) AS question_4_true_part,
            sum(CASE WHEN  csac.question_4 IS false THEN 1 ELSE 0 END) AS question_4_false_part,
            sum(CASE WHEN  csac.question_4 IS false THEN 1 ELSE 1 END) AS question_4_whole
            FROM customer_survey_app_customerfeedback csac; ''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_4_true = get_percentage(data[0]['question_4_true_part'], data[0]['question_4_whole'])
            question_4_false = get_percentage(data[0]['question_4_false_part'], data[0]['question_4_whole'])

            # Question 5
            cursor.execute(''' SELECT 
            sum(CASE WHEN csac.question_5 IS true THEN 1 ELSE 0 END) AS question_5_true_part,
            sum(CASE WHEN  csac.question_5 IS false THEN 1 ELSE 0 END) AS question_5_false_part,
            sum(CASE WHEN  csac.question_5 IS false THEN 1 ELSE 1 END) AS question_5_whole
            FROM customer_survey_app_customerfeedback csac; ''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_5_true = get_percentage(data[0]['question_5_true_part'], data[0]['question_5_whole'])
            question_5_false = get_percentage(data[0]['question_5_false_part'], data[0]['question_5_whole'])

            # Question 6
            cursor.execute(''' SELECT 
            sum(CASE WHEN csac.question_6 = 'Small' THEN 1 ELSE 0 END) AS question_6_small_part,
            sum(CASE WHEN csac.question_6 = 'Medium' THEN 1 ELSE 0 END) AS question_6_medium_part,
            sum(CASE WHEN csac.question_6 = 'Large' THEN 1 ELSE 0 END) AS question_6_large_part,
            sum(CASE WHEN csac.question_6 = 'Extra Large' THEN 1 ELSE 0 END) AS question_6_extra_large_part,
            sum(CASE WHEN csac.question_6 = 'Extra Extra Large' THEN 1 ELSE 0 END) AS question_6_extra_extra_large_part,
            sum(CASE WHEN csac.question_6 = 'Small' THEN 1 ELSE 1 END) AS question_6_whole
            FROM customer_survey_app_customerfeedback csac; ''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_6_small = get_percentage(data[0]['question_6_small_part'], data[0]['question_6_whole'])
            question_6_medium = get_percentage(data[0]['question_6_medium_part'], data[0]['question_6_whole'])
            question_6_large = get_percentage(data[0]['question_6_large_part'], data[0]['question_6_whole'])
            question_6_extra_large = get_percentage(data[0]['question_6_extra_large_part'], data[0]['question_6_whole'])
            question_6_extra_extra_large = get_percentage(data[0]['question_6_extra_extra_large_part'],
                                                          data[0]['question_6_whole'])

            # Question 7
            cursor.execute(''' SELECT 
            sum(CASE WHEN csac.question_7 = 'Black' THEN 1 ELSE 0 END) AS question_7_black_part,
            sum(CASE WHEN csac.question_7 = 'White' THEN 1 ELSE 0 END) AS question_7_white_part,
            sum(CASE WHEN csac.question_7 = 'Others' THEN 1 ELSE 0 END) AS question_7_others_part,
            sum(CASE WHEN csac.question_7 = 'Others' THEN 1 ELSE 1 END) AS question_7_whole
            FROM customer_survey_app_customerfeedback csac; ''')

            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            question_7_black = get_percentage(data[0]['question_7_black_part'], data[0]['question_7_whole'])
            question_7_white = get_percentage(data[0]['question_7_white_part'], data[0]['question_7_whole'])
            question_7_others = get_percentage(data[0]['question_7_others_part'], data[0]['question_7_whole'])

            context = {
                'question_1_true': question_1_true,
                'question_1_false': question_1_false,
                'question_2_friendly': question_2_friendly,
                'question_2_knowledgeable': question_2_knowledgeable,
                'question_2_helpful': question_2_helpful,
                'question_3_slightly': question_3_slightly,
                'question_3_moderate': question_3_moderate,
                'question_3_strongly': question_3_strongly,
                'question_4_true': question_4_true,
                'question_4_false': question_4_false,
                'question_5_true': question_5_true,
                'question_5_false': question_5_false,
                'question_6_small': question_6_small,
                'question_6_medium': question_6_medium,
                'question_6_large': question_6_large,
                'question_6_extra_large': question_6_extra_large,
                'question_6_extra_extra_large': question_6_extra_extra_large,
                'question_7_black': question_7_black,
                'question_7_white': question_7_white,
                'question_7_others': question_7_others,
            }
            return render(request, 'customer_survey_app/customer-survey-report.html', context)
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

                    if mobile_no != '' and not mobile_no.startswith('+88'):
                        number = '+88' + mobile_no
                    else:
                        number = mobile_no

                    user_update = ShopUser.objects.filter(id=user_id).update(user_name=user_name,
                                                                             email=email,
                                                                             password=encoded_password,
                                                                             shop_name=shop_name,
                                                                             mobile_no=number,
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
                question_6 = request.POST.get('question_6')
                question_7 = request.POST.get('question_7')
                question_8 = request.POST.get('question_8')
                address = request.POST.get('address')

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


def show_comments(request):
    try:
        if request.session.has_key('user_name'):
            customer_feedbacks = CustomerFeedback.objects.all()
            paginator = Paginator(customer_feedbacks, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request=request, template_name="customer_survey_app/show_comments.html",
                          context={'customer_feedbacks': page_obj})
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


# String Covert into Boolean Field
def str_to_bool(radio_button_value):
    if radio_button_value == 'True':
        return True
    elif radio_button_value is None:
        return False
    else:
        raise ValueError


# Get Percentage
def get_percentage(part, whole):
    percentage = 100 * float(part) / float(whole)
    limited_float_percentage = ("%.2f" % percentage)
    return str(limited_float_percentage) + '%'


