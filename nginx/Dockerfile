# Usa la imagen oficial de Nginx
FROM nginx:latest

# Elimina la configuración de Nginx existente
RUN rm /etc/nginx/conf.d/default.conf

# Copia tu archivo de configuración personalizado de Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Expone el puerto 80
EXPOSE 80 443

# Inicia Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]