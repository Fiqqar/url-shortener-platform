output "backend_url" {
  description = "Local URL for the backend API."
  value       = "http://localhost:${var.backend_port}"
}

output "backend_container_name" {
  description = "Terraform-managed backend container name."
  value       = docker_container.backend.name
}

output "redis_container_name" {
  description = "Terraform-managed Redis container name."
  value       = docker_container.redis.name
}

output "redis_volume_name" {
  description = "Persistent Terraform-managed Redis volume name."
  value       = docker_volume.redis.name
}

output "network_name" {
  description = "Dedicated Terraform-managed Docker network name."
  value       = docker_network.app.name
}