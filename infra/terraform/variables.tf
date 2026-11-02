variable "location" {
  description = "Azure region verified for AKS and the selected VM SKU."
  type        = string
}

variable "resource_group_name" {
  description = "Name for the dedicated demonstration resource group."
  type        = string
}

variable "cluster_name" {
  description = "Name for the AKS cluster."
  type        = string
}

variable "node_vm_size" {
  description = "One small VM SKU confirmed available in the selected region and subscription."
  type        = string
  default     = "Standard_B2s_v2"
}

variable "node_count" {
  description = "Fixed node count. Autoscaling is intentionally disabled."
  type        = number
  default     = 1

  validation {
    condition     = var.node_count == 1
    error_message = "This demonstration is configured for exactly one worker node."
  }
}
