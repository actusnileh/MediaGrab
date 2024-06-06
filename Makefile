DC = docker compose
APP_FILE = docker_compose/app.yaml

.PHONY: app
app-start:
	${DC} -f ${APP_FILE} up -d

.PHONY: app-drop
app-drop:
	${DC} -f ${APP_FILE} down

.PHONY: logs
logs:
	${DC} -f ${APP_FILE} logs -f

.PHONY: build
all:
	${DC} -f ${APP_FILE} up --build -d