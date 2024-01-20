terraform {

  cloud {
    organization = "nwjbrandon"
    workspaces {
      name = "roboteacher"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.46.0"
    }
  }
  required_version = "~> 1.3.6"
}

provider "aws" {
  region = var.AWS_REGION
}