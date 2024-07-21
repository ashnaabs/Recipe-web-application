from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger
from django.shortcuts import render,redirect
from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .forms import *
from django.contrib import messages
import requests
# Create your views here.

class RecipeCreativeView(generics.ListCreateAPIView):
    queryset = recipes.objects.all()
    serializer_class = RecipesSerializers
    permission_classes = [AllowAny]

class RecipesDetails(generics.RetrieveAPIView):
    queryset = recipes.objects.all()
    serializer_class = RecipesSerializers

class RecipesUpdateView(generics.RetrieveUpdateAPIView):
    queryset = recipes.objects.all()
    serializer_class = RecipesSerializers

class RecipesDelete(generics.DestroyAPIView):
    queryset = recipes.objects.all()
    serializer_class = RecipesSerializers


class RecipeSearch(generics.ListAPIView):  #to search a recipe by name, ListAPIview used to show the list of search items
    queryset = recipes.objects.all()
    serializer_class = RecipesSerializers

    def get_queryset(self):    #fn created to search by a name
        name=self.kwargs.get('Name')      #search by name,keywordarguments
        return recipes.objects.filter(Name_icontains=name) #returning the name contains result


import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import RecipesForm
import requests


# to connect the created api with front end, form
def CreateRecipe(request):
    if request.method=='POST':
        form=RecipesForm(request.POST,request.FILES) #FILES is the uploaded data
        print(form.data)
        if form.is_valid():           #checking if the form is valid
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/create_recipe/'
                data=form.cleaned_data

                print(data)

                response=requests.post(api_url,data=data,files={'Recipe_img': request.FILES['Recipe_img']}) #The request.post method sends a POST request to the API URL with the data dictionary and the recipe image file (request.FILES['Recipe_img']) under the key 'Recipe_img'.

                if response.status_code == 400:         #to handle api response, if the stss code of response is 200 it is success
                    messages.success(request,'Recipe inserted successfullu')  #success msg

                else:
                    messages.error(request,f'Error{response.status_code}') #error msg

            except requests.RequestException as e:    #if there is an exception occurs an error msg will show
                messages.error(request,f'Error during API request {str(e)}')

        else:
            messages.error(request,'Form is not valid')
        return redirect('index')
    else:
        form=RecipesForm()       #If the request method is GET (likely the initial page load), an empty RecipesForm instance is created.
    recipe= recipes.objects.all()

    return render(request,'create_recipe.html',{'form':form,'recipe':recipe}) #This renders the template named create_recipe.html.
#     #The context dictionary ({'form': form}) passes the form object to the template, likely for displaying the form fields in the HTML.


def update_detail(request,id):  #handles potentially updating a recipe detail in your Django application
    api_url = f'http://.0.0.1:8000/detail/{id}'
    response = requests.get(api_url)  #getting data from api_url
    if response.status_code == 200:
        data = response.json()    #The response data is assumed to be JSON format, so it's converted to a Python dictionary using response.json().
        ingredients=data['description'].split('.')  #The code extracts a list of ingredients by splitting the recipe's Description field at each "." (period)
    return render(request,'recipe_update.html',{'recipes':data,'ingredients':ingredients})
    #recipes: This passes the entire retrieved recipe data (data) to the template, likely for pre-populating form fields with existing values.
     #'ingredients': This passes the extracted list of ingredients (ingredients) to the template, potentially for separate display or manipulation.
def update_recipe(request, id):
    api_url = f'http://127.0.0.1:8000/update/{id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        existing_data = response.json()
    else:
        existing_data = None
        messages.error(request, 'Error fetching data from the API.')

    if request.method == 'POST':
        form = RecipesForm(request.POST, request.FILES, instance=recipes.objects.get(pk=id))
        if form.is_valid():
            try:
                form.save()
                update_api_url = f'http://127.0.0.1:8000/update_recipe/{id}/'
                data = form.cleaned_data

                files = {'Recipe_img': request.FILES['Recipe_img']} if 'Recipe_img' in request.FILES else None

                response = requests.put(update_api_url, data=data, files=files)

                if response.status_code == 200:
                    messages.success(request, 'Recipe updated successfully.')
                else:
                    messages.error(request, f'Error {response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request {str(e)}')
        else:
            messages.error(request, 'Form is not valid')
        return redirect('index')
    else:
        form = RecipesForm(instance=recipes.objects.get(pk=id))

    return render(request, 'recipe_'
                           'update.html', {'form': form, 'recipe': existing_data})

#This code snippet doesn't directly leverage Django forms. It manually extracts data from the request object.
#The code manually extracts individual form field values from the request object's POST dictionary:
#name, prep_time, difficulty, and description are retrieved directly by their names.
#vegetarian is retrieved using request.POST.get('vegetarian', 'false'). This provides a default value of 'false' if the key doesn't exist in the POST data.
#A dictionary named data is constructed. It includes the extracted form field values as key-value pairs.
#A separate dictionary named files is created to handle the image file upload (if present). It uses request.FILES.get('Recipe_image') again to potentially retrieve the image file.

def index(request):
    if request.method == 'POST':
        search = request.POST.get('search', '')
        api_url = f'http://127.0.0.1:8000/search/{search}/'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return render(request, 'index.html', {'data': data})
            else:
                return render(request, 'index.html', {'error_message': f'Error: {response.status_code}'})
        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error: {str(e)}'})

    else:
        api_url = f'http://127.0.0.1:8000/create/'

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                original_data = response.json()

                paginator = Paginator(original_data, 6)

                page = request.GET.get('page', 1)

                try:
                    recepies = paginator.page(page)

                except PageNotAnInteger:
                    destinations = paginator.page(1)
                except EmptyPage:
                    destinations = paginator.page(paginator.num_pages)

                context = {'original_data': original_data, 'recepies': recepies}

                return render(request, 'index.html', context)

            else:
                return render(request, 'index.html', {'error_message': f'Error {response.status_code}'})

        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error {str(e)}'})

    return render(request, 'index.html')

def recipe_fetch(request,id):
    api_url = f'http://127.0.0.1:8000/details/{id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        ingredients=data['description'].split('.')
        return render(request,'recipe_fetch.html',{'recipes':data,'ingredients':ingredients})
    return render(request,'recipe_fetch.html')

def recipe_delete(request,id):
    api_url = f'http://.0.0.1:8000/delete/{id}'
    response = request.delete(api_url)

    if response.status_code == 200:
        print(f'item with id{id} has been deleted')

    else:
        print(f'failed to delete item. status code{response.status_code}')

    return redirect('/')

'''Overall, this view function handles user interaction for creating a new recipe:

It displays a form for users to enter recipe details.
Upon form submission (POST request), it validates the data.
If valid, it saves the data to the database and potentially interacts with an external API.
It displays success or error messages based on the outcome.'''