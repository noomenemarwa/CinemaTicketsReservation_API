from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Resevation, Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializer,MovieSerializer,ReservationSerializer,PostSerializer
from rest_framework import status, generics, mixins, viewsets,filters
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .permissions import IsAuthorOrReadOnly


# 1 without REST and no model 
def no_rest_no_model(request):
    guests = [ 
        {
            'id':1,
            "name":"marwa",
            'mobile': 26185002,
        },
        {
            'id':2,
            "name":"yosra",
            'mobile': 26185003,
        }, 
    ]
    return JsonResponse(guests, safe=False)



# 2  model data default and without REST 
def no_rest_from_model(request):
    # get all data
    data = Guest.objects.all()
    # convert data to list 
    response = {
        'guests': list(data.values('name','mobile'))
    }
    return JsonResponse(response)

# 3 ******************function based views(FBV)***********************
# 3.1 GET POST
# decorator
@api_view(['GET', 'POST'])
def FBV_list(request):
    # GET
    if request.method=='GET':
        # get all guests
        guests = Guest.objects.all()
        # serialize guests(format of data)
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method=='POST':
        # deserializer  
        # recuperate entered data
        serializer =GuestSerializer(data=request.data)
        # check if data is valid
        if serializer.is_valid():
            # save data 
            serializer.save()
            # return success msg
            return Response(serializer.data,status.HTTP_201_CREATED)
        # return error msg
        return Response(serializer.data,status.HTTP_400_BAD_REQUEST)


# 3.1 GET PUT DELETE
@api_view(['GET', 'PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        # get Guests by pk
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET 
    if request.method=='GET':
        # serialize guests(format of data)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    # PUT
    elif request.method=='PUT':
        # deserializer  
        # recuperate entered data
        serializer =GuestSerializer(guest,data=request.data)
        # check if data is valid
        if serializer.is_valid():
            # save data 
            serializer.save()
            # return success msg
            return Response(serializer.data)
        # return error msg
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    if request.method=='DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 4 ******************class based views (CBV)**************************

# 4.1 List and Create == GET and POST
class CBV_list(APIView) :
    # get all Guest objects
    def get(self,request):
        guests=Guest.objects.all()
        serializer = GuestSerializer(guests, many =True)
        return Response(serializer.data)
    
    # post :create new Guest object
    def post(self,request):
        serializer = GuestSerializer(data=request.data)   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE calss based views --pk
class CBV_pk(APIView):
    # get Guest object with pk
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except:
            Guest.DoesNotExist
            raise Http404
    
    #get Guest with pk 
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    # update Guest
    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # delete
    def delete(self, request,pk):
        self.get_object(pk).delete()    
        return Response(status=status.HTTP_204_NO_CONTENT)

# ==> We use FBV when we have many businesses and we use CBV when we have a small business

# 5 ****************** Mixins **************************
#  5.1 mixins list (get and post)
# ListModelMixin : list of object
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset =Guest.objects.all()
    serializer_class=GuestSerializer

    def get(self,request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# 5.2 mixins get put delete
# RetrieveModelMixin : one object
class Mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset =Guest.objects.all()
    serializer_class=GuestSerializer

    def get(self,request,pk):
        return self.retrieve(request)

    def put(self, request,pk):
        return self.update(request)

    def delete(self, request,pk):
        return self.destroy(request)

# 6 ****************** Generics **************************
#  6.1 Generics list (get and post)

class Generics_list(generics.ListCreateAPIView):
    queryset =Guest.objects.all()
    serializer_class=GuestSerializer
    # basic authentication
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # token 
    authentication_classes = [TokenAuthentication]


#  6.2 Generics get put delete
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset =Guest.objects.all()
    serializer_class=GuestSerializer
    # basic authentication
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # token
    authentication_classes = [TokenAuthentication]

# 7 ****************** Viewsets **************************
# Viewsets for Guest
class Viewsets_guest(viewsets.ModelViewSet):
    queryset =Guest.objects.all()
    serializer_class=GuestSerializer
    
# Viewsets for Movie
class Viewsets_movie(viewsets.ModelViewSet):
    queryset =Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields=['movie']


# Viewsets for Reservation
class Viewsets_reservation(viewsets.ModelViewSet):
    queryset =Resevation.objects.all()
    serializer_class=ReservationSerializer


# *******************************************

# 8 Find movie(with FBV)
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(movie = request.data['movie'], hall =request.data['hall'])
    serializer= MovieSerializer(movies, many =True)
    return Response (serializer.data)

# 9 create reservation
@api_view(['POST'])
def new_reservation(request):
    movie= Movie.objects.get( hall =request.data['hall'],movie = request.data['movie'])
    guest =Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation =Resevation()
    reservation.guest =guest
    reservation.movie = movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)

# 10 post author editior 
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset= Post.objects.all()
    serializer_class=PostSerializer
    
