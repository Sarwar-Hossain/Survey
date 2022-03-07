from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.login, name='login'),
                  path('customer/survey/report/', views.customer_survey_report, name='customer_survey_report'),
                  path('create/shop/user', views.create_shop_user, name='create_shop_user'),
                  path('loylity/membership/form/', views.loylity_membership, name='loylity_membership'),
                  path('customer/feedback/form/', views.customer_feedback, name='customer_feedback'),
                  path('thank/you/', views.thank_you, name='thank_you'),
                  path('delete/user/', views.delete_user, name='delete_user'),
                  path('logout/', views.logout, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
