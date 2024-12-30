resource "aws_security_group" "worker_group_mgmt" {
  for_each = {
    one = "worker_group_mgmt_one"
    two = "worker_group_mgmt_two"
    all = "all_worker_mgmt"
  }

  name_prefix = each.value
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
}
