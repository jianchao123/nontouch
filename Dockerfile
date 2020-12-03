# 基础镜像
FROM ubuntu:18.04

# 维护者
MAINTAINER jianchao

# RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
# COPY ./conf/sources.list /etc/apt/sources.list

RUN mkdir /root/.pip
COPY ./conf/pip.conf /root/.pip/pip.conf

# 创建代码目录
RUN mkdir -p /data/www
RUN mkdir -p /data/logs/uwsgi
RUN mkdir -p /data/logs/supervisor

# 复制代码
COPY ./src/ /data/www
COPY ./conf/app.ini /etc/uwsgi/apps-enabled/app.ini
COPY ./conf/timer.conf /etc/supervisor/conf.d/timer.conf

# 安装包
WORKDIR /data/www


RUN apt-get update \
    && apt-get install -y --no-install-recommends swig libssl-dev python-dev \
    python2.7 python-pip libpq-dev libmysqlclient-dev \
    # && apt-get remove --purge -y $(apt-mark showauto) \
    && pip install --upgrade pip \
    && pip install setuptools && PACKAGES='uwsgi uwsgi-plugin-python supervisor' \
    && apt-get install -y --no-install-recommends ${PACKAGES}


# CMD ["/usr/bin/uwsgi", "--ini", "/etc/uwsgi/apps-enabled/app.ini"]
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/timer.conf"]
CMD ["/bin/bash"]