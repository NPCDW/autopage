FROM python

RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN code-server --install-extension MS-CEINTL.vscode-language-pack-zh-hans
RUN code-server --install-extension rust-lang.rust-analyzer
RUN code-server --install-extension tamasfe.even-better-toml
RUN code-server --install-extension fill-labs.dependi
RUN code-server --install-extension njzy.stats-bar
RUN code-server --install-extension Tencent-Cloud.coding-copilot
RUN code-server --install-extension cnbcool.cnb-welcome
RUN code-server --install-extension donjayamanne.githistory

RUN apt-get update && apt-get install -y wget unzip openssh-server git libc++1

# 安装编码
RUN apt-get update
RUN apt-get install -y locales
RUN locale-gen zh_CN.GB18030
RUN locale-gen zh_CN.UTF-8

RUN apt update
RUN apt install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8