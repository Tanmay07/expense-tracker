# Redis Security Group
module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${var.cluster_id}-sg"
  description = "Security group for Redis ElastiCache"
  vpc_id      = var.vpc_id

  ingress_with_source_security_group_id = [
    for sg_id in var.allowed_security_group_ids : {
      from_port                = 6379
      to_port                  = 6379
      protocol                 = "tcp"
      description              = "Redis access from allowed SG"
      source_security_group_id = sg_id
    }
  ]
}

resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "${var.cluster_id}-subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = var.cluster_id
  engine               = "redis"
  node_type            = var.node_type
  num_cache_nodes      = var.num_cache_nodes
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379

  subnet_group_name    = aws_elasticache_subnet_group.redis_subnet_group.name
  security_group_ids   = [module.security_group.security_group_id]

  tags = {
    Environment = var.environment
    Project     = "PFOS"
    Terraform   = "true"
  }
}
