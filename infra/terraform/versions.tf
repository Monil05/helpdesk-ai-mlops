terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  # Provider registration is managed explicitly; Terraform plan must stay read-only.
  resource_provider_registrations = "none"
  features {}
}
