FROM python:3.11-alpine AS builder

WORKDIR /app

COPY app.py .

RUN pip install flask && \
    python app.py && \
    ls -la /tmp/

FROM nginx:alpine

COPY --from=builder /tmp/index.html /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]