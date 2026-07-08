variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "cluster_id" {
  description = "Id of the ElastiCache cluster"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the cluster will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for the ElastiCache instance"
  type        = list(string)
}

variable "allowed_security_group_ids" {
  description = "Security groups allowed to access Redis"
  type        = list(string)
}

variable "node_type" {
  description = "Instance type for Redis"
  type        = string
  default     = "cache.t4g.micro"
}

variable "num_cache_nodes" {
  description = "Number of cache nodes"
  type        = number
  default     = 1
}
