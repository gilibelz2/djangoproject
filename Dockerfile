FROM python:3.8.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . /code/
RUN chmod u+x /code/run.sh
CMD ["/code/run.sh"]