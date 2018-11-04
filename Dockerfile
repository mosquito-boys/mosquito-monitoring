FROM python:3.6-onbuild
COPY . /usr/src/app
CMD ["python", "server.py"]