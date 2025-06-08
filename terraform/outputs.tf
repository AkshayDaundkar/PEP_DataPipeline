output "lambda_function_name" {
  value = aws_lambda_function.data_processor.function_name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.data_bucket.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.energy_table.name
}


output "lambda_role_arn" {
  value = aws_iam_role.lambda_exec_role.arn
}
