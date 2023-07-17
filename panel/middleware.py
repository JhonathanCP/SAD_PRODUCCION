from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect

class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario está autenticado y tiene una sesión activa
        if request.user.is_authenticated and 'last_activity' in request.session:
            last_activity_str = request.session['last_activity']
            # Convertir la cadena en formato ISO 8601 a un objeto datetime
            last_activity = datetime.fromisoformat(last_activity_str)
            # Calcular el tiempo de inactividad permitido
            idle_timeout = timedelta(seconds=settings.SESSION_IDLE_TIMEOUT)
            if datetime.now() - last_activity > idle_timeout:
                # Cerrar la sesión del usuario
                auth.logout(request)
                return redirect(settings.LOGOUT_REDIRECT_URL)

        response = self.get_response(request)

        # Actualizar la marca de tiempo de la última actividad en cada solicitud
        if request.user.is_authenticated:
            # Convertir el objeto datetime a una cadena en formato ISO 8601
            last_activity_str = datetime.now().isoformat()
            request.session['last_activity'] = last_activity_str
            print("cerrar")

        return response