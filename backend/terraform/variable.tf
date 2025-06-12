variable "region" {
  default = "us-east-1"
}

variable "s3_bucket_name" {
  default = "renewable-energy-pipeline-akshay"
}

variable "dynamodb_table" {
  default = "energy_data"
}

variable "alert_email" {
  description = "Email address to receive anomaly alerts"
  type        = string
}
