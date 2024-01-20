resource "aws_s3_bucket" "audio_bucket" {
  bucket = "${var.PROJECT_NAMESPACE}-audio"
}

resource "aws_s3_bucket_cors_configuration" "audio_bucket_cors_configuration" {
  bucket = aws_s3_bucket.audio_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD", "PUT"]
    allowed_origins = ["*"]
    expose_headers  = []
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_policy" "audio_bucket_policy" {
  bucket = aws_s3_bucket.audio_bucket.id
  policy = data.aws_iam_policy_document.audio_bucket_policy_document.json
}

resource "aws_s3_bucket_server_side_encryption_configuration" "audio_bucket_server_side_encryption_configuration" {
  bucket = aws_s3_bucket.audio_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "audio_bucket_policy_document" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      aws_s3_bucket.audio_bucket.arn,
      "${aws_s3_bucket.audio_bucket.arn}/*",
    ]
  }

  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:DeleteBucket",
    ]

    effect = "Deny"

    resources = [
      aws_s3_bucket.audio_bucket.arn,
      "${aws_s3_bucket.audio_bucket.arn}/*",
    ]
  }
}