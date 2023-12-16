import psycopg2
import os
from django.db import transaction
from django.shortcuts import render, redirect
from .models import User1, Solicitud, Registro
# login-register
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate, update_session_auth_hash
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
import pymysql.cursors
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from .plotly_plot import *
from django.contrib.auth.hashers import make_password
import socket
from django.contrib.contenttypes.models import ContentType
import random

# importaciones para los contadores
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
# last modificacion 19 - 06 - 2023
# conexion bd
conn=psycopg2.connect(host="10.0.1.228", database="dw_essalud", user="postgres", password="AKindOfMagic")
cur=conn.cursor()
cur.execute("SELECT des_men1, pref_user, id_red, cod_red FROM dim_red WHERE id_red <> 32 ORDER BY des_men1  ")
results= cur.fetchall()
df = pd.DataFrame(results, columns=["des_red","pref_user", "id_red", "cod_red"])

# print(df)

cur5=conn.cursor()
cur5.execute("SELECT * FROM dim_sedec ORDER BY des_sed")
results5 = cur5.fetchall()
df5 = pd.DataFrame(results5, columns = ["id_sede", "pre_sed", "des_sed"])
# print("tabla dim sedec")
# print(df5)

# prefijos
cur2=conn.cursor() 
cur2.execute("SELECT pref_user FROM dim_red WHERE id_red <> 32 ")
results2= cur2.fetchall()
df2 = pd.DataFrame(results2, columns=["pref_user"])


# dando formato al dataframe para enviar al template
# dropdown_options = [{'label': i, 'value': i} for i in df['des_red'].unique()]
dropdown_options = [{"label":f"{row['des_red']}", "value": row['id_red']} for _, row in df.iterrows()]
# [{"label":f"{row['des_red']}", "value": row['cod_red']} for _, row in df.iterrows()]

dropdown_options2 = [{'label': i, 'value': i} for i in df2['pref_user']]
# dropdown_options = [{'label': str(row['des_red']) + ' - ' + str(row['des_red']), 'value': str(row['pref_user']) + '_' + str(row['pref_user'])} for index, row in df.iterrows()]

# prefijo de las redes almacenadas en un dropdown
pref_user = [{'label': i, 'value': i} for i in df2['pref_user'].unique()]

# sede_central
# pref_sede = [{'label': i, 'value': i} for i in df5['des_sed'].unique()]
pref_user2 = [{"label":f"{row['des_red']}", "value": row['id_red']} for _, row in df.iterrows()]
pref_sede2 = [{"label": f"{row['des_sed']}", "value": row['pre_sed']} for _, row in df5.iterrows()]

# forma para enviar los 2 datos uno para codigo y descripcion
# pref_sede2 = [{"label": f"{row['des_sed']} ({row['pre_sed']})", "value": row['pre_sed']} for _, row in df5.iterrows()]

# print("pref_sede2")
# print(pref_sede2)

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR,"templates")'
)

# funcion obtener urls
@csrf_exempt
def url_bi(request):
    if request.method == 'POST':
        pattern = json.loads(request.body)['pattern']
        conn3 = psycopg2.connect(host = "localhost", database = "sig_ugad", user = "postgres", password = "AKindOfMagic")
        cur6 = conn3.cursor()
        # cur6.execute("SELECT COUNT(*) FROM public.auth_user WHERE username LIKE 'ugad%' ")
        cur6.execute("SELECT url_bi FROM panel_powerbi WHERE stat = 1 AND template_view = %s",
        (pattern,))
        # cur6.execute("SELECT url_bi FROM panel_powerbi WHERE template_view = 'pacientes_diabetes' ")
        count1 = cur6.fetchone()
        url = count1[0]
        print(url)
        return JsonResponse({'data': url})
    else:
        return JsonResponse({'error': 'Error al obtener URL'}, status = 405)
# FIN funcion obtener urls

# funcion para obtener los contadores
@csrf_exempt
def count_users_by_pattern(request):
    if request.method == 'POST':
        pattern = json.loads(request.body)['pattern']
        conn3=psycopg2.connect(host="localhost", database="sig_ugad", user="postgres", password="AKindOfMagic")
        cur6=conn3.cursor()
        # cur6.execute("SELECT COUNT(*) FROM public.auth_user WHERE username LIKE 'ugad%' ")
        cur6.execute("SELECT COUNT(*) FROM public.auth_user WHERE username LIKE %s",
        (pattern + '%',))
        count1 = cur6.fetchone()
        count = count1[0]
        # print(count)
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status = 405)


@csrf_exempt
def filtro_status(request):
    if request.method == 'POST':
        est_soli = json.loads(request.body)['pattern']
        conn = psycopg2.connect(host = "localhost", database = "sig_ugad", user = "postgres", password = "AKindOfMagic")
        cur = conn.cursor()
        cur.execute("SELECT * FROM panel_solicitud WHERE estado_soli = %s", (est_soli,))
        data = cur.fetchall()
        return JsonResponse({'solicitud_opcion': data})
    else:
        return JsonResponse({'error': 'Query incorrecta'}, status = 405)


@csrf_exempt
def update_estado_soli(request):
    if request.method == 'POST':
        id_soli = json.loads(request.body)['id']
        estado_soli = json.loads(request.body)['estado_soli']
        # actualizacion de estado_soli
        Solicitud.objects.filter(id=id_soli).update(estado_soli = estado_soli)
        return JsonResponse({'rpta': True})
    else:
        return JsonResponse({'error': 'Fallo al actualzar'}, status = 405)

# CRUD django_content_type
# @login_required
# def view_content_type(request):  #read models
#     content_types = ContentType.objects.all().order_by('-id').all()
#     print(content_types)
#     return render(request, 'content_type.html', {'content_type': content_types})

# @csrf_exempt
# def count_content_type(request): #conteo de models
#     if request.method == 'GET':
#         conn=psycopg2.connect(host="localhost", database="sig_ugad_bk_users", user="postgres", password="root")
#         cur = conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM django_content_type")
#         count = cur.fetchone()
#         count_number = count[0]
#         print(count_number)
#         return JsonResponse({'count': count_number})
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status = 405)

# @login_required
# def new_content_type(request): # create new model
#     if request.method == 'POST':
#         id_content = request.POST.get('number_content')
#         app_label = request.POST.get('app_label')
#         type_model = request.POST.get('type_model')
#         content_type = ContentType.objects.create(id = id_content, app_label = app_label, model = type_model)
#         content_type.save()
#         return redirect('view_content_type')

# @login_required
# def uodate_content_type(request):    #actualizar content_type
#     if request.method == 'POST':
#         id = json.loads(request.body)['id_content']
#         app = json.loads(request.body)['app_label']
#         model = json.loads(request.body)['model']
#         ContentType.objects.filter(id = id).update(app_label = app, model = model)
#         return JsonResponse({'rpta': True})
#     else:
#         return JsonResponse({'error': 'Fallo al actualizar'}, status = 405)

# @login_required
# @permission_required('panel.delete_user', login_url='vista_usuarios')
# def delete_content_type(request): #delete content_type
#     if request.method == 'POST':
#         id = json.loads(request.body)['id_label']
#         content_type = ContentType.objects.get(id=id)
#         content_type.delete()
#         return JsonResponse({'rpta': True})
#     else:
#         return JsonResponse({'error': 'Fallo al eliminar'}, status = 405)

# @login_required
# def obtener_content(request): # Obtener datos de content por ID
#     conn=psycopg2.connect(host="localhost", database="sig_ugad_bk_users", user="postgres", password="root")
#     if request.method == 'POST':
#         id_content = json.loads(request.body)['id_content']
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM public.django_content_type WHERE id = %s", (id_content,))
#         data = cur.fetchall()
#         data_list = []
#         for row in data:
#             data_dict = {'id': row[0], 'app_label': row[1], 'model': row[2]}  # Reemplaza los campos 'id', 'name', ... con los nombres correctos de las columnas en tu tabla
#             data_list.append(data_dict)
#         return JsonResponse({'data': data_list})
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status = 405)

# FIN CRUD django_content_type

@csrf_exempt
def count_users_by_pattern2(request):
    conn3=psycopg2.connect(host="localhost", database="sig_ugad", user="postgres", password="AKindOfMagic")
    conn4=psycopg2.connect(host="10.0.1.228", database="dw_essalud", user="postgres", password="AKindOfMagic")
    if request.method == 'POST':
        pattern = json.loads(request.body)['pattern']
        cur7=conn4.cursor()
        # cur6.execute("SELECT COUNT(*) FROM public.auth_user WHERE username LIKE 'ugad%' ")
        cur7.execute("SELECT pref_user FROM dim_red WHERE id_red = %s",
        (pattern,))
        count1 = cur7.fetchone()
        count2 = count1[0]
        count = count2.strip()
        # print('pref_user')
        # print(count)

        cur9=conn4.cursor()
        cur9.execute("SELECT des_red FROM dim_red WHERE id_red = %s",
        (pattern,))
        count4 = cur9.fetchone()
        count6 = count4[0]
        # print('des_red')
        # print(count6)

        # contador de usuarios
        cur8=conn3.cursor()
        # cur6.execute("SELECT COUNT(*) FROM public.auth_user WHERE username LIKE 'ugad%' ")
        cur8.execute("SELECT COUNT(*) FROM public.auth_user WHERE username LIKE %s",
        (count.lower() + '%',))
        count3 = cur8.fetchone()
        count2 = count3[0]
        # print('count')
        # print(count2)

        return JsonResponse({'count': count, 'count2': count2, 'count6': count6})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status = 405)
        
def redirect_if_authenticated(view_func):
    @user_passes_test(lambda user: not user.is_authenticated, login_url='index')
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapped_view

@login_required(login_url='login')
def roles(request):
   return render(request, 'roles.html')

@login_required(login_url='login')
def programacion(request):
    if 'DJANGO_SETTINGS_MODULE' in os.environ and 'production' in os.environ['DJANGO_SETTINGS_MODULE']:
        ip1 = socket.gethostbyname(socket.gethostname())
    else:
        ip1 = request.META['REMOTE_ADDR']
    # print(ip1)
    
    hostname1 = socket.gethostname()
    ip1 = request.META['REMOTE_ADDR']
    # ip1 = socket.gethostbyname(hostname1)    
    ip1 = format(ip1)
    url1 = reverse('programacion')
    username1 = request.user.username
    nuevo_registro1 = Registro( ip = ip1, usuario = username1, url = url1)
    nuevo_registro1.save()

    return render(request, 'programacion_asistencial.html')

@login_required(login_url='login')
def tables(request):
   return render(request, 'form-row-separator.html')

# funcion corresponde a solicitudes.html
@login_required(login_url='login')
def view_solicitud(request):
    hostname1 = socket.gethostname()
    ip1 = request.META['REMOTE_ADDR']
    # ip1 = socket.gethostbyname(hostname1)    
    ip1 = format(ip1)
    url1 = reverse('view_solicitud')
    username1 = request.user.username
    nuevo_registro1 = Registro( ip = ip1, usuario = username1, url = url1)
    nuevo_registro1.save()
    solicitud = Solicitud.objects.all()
    tp_estados = Solicitud.objects.values_list('estado_soli', flat=True)     

    # for tp_estado in tp_estados:
    #    print(tp_estado)
    #    if tp_estado == '1':
    #     estado = '<span class="badge text-bg-primary">Primary</span>'
    #     break     
    return render(request, "solicitudes.html", {'solicitud': solicitud, 'pref_user': pref_user2, 'pref_sede2': pref_sede2})

# datos acceso
def datos_registro(request):
   return render(request, 'registro_datos.html',{'dropdown_options': pref_user2})

@login_required(login_url='login')
def index(request):
   return render(request, 'prestaciones_salud.html')
#    return render(request, 'index.html')

# prestaciones  
@login_required(login_url='login')
def prestaciones(request):
    hostname1 = socket.gethostname()
    # ip1 = socket.gethostbyname(hostname1)   
    ip1 = request.META['REMOTE_ADDR'] 
    ip1 = format(ip1)
    url1 = reverse('prestaciones')
    username1 = request.user.username
    nuevo_registro1 = Registro( ip = ip1, usuario = username1, url = url1)
    nuevo_registro1.save()    
    return render(request, 'prestaciones_salud.html')

# servicio de emergencia   
@login_required(login_url='login')
def servicio_emergencia(request):
    hostname1 = socket.gethostname()
    # ip1 = socket.gethostbyname(hostname1)
    ip1 = request.META['REMOTE_ADDR']    
    ip1 = format(ip1)
    url1 = reverse('servicio_emergencia')
    username1 = request.user.username
    nuevo_registro1 = Registro( ip = ip1, usuario = username1, url = url1)
    nuevo_registro1.save()    
    
    return render(request, 'servicio_emergencia.html')

# servicio de emergencia   
@login_required(login_url='login')
def index_new(request):
   return render(request, 'index_second.html')

@login_required(login_url='login')
def userView(request):
    # print('vista de usuarios')
    hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)  
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('userView')
    username = request.user.username
   
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()

    users = User.objects.all()
    return render(request, "usuarios_view.html", {'users': users, 'ip': ip,'url': url})

# Tabla
# Solicitudes
@login_required(login_url='login')
def solicitudView(request):
    # print('vista de solicitudes')
    hostname1 = socket.gethostname()
    # ip1 = socket.gethostbyname(hostname1)
    ip1 = request.META['REMOTE_ADDR']    
    ip1 = format(ip1)
    url1 = reverse('solicitudView')
    username1 = request.user.username
    # print('username')
    # print(username1)
    # guardar en tabla registro
    nuevo_registro1 = Registro( ip = ip1, usuario = username1, url = url1)
    nuevo_registro1.save()

    solicitud = Solicitud.objects.all()
    return render(request, "solicitudes.html", {'solicitud': solicitud, 'ip': ip1, 'url': url1})

@login_required(login_url='login')
def lock_account(request):
    # user=request.user
    # user.is_active = False
    return render(request, "lock_account.html")

@login_required(login_url='lock')
def unlock_account(request):
    # logout(request)
    user = request.user
    user.is_active = False
    if request.method == 'GET':
        return render(request, 'lock_account.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['email'], password=request.POST['password'])
        # print(request.POST)
        if user is None:
            return render(request, 'lock_account.html', {
                'form': AuthenticationForm,
                'error': 'Contraseña incorrecta'
            })
        else:
            auth_login(request,user)
            return redirect('index')

@login_required(login_url='login')
# @permission_required('panel.view_user', login_url='index')
def UserListView(request):    
    users = User.objects.all()
    return render(request, "usuarios_view.html", {'users': users})

# funcion crear

@login_required(login_url='login')
@permission_required('panel.add_user', login_url='index')
def CreateUserView(request):
    user = User(username = request.POST['username'], first_name = request.POST['nombres'],last_name = request.POST['apellidos'], email = request.POST['correo'], password = request.POST['password'])
    user.save()
    return redirect('vista_usuarios')

# vista

@login_required(login_url='login')
@permission_required('panel.add_user', login_url='vista_usuarios')
def VistaCreateUserView(request):
    return render(request, 'register.html', {'pref_sede2': pref_sede2, 'dropdown_options': dropdown_options})

# funcion eliminar

@login_required(login_url='login')
@permission_required('panel.delete_user', login_url='vista_usuarios')
def DeleteUserView(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id_user']
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse({'rpta': True})
        # return redirect('vista_usuarios')
    else:
        return JsonResponse({'error': 'Fallo al eliminar'}, status = 405)
        # return redirect('vista_usuarios')

@login_required(login_url='login')
@permission_required('panel.change_user', login_url='vista_usuarios')
def EditUserView(request, id):
    user = User.objects.get(id=id)
    # print(user)
    return render(request, 'usuario_update.html', {'user': user})

@login_required(login_url='login')
def EditUserView2(request, id):
    user = User.objects.get(id=id)
    # print(user)
    return render(request, 'usuario_update2.html', {'user': user})

@login_required(login_url='login')
@permission_required('panel.change_user', login_url='vista_usuarios')
def UpdateUserView(request, id):
    password = make_password(request.POST['password'])
    User.objects.filter(id=id).update(username=request.POST['username'], first_name = request.POST['nombres'], last_name=request.POST['apellidos'], email = request.POST['correo'], password=password)
    return render(request, 'usuarios_view.html')

@login_required(login_url='login')
def UpdateUserView2(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.username=request.POST['username'] 
        user.first_name=request.POST['nombres']
        user.last_name=request.POST['apellidos'] 
        user.email=request.POST['correo'] 
        password=request.POST['password']
        if password:
            user.password=make_password(password)
            update_session_auth_hash(request, user)
        user.save()
        return redirect('index')

# funcion solicitud
# with transaction.atomic():

@login_required(login_url='login')
def registra_new_user(request):
    if request.method == 'POST':
        estado_soli = '2'
        cod_arch = 'n'
        id_soli = request.POST.get('id_modal')
        nombres = request.POST.get('nombre_modal')
        apellido = request.POST.get('apellido_modal')
        correo = request.POST.get('correo_modal')
        usuario = request.POST.get('username_modal')
        name_sede = request.POST.get('name_sede_modal')
        
        if( name_sede == 'SEDE CENTRAL' ):
            prefijo = request.POST.get('pref2')
        else:
            prefijo = request.POST.get('pref')

        password = request.POST.get('password1_modal')
        new_user = usuario.lower()
        dni = request.POST.get('doc_ide_modal')
        tel = request.POST.get('tel_cont_modal')
        anexo = request.POST.get('anexo_sede_modal')
        id_red = request.POST.get('id_modal')
        # Actualizar tabla solicitudes
        Solicitud.objects.filter(id=id_soli).update(estado_soli = estado_soli, cod_arch = cod_arch)
        # guarda en tabla panel_user
        panel_user = User1(nombreusuario = new_user, nombres = nombres, apellidos = apellido, correo = correo, password = password, doc_ide = dni, telefono_contacto = tel, anexo = anexo, id_red = id_red )
        panel_user.save()
        # print(new_user)
        nuevo_user = User.objects.create_user( username = new_user, first_name = nombres, last_name = apellido, email = correo, password = password )
        nuevo_user.save()

    return redirect('vista_usuarios')
    


def solicitud(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        if Solicitud.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, utilice otro.')
            return render(request, 'login.html', {'error': 'El correo electrónico ya está registrado. Por favor, utilice otro.'})
        else:
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            dni = request.POST.get('dni')
            telefono_contacto = request.POST.get('telefono')
            anexo = request.POST.get('anexo')
            red = request.POST.get('red')
            area = request.POST.get('area')
            estado_soli = '1'
            cod_arch = 's'
            # Crear una nueva instancia de Solicitud con los valores de los campos
            nueva_solicitud = Solicitud(nombres = nombres, apellidos = apellidos, correo = correo, dni = dni, telefono_contacto = telefono_contacto, anexo = anexo, red = red, area = area, estado_soli = estado_soli, cod_arch = cod_arch)
            # Guardar la instancia de Solicitud en la base de datos
            nueva_solicitud.save()
            # mensaje de registro de solicitud
            messages.success(request, 'Solicitud enviada. ¡Gracias!')
            # Redireccionar al usuario a la página de inicio de sesión
            return redirect('login')
    # Si el método de solicitud no es POST, mostrar la página de solicitud de nuevo
    return render(request, 'solicitud.html')

# DASHBOARD

@login_required(login_url='login')
@permission_required('django_plotly_dash.view_dashapp', login_url='index')
def dash(request):
    return render(request, 'dash.html')

@login_required(login_url='login')
def alta_direccion(request):
    # hostname1 = socket.gethostname()
    ip1 = request.META['REMOTE_ADDR']   
    ip1 = format(ip1)
    url1 = reverse('alta_direccion')
    username1 = request.user.username
    nuevo_registro1 = Registro( ip = ip1, usuario = username1, url = url1)
    nuevo_registro1.save()    

    return render(request, 'alta_direccion.html')

@login_required(login_url='login')
@permission_required('django_plotly_dash.view_dashapp',login_url='index')
def dashinteractive(request):
    return render(request,'dashinteractive.html')

@login_required(login_url='login')
@permission_required('django_plotly_dash.view_dashapp',login_url='index')
def dashreporte(request):
    return render(request,'dashreporte.html')

@login_required(login_url='login')
@permission_required('django_plotly_dash.view_dashapp',login_url='index')
def dashtwo(request):
    return render(request,'dash_two.html')

@login_required(login_url='login')
@permission_required('django_plotly_dash.view_dashapp', login_url='index')
def dashthree(request):
    return render(request,'dash_three.html')

@login_required(login_url='login')
@permission_required('django_plotly_dash.view_dashapp', login_url='index')
def dashfour(request):
    return render(request,'dash_four.html')

# Register

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'].lower(), password=request.POST['password1'], first_name=request.POST['nombres'], last_name=request.POST['apellidos'], email=request.POST['correo'] )
                user.save()
                # auth_login(request,user)
                return redirect('vista_usuarios')
            except IntegrityError:
                return render(request, 'login.html', {'form': UserCreationForm, 'error': 'Usuario ya existe'})

        return render(request, 'login.html', {'form': UserCreationForm, 'error': 'Password no coinciden'})

@redirect_if_authenticated
def login(request):
    ip1 = request.META['REMOTE_ADDR']    
    ip1 = format(ip1)
    url1 = 'login'
    nuevo_registro1 = Registro( ip = ip1, url = url1)
    nuevo_registro1.save()
        
    # print("imprimiendo ip: {0}".format(ip))    
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['email'].lower(), password=request.POST['password'])
        # print(request.POST)
        if user is None:
            messages.error(request, 'Nombre de usuario o contraseña es incorrecto')
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Nombre de usuario o contraseña es incorrecto'
            })
        else:
            auth_login(request,user)
            return redirect('prestaciones')

def signout(request):
    logout(request)
    return redirect('login')


# new login

def authentication_login(request):
    return render(request,'authentication-login3.html')

@login_required(login_url='login')
def emergencia_second(request):
    return render(request, 'servicio_emergencia2.html')

@login_required(login_url='login')
def dashinteractive(request):
    return render(request,'dashinteractive.html')

# funciones para bienes estrategicos
@login_required(login_url='login')
def monitoreo_abastecimiento(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('monitoreo_abastecimiento')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'bienes_estrategicos/monitoreo_abastecimiento.html')

@login_required(login_url='login')
def canal_distribucion(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('canal_distribucion')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'bienes_estrategicos/canal_distribucion.html')

@login_required(login_url='login')
def carga_consumo(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('carga_consumo')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'bienes_estrategicos/carga_consumo.html')

# funciones para prestaciones economicas
@login_required(login_url='login')
def aporte_asegurados(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('aporte_asegurados')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/aporte_asegurados.html')

@login_required(login_url='login')
def certificado_incapacidad(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('certificado_incapacidad')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/certificado_incapacidad.html')

@login_required(login_url='login')
def pacientes_cronicos(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('pacientes_cronicos')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/pacientes_cronicos.html')

@login_required(login_url='login')
def poblacion_asegurada(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('poblacion_asegurada')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/poblacion_asegurada.html')

@login_required(login_url='login')
def seguro_accidentes(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('seguro_accidentes')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/seguro_accidentes.html')

@login_required(login_url='login')
def seguro_complementario(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('seguro_complementario')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/seguro_complementario.html')

@login_required(login_url='login')
def subsidios_procesados(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('subsidios_procesados')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/subsidios_procesados.html')

# funciones para prestaciones essalud
@login_required(login_url='login')
def pacientes_diabetes(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('pacientes_diabetes')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_essalud/pacientes_diabetes.html')

@login_required(login_url='login')
def pacientes_hipertension(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('pacientes_hipertension')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_essalud/pacientes_hipertension.html')

@login_required(login_url='login')
def pacientes_its(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('pacientes_its')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_essalud/pacientes_its.html')

@login_required(login_url = 'login')
def dengue(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('dengue')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_essalud/dengue.html')

@login_required(login_url = 'login')
def indicadores_salud_renal(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('indicadores_salud_renal')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'salud_renal/indicadores_salud_renal.html')

@login_required(login_url = 'login')
def indicadores_fonafe(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('fonafe')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'fonafe/indicadores_fonafe.html')
    
@login_required(login_url = 'login')
def subsidios_otorgados(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('subsidios_otorgados')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/subsidios_otorgados.html')

@login_required(login_url = 'login')
def analisis_financiero(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('analisis_financiero')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'prestaciones_economicas/analisis_financiero.html')

@login_required(login_url = 'login')
def mi_consulta(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('mi_consulta')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'mi_consulta/mi_consulta.html')

@login_required(login_url = 'login')
def fenomeno_del_nino(request):
    ip1 = request.META['REMOTE_ADDR']  
    ip = format(ip1)  
    url = reverse('fenomeno_del_nino')
    username = request.user.username
    # guardar en tabla registro
    nuevo_registro = Registro( ip = ip, usuario = username, url = url)
    nuevo_registro.save()
    return render(request,'fenomeno_del_nino/fenomeno_del_nino.html')