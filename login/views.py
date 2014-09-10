# -*- coding: utf-8 -*
import commands
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache, get_cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.importlib import import_module
from django.utils.timezone import timedelta
import io
from login.forms import LoginControlForm, UserForm
from login.models import Session, Log


class UserRestrictMiddleware(object):
    def process_request(self, request):
        """
        Checks if different session exists for user and deletes it.
        """
        if request.user.is_authenticated():
            cache = get_cache('default')
            cache_timeout = 86400
            cache_key = "user_pk_%s_restrict" % request.user.pk
            cache_value = cache.get(cache_key)

            if cache_value is not None:
                if request.session.session_key != cache_value:
                    engine = import_module(settings.SESSION_ENGINE)
                    session = engine.SessionStore(session_key=cache_value)
                    session.delete()
                    cache.set(cache_key, request.session.session_key, 
                              cache_timeout)
            else:
                cache.set(cache_key, request.session.session_key, cache_timeout)
                
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
                userId = request.user.id
                # django methods not recognized, but still working
                listUserId = list(Session.objects.filter(user_id=userId))
                for sessions in listUserId:
                    if (sessions.start == sessions.end):
                        sessions.end = get_time()
                        sessions.save()
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
    # django methods not recognized by eclipse, but still working
    listUserId = list(Session.objects.filter(user_id=userId))
    session = Session.objects.get(idsession=listUserId[-1].idsession)
    session.end = end_time
    session.save()
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

def get_time():
    return timezone.now() - timedelta(hours=3)

@login_required
def login_control(request):
    form = LoginControlForm()
    form.updateForm()
    rendered_page = render(request, 'login_control.html', {'form': form})
    return rendered_page

@login_required
def login_control_generate(request):
    if request.method  == 'POST':
        form = LoginControlForm(request.POST)
        form.updateForm()
        if form.is_valid():
            userId = form.cleaned_data['dropDownUsers']
            month = int(form.cleaned_data['dropDownMonth'])
            year = int(form.cleaned_data['dropDownYear'])
            return createPDF(userId,month,year)
    else:
        return HttpResponseRedirect('/login_control/')


def createPDF(userId,month,year):
    if month == 0 and userId == "all":
        sessions = Log.objects.filter(time__year=year)
    elif int(month) == 0:
        sessions = Log.objects.filter(time__year=year, user_id=userId)
    elif userId == "all":
        sessions = Log.objects.filter(time__year=year, time__month=month)
    else:
        sessions = Log.objects.filter(user_id=userId, time__month=month, time__year=year)
    ids = [int(session.user_id) for session in sessions]
    names = [str(User.objects.get(id=user_id).username) for user_id in ids]
    actions = [session.action for session in sessions]
    times = [session.time for session in sessions]
    sessions = zip(names, actions, times)
    if len(names) != 0:
        name = "login_control"
        t = render_to_string('texFiles/loginControl.tex', Context({'sessions': sessions}))
        l = io.open(name + ".tex", "w", encoding='utf8')
        l.write(t)
        l.close()
        commands.getoutput("pdflatex " + name + ".tex")                              
        commands.getoutput("rm " + name + '.log')
        commands.getoutput("rm " + name + '.aux')
        pdf = file(name + '.pdf').read()
        commands.getoutput("rm " + name + '.tex')
        commands.getoutput("rm " + name + '.pdf')
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-disposition'] = 'attachment; filename=' + name + '.pdf'
        return response
    else:
        return HttpResponse('Não há Log deste usuário neste mês e neste ano.')
    
    
