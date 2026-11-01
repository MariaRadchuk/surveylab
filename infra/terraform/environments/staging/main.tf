terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

provider "aws" {
  region = "us-east-1"

  # Локальний емулятор AWS (LocalStack) і тестові ключі
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  endpoints {
    ec2            = "http://localhost:4566"
    s3             = "http://localhost:4566"
    secretsmanager = "http://localhost:4566"
  }
}

module "network" {
  source      = "../../modules/network"
  environment = var.environment
}

module "app_host" {
  source        = "../../modules/app-host"
  environment   = var.environment
  instance_type = var.instance_type
  vpc_id        = module.network.vpc_id
  subnet_id     = module.network.public_subnet_ids[0]
}

module "backups" {
  source      = "../../modules/backups"
  environment = var.environment
}

module "secrets" {
  source      = "../../modules/secrets"
  environment = var.environment
}

output "app_host_ip" {
  value = module.app_host.public_ip
}

output "backups_bucket" {
  value = module.backups.bucket_name
}

output "db_secret_arn" {
  value = module.secrets.secret_arn
}
