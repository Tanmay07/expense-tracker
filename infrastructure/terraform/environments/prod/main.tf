terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "pfos-terraform-state-prod"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "pfos-terraform-locks-prod"
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Environment = "prod"
      Project     = "PFOS"
      ManagedBy   = "Terraform"
    }
  }
}

locals {
  environment = "prod"
  region      = "us-east-1"
}

module "vpc" {
  source = "../../modules/vpc"

  environment        = local.environment
  vpc_cidr           = "10.30.0.0/16"
  azs                = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets    = ["10.30.1.0/24", "10.30.2.0/24", "10.30.3.0/24"]
  public_subnets     = ["10.30.101.0/24", "10.30.102.0/24", "10.30.103.0/24"]
  
  single_nat_gateway = false
}

module "eks" {
  source = "../../modules/eks"

  environment         = local.environment
  cluster_name        = "pfos-cluster-${local.environment}"
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnets
  
  node_instance_types = ["m5.large"]
  min_size            = 3
  max_size            = 10
  desired_size        = 5
}

module "rds" {
  source = "../../modules/rds"

  environment                = local.environment
  identifier                 = "pfos-db-${local.environment}"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnets
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  
  instance_class             = "db.m6g.large"
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
  
  node_type                  = "cache.m6g.large"
}

module "s3_assets" {
  source = "../../modules/s3"

  environment       = local.environment
  bucket_name       = "pfos-assets-${local.environment}-us-east-1"
  enable_cloudfront = true
}
