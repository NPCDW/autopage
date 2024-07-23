FROM selenium/standalone-chrome

RUN apt update
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip3 install -r requirements.txt
