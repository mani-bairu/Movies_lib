from django.shortcuts import render,redirect
import requests
from .forms import MovieForm

def Submit_Movie(request):
    form = MovieForm()
    movie_data = []
    
    movedata=requests.get('http://127.0.0.1:8000/get_movie_api/')
    if movedata.status_code == 200:
        movie_data = movedata.json()
        
    else:
        print('Error:', movedata.status_code)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                protagonists=form.cleaned_data['protagonists']
                release_date = form.cleaned_data['release_date']
                status = form.cleaned_data['status']

             
                data = {
                    'name': name,
                    'release_date': release_date,
                    'status': status,
                    'protagonists':protagonists
                }
                files = {
                    'poster': request.FILES.get('poster'),
                    'trailer': request.FILES.get('trailer')

                }
                try:


                    response = requests.post('http://127.0.0.1:8000/get_movie_api/', data=data , files=files)
                    response.raise_for_status() 

                    if response.status_code == 201:
                        print('Data added successfully')
                        return redirect('/addmovie/',{response.status_code})
                    
                    
                    else:
                        print(f"Unexpected status code: {response.status_code}")

                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

    return render(request, 'addmovie.html', {'form': form,'movie_data':movie_data})


def Update_Movie_Status(request,id):
    
    movie_details=requests.get("http://127.0.0.1:8000/get_movie_api/"+str(id))
    print("movie id ",{id})
    if movie_details.status_code == 200:
        current_movie_data = movie_details.json()
       
    else:
        print('Error:', movie_details.status_code)

    if request.method =='POST':
        updated_status=request.POST.get('status')
        updated_date=request.POST.get('release_date')
        print(updated_status)
        print(updated_date)
        print(current_movie_data['protagonists'])

        updated_data={
           
            'status':updated_status,
            'name':current_movie_data['name'],
            'protagonists':current_movie_data['protagonists'],
            'release_date':current_movie_data['release_date'],
            }
        
        try:
            
            response=requests.put('http://127.0.0.1:8000/get_movie_api/'+str(id)+'/',json=updated_data)
            try:
                response.status_code==200
                print("status code: ",response.status_code)
                updated_movie_data=response.json()
                print(current_movie_data['poster'])
                print(current_movie_data['trailer'])

                print("updated movie data: ",updated_movie_data)
                return redirect('/addmovie/')
                
                
            except Exception as e:
             print('Error:',e)
        except Exception as e:
            print(e)





    return render(request,"update_status.html",{'movie_data':current_movie_data})


















                # print("which type of name in demo2",type(data['name']))
                # print("which type of release_date demo2",type(data['release_date']))
                # print("which type of status demo2",type(data['status']))


                
              

                # print("poster type demo2: ",type(files['poster']))
                # print("trailer type demo2: ",type(files['trailer']))

#  print("trailer value from data dict ",type(files['trailer']))
#             print("poster value from data dict ",type(files['poster']))
#  print("type of name",type(data['name']))
#             print("type of release_date",type(data['release_date']))
#             print("type of status",type(data['status']))

 # poster = request.FILES['poster']  # Get the uploaded poster file
            # trailer = request.FILES['trailer']  # Get the uploaded trailer file

            # Assume 'uploaded_file' is an InMemoryUploadedFile object
            # poster_file = InMemoryUploadedFile(poster)
            # trailer_file = InMemoryUploadedFile(trailer)


            # Extract file data from the InMemoryUploadedFile object
            # poster_data = poster_file.read()
            # trailer_data = trailer_file.read()


            # Process the files (e.g., convert to Base64, save to disk)
            # For demonstration, let's assume you're converting files to Base64
            # poster_data = poster.read()
            # trailer_data = trailer.read()
            # poster_base64 = base64.b64encode(poster_data).decode('utf-8')
            # trailer_base64 = base64.b64encode(trailer_data).decode('utf-8')
