provider "aws" {
  region = var.region
}

# S3 Bucket
resource "aws_s3_bucket" "data_bucket" {
  bucket = var.s3_bucket_name

  tags = {
    Project = "EnergyPipeline"
  }
}

# DynamoDB Table
resource "aws_dynamodb_table" "energy_table" {
  name         = var.dynamodb_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "site_id"
  range_key    = "timestamp"

  attribute {
    name = "site_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Project = "EnergyPipeline"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach basic execution policy
resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda-policy-attachment"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "data_processor" {
  function_name = "data_processor_lambda"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "process_data.lambda_handler"
  runtime       = "python3.11"
  filename      = "${path.module}/function.zip"

  source_code_hash = filebase64sha256("${path.module}/function.zip")

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table
      SNS_TOPIC_ARN = aws_sns_topic.anomaly_alerts.arn

    }
  }
}

# Lambda Permission for S3 to trigger it
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.data_bucket.arn
}

# S3 Trigger
resource "aws_s3_bucket_notification" "lambda_trigger" {
  bucket = aws_s3_bucket.data_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.data_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_function.data_processor,
    aws_lambda_permission.allow_s3
  ]
}


resource "aws_iam_policy" "lambda_s3_access" {
  name = "lambda-s3-access-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = "${aws_s3_bucket.data_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_s3_policy_attach" {
  name       = "lambda-s3-access-attachment"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = aws_iam_policy.lambda_s3_access.arn
}

resource "aws_iam_policy" "lambda_dynamodb_access" {
  name = "lambda-dynamodb-access-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem"
        ],
        Resource = aws_dynamodb_table.energy_table.arn
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_dynamodb_policy_attach" {
  name       = "lambda-dynamodb-access-attachment"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = aws_iam_policy.lambda_dynamodb_access.arn
}


# Create SNS Topic
resource "aws_sns_topic" "anomaly_alerts" { 
  name = "energy-anomaly-alerts"
}

# Subscribe an email address to the topic
resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.anomaly_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email  # e.g. "your.email@example.com"
}


resource "aws_iam_role_policy" "lambda_sns_publish" {
  name = "LambdaSNSSendPolicy"
  role = aws_iam_role.lambda_exec_role.name  

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "sns:Publish"
        Resource = aws_sns_topic.anomaly_alerts.arn
      }
    ]
  })
}
