data "aws_caller_identity" "me" {}

resource "aws_s3_bucket" "lake" {
  bucket = "airquality-lake-${data.aws_caller_identity.me.account_id}"
}