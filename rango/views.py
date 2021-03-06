from django.shortcuts import render
from rango.models import Tapas
from rango.models import Bares
from rango.forms import TapasForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

def index(request):
    tapas_list = Tapas.objects.order_by('-votos')
    context_dict = {'tapas': tapas_list}

    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)

def reclama_datos(request):
    datos = ()#lista
    votos = []
    lista_tapas = []
    tapas =  Tapas.objects.order_by('-votos')
    for t in tapas:
        lista_tapas.append(t.nombre_tapa)
        votos.append(t.votos)

    datos = lista_tapas, votos
    return JsonResponse(datos, safe=False)

def tapa(request, tapa_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        tapa = Tapas.objects.get(slug=tapa_name_slug)
        context_dict['tapa_name'] = tapa.nombre_tapa
        tapa.votos += 1
        tapa.save()

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        bar = Bares.objects.filter(tapa=tapa)

        # Adds our results list to the template context under name pages.
        context_dict['bar'] = bar
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['tapa'] = tapa
    except Tapas.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/tapa.html', context_dict)

def bar(request, tapa_name_slug, nombre_bar):
    context_dict = {}

    try:
        t = Tapas.objects.get(slug= tapa_name_slug)
        b = Bares.objects.get(nombre_bar = nombre_bar)
        nombretapa =b.tapa.nombre_tapa

        b.n_visitas += 1
        b.save()
        context_dict['nombrebar'] = b.nombre_bar
        context_dict['votos_bar'] = b.n_visitas
        context_dict['bar_direccion'] = b.direccion
        context_dict['bar'] = b

    except Tapas.DoesNotExist:
        pass

    return render(request, 'rango/bar.html', context_dict)


def add_tapa(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = TapasForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = TapasForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_tapa.html', {'form': form})


from rango.forms import BaresForm

def add_bar(request, tapa_name_slug):

    try:
        cat = Tapas.objects.get(slug=tapa_name_slug)
    except Tapas.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = BaresForm(request.POST)
        if form.is_valid():
            if cat:
                bar = form.save(commit=False)
                bar.tapa = cat
                bar.n_visitas = 0
                bar.save()
                # probably better to use a redirect here.
                return tapa(request, tapa_name_slug)
        else:
            print form.errors
    else:
        form = BaresForm()

    context_dict = {'form':form, 'tapa': cat}

    return render(request, 'rango/add_bar.html', context_dict)

from rango.forms import UserForm, UserProfileForm

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

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
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
