variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "identifier" {
  description = "Name of the RDS instance"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the RDS cluster will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for the RDS instance"
  type        = list(string)
}

variable "allowed_security_group_ids" {
  description = "Security groups allowed to access RDS"
  type        = list(string)
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.micro"
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Initial database name"
  type        = string
  default     = "pfos_ledger"
}

variable "db_username" {
  description = "Master username"
  type        = string
}

variable "multi_az" {
  description = "Enable Multi-AZ for high availability"
  type        = bool
  default     = false
}
