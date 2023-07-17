# Basado en la imagen oficial de Python
FROM python:3.9

# Evita que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y instalar
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Django==4.1.6

# Instalar Apache y mod_wsgi
RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi-py3
RUN a2enmod wsgi

# Copiar el código de la aplicación y configuración Apache
COPY . /app/
COPY django-app.conf /etc/apache2/sites-available/
RUN a2ensite django-app.conf
RUN a2dissite 000-default.conf

# Exponer el puerto 80
EXPOSE 80

# Iniciar Apache en segundo plano
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
