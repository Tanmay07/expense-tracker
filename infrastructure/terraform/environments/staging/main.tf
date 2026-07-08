terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "pfos-terraform-state-staging"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "pfos-terraform-locks-staging"
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Environment = "staging"
      Project     = "PFOS"
      ManagedBy   = "Terraform"
    }
  }
}

locals {
  environment = "staging"
  region      = "us-east-1"
}

module "vpc" {
  source = "../../modules/vpc"

  environment        = local.environment
  vpc_cidr           = "10.20.0.0/16"
  azs                = ["us-east-1a", "us-east-1b"]
  private_subnets    = ["10.20.1.0/24", "10.20.2.0/24"]
  public_subnets     = ["10.20.101.0/24", "10.20.102.0/24"]
  
  # Staging needs HA
  single_nat_gateway = false
}

module "eks" {
  source = "../../modules/eks"

  environment         = local.environment
  cluster_name        = "pfos-cluster-${local.environment}"
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnets
  
  node_instance_types = ["t3.large"]
  min_size            = 2
  max_size            = 5
  desired_size        = 3
}

module "rds" {
  source = "../../modules/rds"

  environment                = local.environment
  identifier                 = "pfos-db-${local.environment}"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnets
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  
  instance_class             = "db.t4g.small"
  db_username                = "pfos_admin"
  multi_az                   = true
}

module "elasticache" {
  source = "../../modules/elasticache"

  environment                = local.environment
  cluster_id                 = "pfos-redis-${local.environment}"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnets
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  
  node_type                  = "cache.t4g.small"
}

module "s3_assets" {
  source = "../../modules/s3"

  environment       = local.environment
  bucket_name       = "pfos-assets-${local.environment}-us-east-1"
  enable_cloudfront = true
}
