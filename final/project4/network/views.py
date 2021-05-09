from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User, Timer, Profile
import json


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def index(request):
    if request.user.is_authenticated:
        timers = Timer.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'network/index.html', {'timers': timers})
    return render(request, 'network/index.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def create_new_timer(request):
    if request.method == "POST":
        # grab data from request
        timer_data = json.loads(request.body)
        title = timer_data.get("title")
        work_interval = timer_data.get("work_interval")
        rest_interval = timer_data.get("rest_interval")
        repititions = timer_data.get("repititions")
        sound = timer_data.get("sound")

        # create and save new timer
        obj = Timer()
        obj.title = title
        obj.work_interval = work_interval
        obj.rest_interval = rest_interval
        obj.user = request.user
        obj.repititions = repititions
        obj.sound = sound
        obj.save()

        context = {
            'msg': 'success',
            't': 'saved',
        }
        return JsonResponse(context, status=201)
    return render(request, "network/create_new_timer.html")


@login_required
def timer(request, timer_id):
    try:
        timer = Timer.objects.get(user=request.user, id=timer_id)
    except Timer.DoesNotExist:
        return JsonResponse({"error": "Timer not found."}, status=404)

    # Return timer data
    if request.method == "GET":
        context = {
            'timer': timer,
        }
        return render(request, "network/timer.html", context)


@login_required
@csrf_exempt
def edit_timer(request, timer_id):
    try:
        timer = Timer.objects.get(user=request.user, id=timer_id)
    except Timer.DoesNotExist:
        return JsonResponse({"error": "Timer not found."}, status=404)

    if request.method == "PUT":
        # grab data from request
        timer_data = json.loads(request.body)
        title = timer_data.get("title")
        work_interval = timer_data.get("work_interval")
        rest_interval = timer_data.get("rest_interval")
        repititions = timer_data.get("repititions")
        sound = timer_data.get("sound")

        # update and save timer
        timer.title = title
        timer.work_interval = work_interval
        timer.rest_interval = rest_interval
        timer.repititions = repititions
        timer.sound = sound
        timer.save()

        context = {
            'msg': 'success',
            't': 'saved',
        }
        return JsonResponse(context, status=201)
    if request.method == "GET":
        context = {
            'timer': timer,
        }
    return render(request, "network/edit_timer.html", context)


@login_required
@csrf_exempt
def delete_timer(request, timer_id):
    try:
        timer = Timer.objects.filter(user=request.user, id=timer_id)
    except Timer.DoesNotExist:
        return JsonResponse({"error": "Timer not found."}, status=404)
    if request.method == "DELETE":
        timer.delete()
        context = {
            'msg': 'success',
            't': 'saved',
        }
        return JsonResponse(context, status=201)
    return render(request, 'network/index.html')
