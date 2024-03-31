from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Movie_Serializer
from rest_framework.parsers import MultiPartParser
from .models import Movie
from rest_framework import status

 # parser_classes = [MultiPartParser]


# Create your views here.

def home_page(request):
    return render(request,"index.html")

class Movie_Api(APIView):

    def get(self,request,id=None,formate=None):
        try:

            if id == None:
                # geting data from the database 
                movies=Movie.objects.order_by('-rating')
                for movie in movies:
                    print("printimg the movie rating in descending order")
                    print(movie.rating)
                serializer=Movie_Serializer(movies,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                try:
                    movies=Movie.objects.get(id=id)
                    serializer=Movie_Serializer(movies)
                    return Response(serializer.data)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
       
        try:
            pydata = request.data
            serializer = Movie_Serializer(data=pydata)
            # Check if the data is valid
            try:
                if serializer.is_valid():
                # Save the data to the database
                    serializer.save()
               
                    msg = {"msg": "Data entry is successful"}
                    return Response(msg, status=status.HTTP_201_CREATED) 
                else:
                    # Return error response if data is not valid
                    msg = {"msg": "Data entry is not successful", "errors": serializer.errors}
                    return Response(msg, status=400)
                
            except Exception as e:
                print(e)
        except Exception as e:
            # Return error response if an exception occurs during processing
            msg = {"msg": "An error occurred", "error": str(e)}
            return Response(msg, status=500)



    
    def put(self,request,id,format=None):
        try:
           
            print(type(request.data))
            print("helloo mani")
            print(id)
            print(request.data)

            movie=Movie.objects.get(id=id)
            print("helloo mani2")
            serializer=Movie_Serializer(movie,data=request.data)
            print("helloo mani3")
            
            try:
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                

            except Exception as e:
                print(e)
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id,format=None):
        try:
            print(id)
            movie=Movie.objects.get(id=id)
            
            
            try:
                serializer=Movie_Serializer(movie , data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(serializer.data,status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
        
        
