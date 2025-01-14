# pages/views.py
import pickle
import pandas as pd
import pdb

from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

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



