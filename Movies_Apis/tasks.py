from celery import shared_task
import requests

@shared_task
def update_movie_rating():
    # Fetch movie details from API
    response = requests.get('http://127.0.0.1:8000/get_movie_api/')
    if response.status_code == 200:
        movies = response.json()

        # Update rating for each movie
        for movie in movies:
            movie_id = movie.get('id')
            movie_status = movie.get('status')

            # Check if movie_id and status are available
            if movie_id is None or movie_status is None:
                print("Skipping movie - id or status missing:", movie)
                continue

            print("Movie status:", movie_status)
           
            if movie_status != "finished":
                rating_increment = 10
                # Increment rating by 10
                movie['rating'] += rating_increment

                # Update movie details with new rating
                try:
                    update_response = requests.patch(f'http://127.0.0.1:8000/get_movie_api/{movie_id}/', json={'rating': movie['rating']})
                    if update_response.status_code != 200:
                        print(f"Failed to update movie {movie_id}")
                except Exception as e:
                    print(e)
            else:
                print(f"Skipping finished movie: {movie_id}")

    else:
        print(f"Failed to fetch movie details from API (status code: {response.status_code})")