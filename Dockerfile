FROM python:3.9
# 基础镜像，python3.9
MAINTAINER Wenhui Zhou
# 镜像作者信息
WORKDIR /app
# 工作目录，这个目录对应于镜像内的工作目录，后面的所有涉及到路径的操作都可以
# 使用WORKDIR的相对路径来指定

COPY requirements.txt ./
# 拷贝requirements.txt 到 镜像中/app/requirements.txt

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 安装pip包
COPY . .
# 将当前文件中的目录复制到/app目录下


CMD ["gunicorn", "xiaoblog:app", "-c", "./gunicorn.conf.py"]

