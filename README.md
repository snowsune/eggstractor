# eggstractor
A super simple docker image packing yt-dlp, and other extractor tools with an api front written in flask

## Developing

### Redis

Yep! Finally made a project with redis, run this to just get it going.
```shell
docker run -d --name eggstractor-redis --network host redis:latest
```

Make sure to set the env variable `REDIS_URL=redis://localhost:6379/0`


### `.env` (Environment Variables)
```env
REDIS_URL=redis://redis:6379/0
DOWNLOAD_DIR=/app/downloads
```

## **Docker Setup**

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  flask:
    build: .
    container_name: yt-dlp-api
    env_file: .env
    depends_on:
      - redis
    ports:
      - "5000:5000"

  redis:
    image: redis:latest
    container_name: yt-dlp-redis
    ports:
      - "6379:6379"
```

## **Run Everything**
```sh
docker-compose up -d --build
```
