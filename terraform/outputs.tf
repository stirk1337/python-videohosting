output "network_name" {
  description = "Backend Docker network name"
  value       = docker_network.backend.name
}

output "db_container_name" {
  description = "Database container name"
  value       = docker_container.db.name
}

output "cache_container_name" {
  description = "Cache container name"
  value       = docker_container.cache.name
}

output "app_container_names" {
  description = "Application container names"
  value       = [for c in docker_container.app : c.name]
}

output "app_external_ports" {
  description = "Published app ports on host"
  value       = [for c in docker_container.app : c.ports[0].external]
}

output "app_container_ips" {
  description = "Application container IP addresses"
  value       = [for c in docker_container.app : c.network_data[0].ip_address]
}

output "db_external_port" {
  description = "Published database port on host"
  value       = docker_container.db.ports[0].external
}

output "db_container_ip" {
  description = "Database container IP address"
  value       = docker_container.db.network_data[0].ip_address
}

output "cache_external_port" {
  description = "Published cache port on host"
  value       = docker_container.cache.ports[0].external
}

output "cache_container_ip" {
  description = "Cache container IP address"
  value       = docker_container.cache.network_data[0].ip_address
}
