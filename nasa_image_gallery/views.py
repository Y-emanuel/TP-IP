# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py
# funciones importadas
from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    # guarda las imagenes en las variables.
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
    # retorna la lista con las imagenes.
    return images, favourite_list

# función principal de la galería.
def home(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    # retorna las imagenes.
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

# función utilizada en el buscador.
def search(request):
    # obtiene la lista de imagenes.
    images, favourite_list = getAllImagesAndFavouriteList(request)
    # envia los datos a la API segun lo solicitado.
    search_msg = request.POST.get('query', '')

    # guarda las imagenes segun la busqueda.
    if search_msg:
        images = services_nasa_image_gallery.getAllImages(search_msg)

    # retorna las imagenes.
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

# si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda

# funcion inicio de sesion.
def inicio_sesion(request):
    # revisa usuario y contraseña.
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            # si el inicio de sesion es valido, muestra un mensaje y lo redirige a la pagina principal.
            if user:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('home')
            # en caso contrario muestra un mensaje de inicio de sesion incorrecto.
            else:
                messages.error(request, 'Credenciales incorrectas. Inténtelo nuevamente.')
        else:
            messages.error(request, 'Formulario de inicio de sesión no válido. Revise los datos ingresados.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

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
