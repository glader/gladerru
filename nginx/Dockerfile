FROM python:3.7 AS backend
WORKDIR /app
ADD requirements.txt /app/requirements.txt
ADD requirements_test.txt /app/requirements_test.txt
RUN pip install -r /app/requirements_test.txt
ADD src /app
RUN python manage.py collectstatic --no-input
RUN cd /app/static/design/3/css && python merge.py

FROM nginx:1.13
RUN rm -v /etc/nginx/nginx.conf
ADD nginx/nginx.conf /etc/nginx/
COPY --from=backend /app/static /app/static

EXPOSE 80
