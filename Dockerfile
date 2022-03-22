# base image
FROM python:3.9.10

# the working directory
WORKDIR /usr/src/app

# install dependencies
COPY requirements.txt ./

# install the app
RUN pip install --no-cache-dir -r requirements.txt

# copy everything to the working directory
COPY . .

# the command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]