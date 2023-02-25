# 拉取python 3.9-slim 版本镜像
FROM python:3.9-slim as builder
ENV WORKSPACES /opt/ms
ENV PYTHONUNBUFFERED=1
ENV MS_ENV=production
RUN mkdir -p ${WORKSPACES}
WORKDIR ${WORKSPACES}
ENV PYPI_SIMPLE_URL  https://pypi.mirrors.ustc.edu.cn/simple

COPY ./requirements.txt ./requirements.txt
RUN python -m venv ${WORKSPACES}/venv &&  \
  ${WORKSPACES}/venv/bin/python -m pip install --upgrade pip  -i ${PYPI_SIMPLE_URL}  &&  \
  ${WORKSPACES}/venv/bin/python -m pip install -r requirements.txt -i ${PYPI_SIMPLE_URL} &&  \
  apt update -y &&  \
  apt upgrade -y &&  \
  apt install -y wget &&  \
  apt install -y vim &&  \
  apt install -y curl &&  \
  apt install -y tzdata
  
COPY . .
RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE >/etc/timezone &&  \
  mkdir -p ${WORKSPACES}/logs && \
  chmod -R 755 ${WORKSPACES}

EXPOSE 7777

CMD ["/opt/ms/venv/bin/supervisord", "-c", "/opt/ms/conf/supervisor.conf"]
