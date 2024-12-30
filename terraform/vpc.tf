module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1"

  name                 = "app-VPC"
  cidr                 = var.vpc_cidr
  azs                  = data.aws_availability_zones.azs.names
  public_subnets       = var.public_subnets
  private_subnets      = var.private_subnets
  enable_nat_gateway   = true
  single_nat_gateway   = true
  one_nat_gateway_per_az = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "app-VPC"
    Terraform   = "true"
    Environment = "production"
  }

  public_subnet_tags = {
    "Name"                   = "app-Public-Subnet"
    "kubernetes.io/role/elb" = 1
  }
  private_subnet_tags = {
    "Name"                            = "app-Private-Subnet"
    "kubernetes.io/role/internal-elb" = 1
  }
}

  //create elastic ip for public subnets
  //resource "aws_eip" "nat" {
  //  count = 1
  //
  //  vpc = true
  //}
}
