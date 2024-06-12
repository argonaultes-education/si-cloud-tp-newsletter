FROM python:3.12-slim
WORKDIR /app
RUN mkdir templates
COPY templates/subscribe.html templates/
COPY templates/welcome.html templates/
RUN mkdir static
COPY static/bg1.jpg static/
COPY newsletter.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PORT 5000
ENV HOST "localhost"
ENV METRICS_PORT 9000
EXPOSE ${PORT}
EXPOSE ${METRICS_PORT}
CMD ["flask", "--app", "newsletter", "run", "--port", "5000", "--host", "0.0.0.0"]