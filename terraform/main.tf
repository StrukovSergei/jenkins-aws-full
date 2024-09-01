terraform {
  backend "s3" {
    bucket = "test-terraform13"
    key    = "path/to/my/key"
    region = "il-central-1"
  }
}
provider "aws" {
  region     = "il-central-1"

}
data "aws_availability_zones" "azs" {
  state = "available"
}
