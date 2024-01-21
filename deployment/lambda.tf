resource "aws_lambda_function" "api_lambda_function" {
  function_name = aws_ecr_repository.api_ecr_repository.name
  architectures = ["arm64"]
  role          = aws_iam_role.lambda_iam_role.arn
  image_uri     = "${var.AWS_ACCOUNT_NUMBER}.dkr.ecr.${var.AWS_REGION}.amazonaws.com/${aws_ecr_repository.api_ecr_repository.name}:v0"
  package_type  = "Image"
  memory_size   = 4096
  timeout       = 300
  environment {
    variables = {
      OPENAI_API_KEY  = var.OPENAI_API_KEY
      DB_HOSTNAME     = var.DB_HOSTNAME
      DB_USERNAME     = var.DB_USERNAME
      DB_PASSWORD     = var.DB_PASSWORD
      DB_NAME         = var.DB_NAME
      S3_BUCKET_AUDIO = aws_s3_bucket.audio_bucket.id
    }
  }
}