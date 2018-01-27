from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, SearchForm
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
import json, requests
import time

def check_login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='/login')
def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #form.save()
            sub = form.cleaned_data.get('subreddit')
            # request.sessions['input'] = sub
            # return redirect('/results')
            return render(request, 'results/top.html', {'top_list': findTop(sub)})
    else:
        form = SearchForm()
    return render(request, 'home/home.html', {'form': form})

# @login_required(login_url='/login')
# def results(request):
#     print(request.sessions.get('input'))
#     return render(request, 'results/top.html', {'top_list': findTop(request.sessions.get('input'))})


def findTop(subreddit):
    # r = requests.get(
    #     'http://www.reddit.com/r/{}.json'.format(subreddit),
    #     headers={'user-agent': 'Mozilla/5.0'}
    # )

    r = requests.get(
        'http://www.reddit.com/r/'+subreddit+'/top.json?sort=top&t=month',
        headers={'user-agent': 'Mozilla/5.0'}
    )

    # view structure of an individual post
    # print(json.dumps(r.json()['data']['children'][0]))

    return_list = []
    for post in r.json()['data']['children']:
        return_list.append(post['data']['title'])
    return return_list

def convertDayEpoch(date): #returns tuple of epoch time with start and end of the day
    #date in format day.month.year
    start_time = date + ' 00:00:00'
    end_time = date + " 23:59:59"
    pattern = '%d.%m.%Y %H:%M:%S'
    start_epoch = int(time.mktime(time.strptime(start_time, pattern)))
    end_epoch = int(time.mktime(time.strptime(end_time, pattern)))
    return (start_epoch, end_epoch)