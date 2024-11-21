FROM python

USER root

# 安装编码
RUN apt-get update
RUN apt-get install -y locales
RUN locale-gen zh_CN.GB18030
RUN locale-gen zh_CN.UTF-8

RUN apt update
RUN apt install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

WORKDIR /autopage
COPY ./ ./
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m"]