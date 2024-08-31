FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]

# $ sudo docker image build --file Dockerfile --tag basic-streamlit-app:v1 .
# $ sudo docker container run -itd --publish 8501:8501 basic-streamlit-app:v1     
# $ curl localhost:8501
# $ curl <PUBLIC_IP>:8501      # running this from another host will also work. make local firewall allow this port first.

