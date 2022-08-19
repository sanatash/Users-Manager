FROM python:3
WORKDIR /usr/src/app
COPY docker_backend_testing.py ./
COPY db_docker_connector.py ./
COPY mysql.env ./
COPY install_requirements.txt ./
RUN pip install -r install_requirements.txt
#RUN chmod 644 rest_api_docker.py
CMD ["sh", "-c", "sleep 20s ; python3 ./docker_backend_testing.py"]