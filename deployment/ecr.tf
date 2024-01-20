resource "aws_ecr_repository" "api_ecr_repository" {
  name = "${var.PROJECT_NAMESPACE}-api"

  image_scanning_configuration {
    scan_on_push = true
  }
}