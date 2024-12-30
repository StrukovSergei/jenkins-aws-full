terraform {
  backend "s3" {
    bucket = "test-terraform13"
    key    = "path/to/my/key"
    region = var.region
  }
}

provider "aws" {
  region = var.region
}

data "aws_availability_zones" "azs" {
  state = "available"
}
