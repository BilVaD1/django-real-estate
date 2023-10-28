FROM nginx:1.21.3-alpine
# Remove default config
RUN rm /etc/nginx/conf.d/default.conf
# Add our config into docker
COPY ./default.conf /etc/nginx/conf.d/default.conf