FROM python:3.9

WORKDIR /folder

ADD . /folder

RUN pip install -r requirements.txt

EXPOSE 8010

CMD ["python", "-u", "/folder/script.py"]

LABEL MAINTAINER jclemente@prodevelop.es