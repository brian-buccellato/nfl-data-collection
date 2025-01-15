terraform {
  backend "s3" {
    bucket = "very-cool-bucket-for-terraform-lab-666"
    key    = "pfr-tf-state/terraform.tfstate"
    dynamodb_table = "pfr-tf-state-lock"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.8"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}