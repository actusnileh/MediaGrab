DC = docker compose
APP_FILE = docker_compose/app.yaml

.PHONY: app
app:
	${DC} -f ${APP_FILE} up -d

.PHONY: app-drop
drop:
	${DC} -f ${APP_FILE} down

.PHONY: logs
logs:
	${DC} -f ${APP_FILE} logs -f

.PHONY: build
build:
	${DC} -f ${APP_FILE} up --build -d