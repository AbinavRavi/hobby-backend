export AWS_DEFAULT_REGION := us-west-2
export COMMIT_HASH := $(shell git rev-parse --short=8 HEAD)
export ECR_REPO := 538780007699.dkr.ecr.us-west-2.amazonaws.com/data_hub
export NAMESPACE := "default"


docker-login:
	aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPO}

docker-build-prod:
	docker build --platform linux/amd64 -t ${ECR_REPO}:${COMMIT_HASH} -f ./Dockerfile .

docker-build-local:
	docker build -t ${ECR_REPO}:${COMMIT_HASH} -f ./Dockerfile .

docker-push: docker-login docker-build-prod
	docker push ${ECR_REPO}:${COMMIT_HASH}