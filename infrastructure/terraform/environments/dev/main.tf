terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "pfos-terraform-state-dev"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "pfos-terraform-locks-dev"
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Environment = "dev"
      Project     = "PFOS"
      ManagedBy   = "Terraform"
    }
  }
}

locals {
  environment = "dev"
  region      = "us-east-1"
}

module "vpc" {
  source = "../../modules/vpc"

  environment        = local.environment
  vpc_cidr           = "10.10.0.0/16"
  azs                = ["us-east-1a", "us-east-1b"]
  private_subnets    = ["10.10.1.0/24", "10.10.2.0/24"]
  public_subnets     = ["10.10.101.0/24", "10.10.102.0/24"]
  
  # Save costs in dev
  single_nat_gateway = true
}

module "eks" {
  source = "../../modules/eks"

  environment         = local.environment
  cluster_name        = "pfos-cluster-${local.environment}"
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnets
  
  # Cost-effective nodes for dev
  node_instance_types = ["t3.medium"]
  min_size            = 1
  max_size            = 3
  desired_size        = 2
}

module "rds" {
  source = "../../modules/rds"

  environment                = local.environment
  identifier                 = "pfos-db-${local.environment}"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnets
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  
  instance_class             = "db.t4g.micro"
  db_username                = "pfos_admin"
  multi_az                   = false
}

module "elasticache" {
  source = "../../modules/elasticache"

  environment                = local.environment
  cluster_id                 = "pfos-redis-${local.environment}"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnets
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  
  node_type                  = "cache.t4g.micro"
}

module "s3_assets" {
  source = "../../modules/s3"

  environment       = local.environment
  bucket_name       = "pfos-assets-${local.environment}-us-east-1"
  enable_cloudfront = true
}
