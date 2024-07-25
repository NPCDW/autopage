FROM selenium/standalone-chrome

USER root

RUN apt update
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

WORKDIR /autopage
COPY ./ ./
RUN pip3 install -r requirements.txt

ENTRYPOINT python3