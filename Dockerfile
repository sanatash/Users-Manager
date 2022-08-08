FROM python:3
WORKDIR /usr/src/app
COPY rest_api.py ./
COPY db_connector.py ./
COPY install_requirements.txt ./
RUN pip install -r install_requirements.txt
#RUN chmod 644 rest_api.py
EXPOSE 5000
CMD ["python3", "rest_api.py", "freedb_user_anat", "RfpG#wf45YrSwWx"]
