FROM nginx:1.25

RUN mkdir -p /etc/nginx/ssl
# for static
RUN mkdir -p /app/staticfiles


RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d