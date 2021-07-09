FROM ubuntu:18.04
MAINTAINER DploY707 <starj1024@gmail.com>
MAINTAINER kordood <gigacms@gmail.com>

# Update apt source list mirror site
RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

# Install basic packages
RUN \
    apt-get update -y &&\
    apt-get install git zip curl unzip vim python3.8 python3-pip -y &&\
    apt-get update -y &&\
	update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Install androguard
WORKDIR /root
RUN \
    mkdir workDir &&\
    cd workDir &&\
    git clone https://github.com/androguard/androguard.git &&\
    cd androguard &&\
    pip3 install setuptools &&\
    python3 ./setup.py install

# Set projects directories
USER root
WORKDIR /root
RUN \
    mkdir result &&\
    cd result

# Set project
COPY ASTParser /root/workDir/ASTParser/
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /root/workDir/ASTParser
# CMD ["python3","parser_main.py"]