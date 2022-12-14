"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# ** for viewsets**
router =DefaultRouter()
router.register('guests', views.Viewsets_guest)
router.register('movies', views.Viewsets_movie)
router.register('reservations', views.Viewsets_reservation)



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('tichets/',include('tichets.urls')),

    # 1
    path('json/norestnomodel/', views.no_rest_no_model),
    # 2
    path('json/jsonresponsemodel/', views.no_rest_from_model),

    # 3.1 GET and POST from REST framework function based view @api_view()
    path('rest/fbvlist/', views.FBV_list),

    # 3.2 GET and PUT and DELETE from REST framework function based view @api_view()
    path('rest/fbvlist/<int:pk>',views.FBV_pk),
  
     # 4.1 GET and POST from REST framework class based view APIView
    path('rest/cbvList/',views.CBV_list.as_view()),

     # 4.2 GET and PUT and DELET from REST framework class based view APIView
    path('rest/cbvList/<int:pk>',views.CBV_pk.as_view()),

     # 5.1 GET and POST from REST framework class based view Mixins
    path('rest/mixins/',views.Mixins_list.as_view()),

     # 5.2 GET and PUT and DELET from REST framework class based view Mixins
    path('rest/mixins/<int:pk>',views.Mixins_pk.as_view()),

     # 6.1 GET and POST from REST framework class based view Generics
    path('rest/generics/',views.Generics_list.as_view()),

     # 6.2 GET and PUT and DELET from REST framework class based view Generics
    path('rest/generics/<int:pk>',views.Generics_pk.as_view()),

    #7  Viewsets
    path('rest/viewsets/', include(router.urls)),

    # 8 find movie

    path('fbv/findmovie', views.find_movie),

    # 9 new reservation
    path('fbv/newreservation',views.new_reservation),

    # 10 rest auth url

    # option log in and log out
    path('api-auth',include('rest_framework.urls')),

    # 11 Token authentication 
    path('api-token-auth',obtain_auth_token),
    # (we must migrate)

    # 12.1 Post generics Post_list
    # path('rest/generics',views.Post_list.as_view()),

    # 12.2 Post generics Post_pk
    path('post/generics/<int:pk>',views.Post_pk.as_view()),
]   

