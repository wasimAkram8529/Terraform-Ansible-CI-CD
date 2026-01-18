terraform {
  backend "s3" {
    bucket         = "remote-backend-my-terraform-state-bucket"
    key            = "monitoring/terraform.tfstate"
    region         = "us-east-1"
    encrypt = true
  }
}