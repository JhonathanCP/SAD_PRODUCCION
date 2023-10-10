from django.contrib import admin
from django.urls import path


from .views import index, UserListView,CreateUserView, VistaCreateUserView, DeleteUserView, EditUserView,EditUserView2, UpdateUserView,dash,register,login,signout,dashinteractive,dashreporte,authentication_login,dashtwo,dashthree,dashfour, UpdateUserView2, lock_account,unlock_account,userView, roles, prestaciones, servicio_emergencia,index_new, datos_registro, solicitud, view_solicitud, solicitudView, registra_new_user, emergencia_second, tables, programacion, alta_direccion, count_users_by_pattern, count_users_by_pattern2,update_estado_soli,monitoreo_abastecimiento,canal_distribucion,carga_consumo,aporte_asegurados,certificado_incapacidad,pacientes_cronicos,poblacion_asegurada,seguro_accidentes,seguro_complementario,subsidios_procesados,pacientes_diabetes,pacientes_hipertension,pacientes_its,filtro_status, url_bi, dengue, indicadores_salud_renal, indicadores_fonafe, subsidios_otorgados,analisis_financiero

from panel.dash_apps.finished_apps import simpleexample,pruebacadena,barraprueba,grafico,reporte,grafico2,pruebacallback,reportesalud,ventas,practica

# from panel.dash_apps.finished_apps import simpleexample
    
urlpatterns=[
    path('',login,name='login'),
    path('login/',authentication_login,name="authentication-login"),
    path('panel/',index, name="index"),
    path('usuarios/',UserListView, name='vista_usuarios'),
    path('usuario/crear/', CreateUserView, name='create_usuarios'),
    path('usuarios/crear/', VistaCreateUserView, name='crear_usuario'),
    path('usuarios/delete/',DeleteUserView, name='eliminar_usuario'),    
    path('usuarios/editar/<int:id>',EditUserView, 
    name='edit_user'),
    path('usuarios2/editar/<int:id>',EditUserView2, 
    name='edit_user2'),
    path('user/editar/<int:id>',UpdateUserView, name='update_user'),    
    path('user2/editar/<int:id>',UpdateUserView2, name='update_user2'),    
    path('dash/', dash, name="dash"),
    path('dash/interactivo/',dashinteractive,name="dashinteractivo"),
    path('dash/reporte/',dashreporte,name="dashreporte"),
    path('dash/two/',dashtwo,name="dash_two"),
    path('dash/three/',dashthree,name='dash_three'),
    path('dash/four/',dashfour,name="dashfour"),
    path('register/',register,name='register'),
    path('logout/',signout,name='logout'),   
    path('lock_account/',lock_account,name='lock'),   
    path('unlock/',unlock_account,name='unlock'),
    path('userview/',userView,name='userView'),
    path('roles/',roles,name='roles'),
    path('prestaciones/',prestaciones,name='prestaciones'),
    path('servicio_emergencia/',servicio_emergencia,name='servicio_emergencia'),
    path('index_new/',index_new,name='index_new'),
    path('datos_registro/',datos_registro,name='datos_registro'),
    path('registrar/',solicitud,name='solicitud'),
    path('solicitudes/',view_solicitud,name='view_solicitud'),
    path('registro_nuevo/',registra_new_user,name='registra_new_user'),
    path('emergencia2/', emergencia_second, name='emergencia2'),
    path('dash/interactivo/',dashinteractive,name="dashinteractivo"),
    path('tables/',tables,name="tables"),
    path('programacion/',programacion,name="programacion"),
    path('altadireccion/',alta_direccion,name="alta_direccion"),
    path('count_users_by_pattern/',count_users_by_pattern,name="count_users_by_pattern"),
    path('filtro_status/', filtro_status, name = "filtro_status"), #filtro para select de status
    path('url_bi/', url_bi, name = "url_bi"), #filtro para select de status
    path('count_users_by_pattern2/',count_users_by_pattern2,name="count_users_by_pattern2"),
    path('update_estado/',update_estado_soli,name="update_estado_soli"),
    # path('view_content_type/',view_content_type,name="view_content_type"),  #content_type vista
    # path('count_content_type/',count_content_type,name="count_content_type"), #content_type conteo
    # path('new_content_type/',new_content_type,name="new_content_type"), #content_type crear
    # path('app_label/delete/',delete_content_type,name="delete_content_type"), #content_type delete
    # path('set/content/',obtener_content,name="obtener_content"), #content_type obtener por id
    # path('update/content/',uodate_content_type,name="update_content_type"), #content_type update
    #funciones bienes estrategicos
    path('monitoreo_abastecimiento/',monitoreo_abastecimiento,name="monitoreo_abastecimiento"),
    path('canal_distribucion/',canal_distribucion,name="canal_distribucion"),
    path('carga_consumo/',carga_consumo,name="carga_consumo"),

    #funciones prestaciones economicas
    path('aporte_asegurados/',aporte_asegurados,name="aporte_asegurados"),
    path('certificado_incapacidad/',certificado_incapacidad,name="certificado_incapacidad"),
    path('pacientes_cronicos/',pacientes_cronicos,name="pacientes_cronicos"),
    path('poblacion_asegurada/',poblacion_asegurada,name="poblacion_asegurada"),
    path('seguro_accidentes/',seguro_accidentes,name="seguro_accidentes"),
    path('seguro_complementario/',seguro_complementario,name="seguro_complementario"),
    path('subsidios_procesados/',subsidios_procesados,name="subsidios_procesados"),
    path('subsidios_otorgados/', subsidios_otorgados, name = "subsidios_otorgados"),
    path('analisis_financiero/', analisis_financiero, name = "analisis_financiero"),
    
    # salud renal
    path('indicadores_salud_renal/', indicadores_salud_renal, name = "indicadores_salud_renal"),

    #funciones prestaciones essalud
    path('pacientes_diabetes/',pacientes_diabetes,name="pacientes_diabetes"),
    path('pacientes_its/',pacientes_its,name="pacientes_its"),
    path('pacientes_hipertension/',pacientes_hipertension,name="pacientes_hipertension"),
    path('dengue/', dengue, name = "dengue"),
    
    # fonafe
    path('indicadores_fonafe/', indicadores_fonafe, name = "fonafe"), # indocadores fonafe



    ]
