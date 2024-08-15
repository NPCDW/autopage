FROM selenium/standalone-chrome

USER root

RUN apt update
RUN apt install -y pip

WORKDIR /autopage
COPY ./ ./
RUN pip3 install -r requirements.txt --break-system-packages

ENTRYPOINT ["python3", "-m"]