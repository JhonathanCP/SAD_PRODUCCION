# Usa la imagen oficial de Python 3.12
FROM python:3.9
# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia los archivos de requerimientos y el código fuente
COPY requirements.txt ./
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
#PRUEBA
#RUN python manage.py collectstatic --noinput

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "admin.wsgi:application", "--bind", "0.0.0.0:8000"]
