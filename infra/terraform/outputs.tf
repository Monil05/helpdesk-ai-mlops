output "resource_group_name" {
  value = azurerm_resource_group.helpdesk.name
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.helpdesk.name
}

output "aks_location" {
  value = azurerm_kubernetes_cluster.helpdesk.location
}

output "aks_node_vm_size" {
  value = var.node_vm_size
}
