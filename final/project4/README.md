# CSCI E-33a <br> Web Programming with Python and JavaScript <br> Harvard Extension School <br>Spring 2021

## Final Project: Timer App

## Description: 

An app that lets users create custom workout timers and pick from a variety of ending sounds or use their own custom sound!

<i>Note: This app is based off of the skeleton from `project4` so if you see references to `project4` or `network` within the file structure or any urls don't be alarmed. </i>

## Models
The app features the base `User` model from Django. I added a `Timer` model which looks like:
```
class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    work_interval = models.IntegerField()
    rest_interval = models.IntegerField()
    repititions = models.IntegerField(default=1)
    sound = models.CharField(max_length=500, null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "work_interval": self.work_interval,
            "rest_interval": self.rest_interval,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
```

## API
The API is a basic REST api that allows for `GET`, `POST`, `PUT` and `DELETE` HTTP methods. Users can create new timers, edit existing timers, and delete timers in their account. The 4 endpoints are:
```
path("timer/new", views.create_new_timer, name="create_new_timer"),
path("timer/<int:timer_id>", views.timer, name="timer"),
path("timer/edit/<int:timer_id>", views.edit_timer),
path("timer/delete/<int:timer_id>", views.delete_timer),
```

## Design choices
Timer app is a Django app using SQlite for its database, vanilla Javascript, and Bootstrap v5.0 on the frontend.

Register

Login

Logout

Timers
    create/edit/delete/view

Default sounds
3 default sounds sourced from:
Originally I had planned on supporting uploads and doing file edits on sounds but that proved to be much larger in scope than anticipated. 

Form validataion
Done on the frontend since we're using JS to fetch API call results and not acutally submitting a form.
Chose to not replace normal alert box with anything from Bootstrap since it works so well on mobile. 

Custom sound support
