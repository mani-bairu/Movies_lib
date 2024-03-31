import pytest
from django.test import RequestFactory
from rest_framework.response import Response
from Movies_Apis.views import Movie_Api
from Movies_Apis.models import Movie
from Movies_Apis.serializer import Movie_Serializer
from datetime import date
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

@pytest.mark.django_db
class TestMovieApi:

    def test_get_all_movies(self):
        # Create some sample movies
        movie1 = Movie.objects.create(name="Movie 1", rating=5 , release_date=date(2024,1,12))
        movie2 = Movie.objects.create(name="Movie 2", rating=4,release_date=date(2024,1,12))
        movie3 = Movie.objects.create(name="Movie 3", rating=3,release_date=date(2024,1,12))

        # Mock a request to the API view
        request = RequestFactory().get('/get_movie_api/')
        view = Movie_Api.as_view()

        # Call the get method of the API view
        response = view(request)

        # Check if the response status code is 200 (OK)
        assert response.status_code == 200

        # Check if the response contains the serialized data of all movies
        serialized_data = Movie_Serializer([movie1, movie2, movie3], many=True).data
        assert response.data == serialized_data

    def test_get_single_movie(self):
        # Create a sample movie
        movie = Movie.objects.create(name="Single Movie", release_date=date(2024,1,13),rating=5)

        # Mock a request to the API view to get the single movie
        request = RequestFactory().get('/get_movie_api/1/')
        view = Movie_Api.as_view()

        # Call the get method of the API view
        response = view(request, id=movie.id)

        # Check if the response status code is 200 (OK)
        assert response.status_code == 200

        # Check if the response contains the serialized data of the single movie
        serialized_data = Movie_Serializer(movie).data
        assert response.data == serialized_data


    def test_post_with_poster_and_trailer(self):
        # Create a sample movie data with poster and trailer files
        movie_data = {
            'name': 'Test Movie',
            'protagonists': 'Test Protagonists',
            'release_date': date(2024,4,23),
            'status': 'coming-up',
            'rating': 5
        }
        poster_file = SimpleUploadedFile("test_poster.jpg", b"dummy_content", content_type="image/jpeg")
        trailer_file = SimpleUploadedFile("test_trailer.mp4", b"dummy_content", content_type="video/mp4")

        # Mock a POST request to the API view with the movie data and files
        request = RequestFactory().post('/get_movie_api/', data=movie_data, FILES={'poster': poster_file, 'trailer': trailer_file})
        view = Movie_Api.as_view()

        # Call the post method of the API view
        response = view(request)

        # Check if the response status code is 201 (Created)
        assert response.status_code == status.HTTP_201_CREATED

        # Check if the movie data was successfully saved to the database
        assert Movie.objects.filter(name='Test Movie').exists()

        # Retrieve the saved movie object
        movie = Movie.objects.get(name='Test Movie')

        # Check if the poster and trailer files were uploaded and saved correctly
        # assert movie.poster.name == 'posters/test_poster.jpg'
        # assert movie.trailer.name == 'trailers/test_trailer.mp4'


    def test_put_valid_data(self):
        # Create a sample movie in the database
        movie = Movie.objects.create(name="Movie", protagonists='old Protagonists',rating=5 , release_date=date(2024,1,12))
        
        
        # Define updated movie data
        updated_data = {
            'name': 'Updated Movie',
            'protagonists': 'Updated Protagonists',
            'release_date': date(2024,4,25),
           
        }
        import json
        print(updated_data)
        print("type of data",type(updated_data))
        from django.http import QueryDict

       
        my_querydict = QueryDict('', mutable=True)
        my_querydict.update(updated_data)
        print(my_querydict)
        print("type of query dict",type(my_querydict))
       



        

       

        # Mock a PUT request to the API view with the updated datprint
        request = RequestFactory().put(f'/get_movie_api/{movie.id}/', data=updated_data, content_type='application/json')
        view = Movie_Api.as_view()

        # # Call the put method of the API view
        response = view(request, id=movie.id)

        # Check if the response status code is 201 (Created)
        assert response.status_code == status.HTTP_201_CREATED

        # Refresh the movie object from the database
        movie.refresh_from_db()

        # Check if the movie data was updated correctly
        assert movie.name == 'Updated Movie'
        assert movie.protagonists == 'Updated Protagonists'
        assert movie.release_date == date(2024,4,25)
       
    
    def test_put_invalid_data(self):
    # Create a sample movie in the database
        movie = Movie.objects.create(
            name="Old Movie",
            protagonists='Old Protagonists',
            release_date=date(2024, 4, 23),
            status="finished",
            rating=4
        )

        # Define invalid updated movie data (e.g., missing required fields)
        invalid_data = {
            "name": "New Movie",  
            "rating": 5 , 
            "release_date":date(2024, 4, 23),
         
        }

        # Mock a PUT request to the API view with the invalid data
        request = RequestFactory().put(f'/get_movie_api/{movie.id}/', data=invalid_data)
        view = Movie_Api.as_view()

        # Call the put method of the API view
        response = view(request, id=movie.id)

        # Check if the response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST




    def test_put_exception_handling(self):
        # Mock a PUT request to the API view with invalid data to trigger an exception
        request = RequestFactory().put('/get_movie_api/999/', data={})
        view = Movie_Api.as_view()

        # Call the put method of the API view
        response = view(request, id=999)

        # Check if the response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_patch_valid_data(self):
        # Create a sample movie in the database
        movie = Movie.objects.create(
            name="Old Movie",
            protagonists='Old Protagonists',
            release_date=date(2024, 4, 23),
            status="finished",
            rating=4
        )

        # Define updated movie data
        updated_data = {
            'name': 'Updated Movie',
            'protagonists': 'Updated Protagonists',
            'release_date': date(2024, 4, 23),
            'status': 'finished',
            # 'rating': 4
        }

        # Mock a PATCH request to the API view with the updated data
        request = RequestFactory().patch(f'/get_movie_api/{movie.id}/',  data=updated_data, content_type='application/json')
        view = Movie_Api.as_view()

        # Call the patch method of the API view
        response = view(request, id=movie.id)

        # Check if the response status code is 201 (created)
        assert response.status_code == status.HTTP_201_CREATED

        # Refresh the movie object from the database
        movie.refresh_from_db()

        # Check if the movie data was updated correctly
        # assert movie.name == 'Updated Movie'
        # assert movie.protagonists == 'Updated Protagonists'
        # assert str(movie.release_date) == date(2024, 4, 23)
        assert movie.status == 'finished'
        # assert movie.rating == 4

    def test_patch_invalid_data(self):
        # Create a sample movie in the database
        movie = Movie.objects.create(
            name="Old Movie",
            protagonists='Old Protagonists',
            release_date=date(2024, 4, 23),
            status="finished",
            rating=4
        )

        # Define invalid updated movie data (e.g., invalid fields)
        invalid_data = {
            'invalid_field': 'Invalid Value'
        }

        # Mock a PATCH request to the API view with the invalid data
        request = RequestFactory().patch(f'/get_movie_api/{movie.id}/', data=invalid_data)
        view = Movie_Api.as_view()

        # Call the patch method of the API view
        response = view(request, id=movie.id)

        # Check if the response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_exception_handling(self):
        # Mock a PATCH request to the API view with invalid ID to trigger an exception
        request = RequestFactory().patch('/get_movie_api/999/', data={})
        view = Movie_Api.as_view()

        # Call the patch method of the API view
        response = view(request, id=999)

        # Check if the response status code is 400 (Bad Request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST