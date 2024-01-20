ACCOUNT_NUMBER="131791614471"
ECR_NAME="roboteacher-api"
IMAGE_TAG="v0"

aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin "${ACCOUNT_NUMBER}.dkr.ecr.ap-southeast-1.amazonaws.com"

docker build -t "${ACCOUNT_NUMBER}.dkr.ecr.ap-southeast-1.amazonaws.com/${ECR_NAME}:${IMAGE_TAG}" .
docker push "${ACCOUNT_NUMBER}.dkr.ecr.ap-southeast-1.amazonaws.com/${ECR_NAME}:${IMAGE_TAG}"