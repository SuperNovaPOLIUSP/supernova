from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from login.forms import UserForm
from login.models import Session
from django.utils.timezone import timedelta


def register(request):
    # Need an user in database to register a new user.
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 
            'register.html',
            {'user_form': user_form, 'registered': registered})

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                start_time = get_time()
                start = Session(start=start_time, user=user, end=start_time)
                start.save()
                return HttpResponseRedirect('/index/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Supernova account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})



# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    end_time = get_time()
    userId = request.user.id
    # django methods not recognized, but still working
    listUserId = list(Session.objects.filter(user_id=userId))
    session = Session.objects.get(idsession=listUserId[-1].idsession)
    session.end = end_time
    session.save()
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

def get_time():
    return timezone.now() - timedelta(hours=3)

