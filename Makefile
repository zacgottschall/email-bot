DEV_IMAGE_NAME = email-bot:latest
PROJECT_DIR = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
LOCAL_CONTAINER_NAME = email-bot

build:
	docker build --rm \
				 -t ${DEV_IMAGE_NAME} \
				 -f ${PROJECT_DIR}/Dockerfile \
				 ${PROJECT_DIR}

stop:
	docker rm -f ${LOCAL_CONTAINER_NAME} || true

run: build
	docker run -t \
			--rm \
			--env EMAIL_BOT_USERNAME='federalregisterbot@gmail.com' \
			--env EMAIL_BOT_PASSWORD='W#3Mz<)?~.~}B"q%'\
			-p 8080:8080 \
			--name ${LOCAL_CONTAINER_NAME} \
			${DEV_IMAGE_NAME}