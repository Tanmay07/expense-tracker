variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "enable_cloudfront" {
  description = "Enable CloudFront distribution for this bucket"
  type        = bool
  default     = false
}
