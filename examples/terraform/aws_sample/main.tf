provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "sample" {
  bucket = "sample-bucket"
  versioning {
    enabled = true
  }
}

resource "aws_db_instance" "db" {
  identifier = "sample-db"
  engine     = "postgres"
  instance_class = "db.t3.micro"
  allocated_storage = 20
}

resource "aws_lb" "app" {
  name               = "sample"
  load_balancer_type = "application"
}

resource "aws_lambda_function" "fn" {
  function_name = "hello"
  role          = "arn:aws:iam::123456:role/lambda"
  runtime       = "python3.10"
  handler       = "main.handler"
  filename      = "dummy.zip"
}

