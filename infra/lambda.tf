# The identity the Lambda runs as
resource "aws_iam_role" "lambda" {
  name = "airquality-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# What that identity is allowed to do
resource "aws_iam_role_policy" "lambda" {
  name = "airquality-lambda-policy"
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.lake.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "collector" {
  function_name    = "airquality-collector"
  role             = aws_iam_role.lambda.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  filename         = "${path.module}/../collector/package.zip"
  source_code_hash = filebase64sha256("${path.module}/../collector/package.zip")
  timeout          = 300
  memory_size      = 256
  environment {
    variables = {
      BUCKET     = aws_s3_bucket.lake.bucket
      OPENAQ_KEY = var.openaq_key
    }
  }
}