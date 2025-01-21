# pages/views.py
# Views that will be displayed and a way to connect html views and have a response based on a request

import pickle
import pandas as pd
import pdb

from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

#models.py imports for db.sqlite3
from pages.models import Item, ToDoList

def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'mynumbers':[1,2,3,4,5,6,],
        'firstName': 'Jonathaniel',
        'lastName': 'Alipes'})


#Use this function create a request to the about html page and return and show case its view
def aboutPageView(request):
    return render(request, 'about.html')

def jonathanielPageView(req):
    return render(req, 'jonathaniel.html')

#Handles Post request

def homePost(request):
    # Use request object to extract choice.

    choice = -999
    gmat = -999  # Initialize gmat variable.

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']

        # print("Just before Jonthaniel's breakpoint")
        # # pdb.set_trace()
        # # breakpoint()
        # print("Just after breakpoint")

        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice = int(currentChoice)
        gmat = float(gmatStr)
    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice': choice, 'gmat': gmat}, ))


#Loads pickle files created from logistic regression training of a model
def results(request, choice, gmat):
    print("*** Inside reults()")
    # load saved model
    with open('../model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf._append({'gmat': gmat,
                                             'work_experience': workExperience},
                                            ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat': gmat,
                                            'prediction': singlePrediction})

# views from db.sqlite3
def todos(request):
    print("*** Inside todos()")
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    print(itemErrandDetail[0].todolist.id)
    print(itemErrandDetail)
    return render(request, 'ToDoItems.html',
                {'ToDoItemDetail': itemErrandDetail})



#ADDED DURING LAB 3 Defining Registration page
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import logout

def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('message',
                                                kwargs={'msg': "Your are registered.", 'title': "Success!"}, ))
    # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})

#Added Lab 3
def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title })
#Added Lab 3
def logoutView(request):
    logout(request)
    print("*****  You are logged out.")
    return HttpResponseRedirect(reverse('home' ))
#Added lab 3
def secretArea(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('message',
               kwargs={'msg': "Please login to access this page.",
                       'title': "Login required."}, ))
    return render(request, 'secret.html', {'useremail': request.user.email })
