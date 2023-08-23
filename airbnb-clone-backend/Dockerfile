FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get -y install vim
# 컨테이너 내에서 코드가 실행될 경로 설정
RUN mkdir /app
WORKDIR /app

# # requirements.txt에 명시된 필요한 packages 설치
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Project를 /usr/src/app으로 복사
COPY . ./ 


