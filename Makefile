DC = docker compose
APP_FILE = docker_compose/docker-compose-local.yaml


up:
	${DC} -f ${APP_FILE} up -d
down:
	${DC}  -f ${APP_FILE} down && docker network prune --force