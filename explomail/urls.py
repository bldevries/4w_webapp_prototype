from django.urls import path

from explomail import views

app_name = 'explomail'
urlpatterns = [
    path('', views.index, name='index'),
    path('mails/', views.index),
    path('mails/<int:pk>/', views.mail_detail, name='detail'),
    path('mails/search/', views.search, name='search'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('api/', views.mail_api),
    path('api/mail_search/<str:search_string>/', views.mail_search_text_api),
    path('api/clients/', views.client_api),
    path('api/clients/<int:pk>/', views.client_api_pk),
    path('api/client_search/<str:search_string>/', views.client_search_name_api),
    path('api/search/', views.api_search),
    # path('text_search/<str:search_string>', views.mail_search_text,
    # 	name='mail_search_text'),
    #path('mails/text_search/', views.mail_search_text),
]