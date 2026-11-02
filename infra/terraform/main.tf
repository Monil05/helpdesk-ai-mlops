resource "azurerm_resource_group" "helpdesk" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_kubernetes_cluster" "helpdesk" {
  name                = var.cluster_name
  location            = azurerm_resource_group.helpdesk.location
  resource_group_name = azurerm_resource_group.helpdesk.name
  dns_prefix          = var.cluster_name
  sku_tier            = "Free"

  default_node_pool {
    name                 = "system"
    node_count           = var.node_count
    vm_size              = var.node_vm_size
    os_disk_size_gb      = 30
    type                 = "VirtualMachineScaleSets"
    auto_scaling_enabled = false
    max_pods             = 30
  }

  identity {
    type = "SystemAssigned"
  }

  role_based_access_control_enabled = true

  azure_active_directory_role_based_access_control {
    tenant_id              = var.tenant_id
    admin_group_object_ids = var.aks_admin_group_object_ids
    azure_rbac_enabled     = true
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    outbound_type     = "loadBalancer"
  }

  tags = {
    project     = "helpdesk-ai"
    environment = "college-demo"
  }
}
