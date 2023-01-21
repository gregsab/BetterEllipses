FROM python:3.9
WORKDIR /code
EXPOSE 5000
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && \
    echo "nobody:x:65534:65534:Nobody:/:" > /etc/passwd
USER nobody
COPY ./app /code/app
ENV LOG_LEVEL=INFO
CMD ["gunicorn", "app.main:app", "-b", ":5000" ]