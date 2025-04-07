from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login 
from apps.accounts.decorators import user_is_not_authenticated
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, Http404
# Create your views here.

@login_required(login_url='/login')
def index(request):
    return render(request,'index.html')

def test(request):
    return render(request, 'test.html')



from django.shortcuts import render
from django.http import Http404

def load_section(request, section_name):
    """
    Carga dinámicamente una sección basada en el nombre proporcionado.
    """
    try:
        # Busca la plantilla en la carpeta section1
        return render(request, f'pages/forms/section1/{section_name}.html')
    except Exception:
        # Si no se encuentra en section1, intenta en section2
        try:
            return render(request, f'pages/forms/section2/{section_name}.html')
        except Exception:
            # Si no se encuentra en ninguna carpeta, lanza un error 404
            raise Http404("Sección no encontrada")

# Log in view
@user_is_not_authenticated
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url =  request.POST.get('next','')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {
                "error":"Incorrect credentials",
            }
            return render(request, 'pages/accounts/login.html',context)
    context = {
        "next":request.GET.get('next', ''),
    }
    return render(request, 'pages/accounts/login.html',context)