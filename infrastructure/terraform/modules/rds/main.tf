# Generate a random password for RDS if not provided via secrets manager
resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# RDS Security Group
module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${var.identifier}-sg"
  description = "Security group for PostgreSQL RDS"
  vpc_id      = var.vpc_id

  ingress_with_source_security_group_id = [
    for sg_id in var.allowed_security_group_ids : {
      from_port                = 5432
      to_port                  = 5432
      protocol                 = "tcp"
      description              = "PostgreSQL access from allowed SG"
      source_security_group_id = sg_id
    }
  ]
}

# RDS Instance
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = var.identifier
  engine     = "postgres"
  engine_version = "15"
  instance_class = var.instance_class
  allocated_storage = var.allocated_storage

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result
  manage_master_user_password = false

  vpc_security_group_ids = [module.security_group.security_group_id]
  create_db_subnet_group = true
  subnet_ids             = var.subnet_ids

  multi_az = var.multi_az

  # Maintenance & Backup
  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"
  backup_retention_period = var.environment == "prod" ? 30 : 7

  deletion_protection = var.environment == "prod" ? true : false

  tags = {
    Environment = var.environment
    Project     = "PFOS"
    Terraform   = "true"
  }
}

# Store credentials in AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "pfos/${var.environment}/rds/${var.identifier}-credentials"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db_credentials_version" {
  secret_id     = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    host     = module.db.db_instance_endpoint
    dbname   = var.db_name
    port     = 5432
  })
}
