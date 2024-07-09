DC = docker compose
APP_FILE = docker_compose/app.yaml
STORAGE_FILE = docker_compose/storages.yaml
ENV_FILE = --env-file .env

.PHONY: app
app:
	${DC} -f ${APP_FILE} up -d

.PHONY: drop-app
drop-app:
	${DC} -f ${APP_FILE} down

.PHONY: storage
storage:
	${DC} ${ENV_FILE} -f ${STORAGE_FILE} up --build -d

.PHONY: drop-storage
drop-storage:
	${DC} ${ENV_FILE} -f ${STORAGE_FILE} down

.PHONY: drop-all
drop-all:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} ${ENV_FILE} down

.PHONY: logs
logs:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} ${ENV_FILE} logs -f

.PHONY: build
build:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} ${ENV_FILE} up --build -d