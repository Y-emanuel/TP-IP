# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py
# funciones importadas
from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    # guarda las imagenes en la variables.
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
     # retorna la lista con las imagenes.
    return images, favourite_list

# función principal de la galería.
def home(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')

    if search_msg:
        images = services_nasa_image_gallery.getAllImages(search_msg)
    
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})
# si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('index-page')

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

def user_login(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            # Formulario de registro
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                print(f"Nuevo usuario registrado: {username}")  # Mensaje de depuración
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Registro e inicio de sesión exitosos.')
                    return redirect('home')
                else:
                    messages.error(request, 'Error al iniciar sesión después del registro.')
            else:
                print(f"Errores de validación en el formulario de registro: {form.errors}")  # Mensaje de depuración
                messages.error(request, 'Formulario de registro no válido. Por favor, revise los datos ingresados.')
        else:
            # Formulario de inicio de sesión
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                print(f"Inicio de sesión intentado para usuario: {username}")  # Mensaje de depuración
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('home')
                else:
                    messages.error(request, 'Credenciales incorrectas. Inténtelo nuevamente.')
            else:
                print(f"Errores de validación en el formulario de inicio de sesión: {form.errors}")  # Mensaje de depuración
                messages.error(request, 'Formulario de inicio de sesión no válido. Por favor, revise los datos ingresados.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

