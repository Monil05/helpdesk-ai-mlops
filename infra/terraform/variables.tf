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

variable "tenant_id" {
  description = "Microsoft Entra tenant used for AKS authentication."
  type        = string
  default     = "bd4a3f0a-4e4d-4fa5-917d-de4fca873197"
}

variable "aks_admin_group_object_ids" {
  description = "Entra security groups with cluster administrator access."
  type        = list(string)
  default     = ["fbf4e581-8f8f-42c1-b9b8-a349a44b732e"]
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
