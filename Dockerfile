FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV DATABASE_URL='postgres://vydiayewoxybgi:2927a1e85eb61d327df37dc3bd0471af8c24ea73b59e9366e5cbcc96b0994a00@ec2-54-83-33-213.compute-1.amazonaws.com:5432/d8dqi8siqhpg1j'
ENV SECRET_KEY="b'\x8a\xd1D~\x11\xaf\xa8\xa4\xfe\t\xf0j\x82\xb0\xdaS5\xa1\x18\xec\xdeS\x8b5'"
ENV FLASK_APP="application.py"
ENTRYPOINT ["python3"]
CMD ["application.py"]
