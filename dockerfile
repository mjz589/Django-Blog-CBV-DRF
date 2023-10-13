# pull the official base image
FROM python:3.10

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



# Install Python dependencies
RUN pip3 install --upgrade pip 
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt


# copy project
COPY ./core /app

EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]