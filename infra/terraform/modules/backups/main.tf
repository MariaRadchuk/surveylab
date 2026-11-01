variable "environment" {
  description = "Назва середовища"
  type        = string
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "backups" {
  bucket        = "surveylab-${var.environment}-backups-${random_id.suffix.hex}"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "backups" {
  bucket                  = aws_s3_bucket.backups.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket_name" {
  value = aws_s3_bucket.backups.bucket
}
