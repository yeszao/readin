docker build --tag english-web . \
 && docker run --rm --env-file /home/gary/docker_services/readmain/local.env english-web python /workspace/src/crawl_news.py