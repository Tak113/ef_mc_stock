# fetch base image
FROM python:3.8-slim-buster

# change working directory to /usr/app
WORKDIR ./usr/app

# copy dependency list to working directory in docker for following pip ...
# this time we do not copy everything assuming python scripts 
# is updated many times, and those are placed at one line of code
# before last 
COPY requirements.txt ./

# install dependency from requirements.txt
# pip freeze > requirements.txt
RUN pip install -r requirements.txt

# specify port for streamlit, streamlit needs specific port
EXPOSE 8501

# copy the contents of app into a directory called /usr/app in docker
COPY ./ ./

# execute the command when starting the container
CMD ["streamlit", "run", "app_main.py"]