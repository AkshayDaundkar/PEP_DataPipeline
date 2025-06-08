output "s3_bucket" {
  value = aws_s3_bucket.data_bucket.bucket
}

output "dynamodb_table" {
  value = aws_dynamodb_table.energy_table.name
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_exec_role.arn
}
