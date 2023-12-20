FROM python:3.8.10


RUN mkdir /var/log/django
WORKDIR /code
ADD requirements.txt /code/
RUN python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
ADD . /code/
RUN apt autoremove -y

RUN addgroup --system --gid 1010 appuser
RUN adduser --system --uid  1010 --group appuser
RUN chown -R appuser:appuser /code
RUN chown -R appuser:appuser /var/log/django
RUN find / -type f -perm /6000 -exec chmod a-s {} \; || true
USER appuser

CMD ["sh", "/code/backend-entrypoint.sh"]
