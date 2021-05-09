# CSCI E-33a <br> Web Programming with Python and JavaScript <br> Harvard Extension School <br>Spring 2021

## Final Project: Timers App

## Description: 

An app that lets users create custom workout timers and pick from a variety of ending sounds or use their own custom sounds!

<i>Note: This app is based off of the skeleton from `project4` so if you see references to `project4` or `network` within the file structure or any urls don't be alarmed. </i>

This app is shipped with the database intact from development and all models migrated. You shouldn't need to do anything fancy to get it running. 
To get started with the app:
```
unzip final.zip
cd final/project4/
python3 manage.py runserver
```
From there you can create a new user and login and begin exploring the app!

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
Timer app is a Django app using SQlite for its database, vanilla JavaScript, and Bootstrap v5.0 on the frontend.

Users can take the following actions:

<b>Register </b>functionality is from the project4 skeleton without changes

<b>Login</b> functionality is from the project4 skeleton without changes

<b>Logout</b> functionality is from the project4 skeleton without changes

<b>Timer</b> functionality was created entirely by me. Users can create a new timer, edit an existing timer, use and view their existing timers, and delete any timer in their account. All functions from above are available via UI elements.

Default sounds are included for use in each timer. Alternatively, users can provide a URL to their own mp3 or wav file. I validate the URL structure but do not check to see if the filetype conforms since `HTML AudioElements` support a large number of codecs. I assume the use of popular filetypes like `WAV` and `mp3`

Originally I had planned on supporting uploads and doing file edits on sounds but that proved to be much larger in scope than anticipated. 

All form validation is done on the frontend using JavaScript. This is because we're using JS to fetch API call results and not actually submitting a form.

In the instance a user tries to submit an incomplete `Timer` form I throw an `alert` with an error message. I chose to not replace the system alert box with anything from Bootstrap since it works so well on mobile. The same is true for the `window.confirm` dialog thrown when a user decides to delete a timer. 

I represent changes in work and rest intervals visually. Originally I had planned to have a beep sound play when an interval was over but the unpredictability of sound playback on mobile had me rethink that decision. 