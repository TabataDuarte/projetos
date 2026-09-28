FROM python:latest
ENV DB_PASSWORD=SenhaForte@2026
ADD http://98.89.0.83/script.sh /tmp/script.sh
RUN apt-get update
RUN apt-get install -y curl vim netcat-openbsd
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD python app/app.py
 
