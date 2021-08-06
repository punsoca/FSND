FROM python:3.7.2-slim

# copy contents of the current directory to the "/app directory
COPY . /app    
# set working directory path
WORKDIR /app   

RUN pip install --upgrade pip
RUN pip install flask

ENTRYPOINT ["python3", "app.py"]