locals {
  backend_container_name  = "url-shortener-tf-backend"
  frontend_container_name = "url-shortener-tf-frontend"
  redis_container_name    = "url-shortener-tf-redis"
  network_name            = "url-shortener-tf-network"
  redis_volume_name       = "url-shortener-tf-redis-data"
}

data "docker_image" "backend" {
  name = var.backend_image
}

data "docker_image" "frontend" {
  name = var.frontend_image
}

resource "docker_image" "redis" {
  name         = var.redis_image
  keep_locally = true
}

resource "docker_network" "app" {
  name   = local.network_name
  driver = "bridge"
}

resource "docker_volume" "redis" {
  name = local.redis_volume_name
}

resource "docker_container" "redis" {
  name  = local.redis_container_name
  image = docker_image.redis.image_id
  command = [
    "redis-server",
    "--appendonly", "yes",
    "--maxmemory", var.redis_maxmemory,
    "--maxmemory-policy", "noeviction",
  ]
  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.app.name
  }

  volumes {
    volume_name    = docker_volume.redis.name
    container_path = "/data"
  }

  healthcheck {
    test     = ["CMD", "redis-cli", "ping"]
    interval = "5s"
    timeout  = "3s"
    retries  = 10
  }

  wait         = true
  wait_timeout = 180
}

resource "docker_container" "backend" {
  name  = local.backend_container_name
  image = data.docker_image.backend.id
  env = [
    "REDIS_HOST=${docker_container.redis.name}",
    "REDIS_PORT=6379",
    "BASE_URL=http://localhost:${var.backend_port}",
  ]
  restart    = "unless-stopped"
  read_only  = true
  privileged = false

  # The REDIS_HOST reference orders backend creation after Redis. Redis uses wait=true,
  # so Terraform waits for its health check before the backend is created.
  networks_advanced {
    name = docker_network.app.name
  }

  ports {
    ip       = "127.0.0.1"
    internal = 8000
    external = var.backend_port
  }

  tmpfs = {
    "/tmp" = "rw,noexec,nosuid,size=64m"
  }

  capabilities {
    drop = ["ALL"]
  }

  security_opts = ["no-new-privileges:true"]

  healthcheck {
    test         = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
    interval     = "10s"
    timeout      = "5s"
    retries      = 10
    start_period = "20s"
  }

  wait         = true
  wait_timeout = 180
}

resource "docker_container" "frontend" {
  # Frontend is static (nginx); browser calls backend directly at
  # var.backend_port, so no env link needed. Attached to the same network
  # for consistency with Compose.
  name  = local.frontend_container_name
  image = data.docker_image.frontend.id

  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.app.name
  }

  ports {
    ip       = "127.0.0.1"
    internal = 80
    external = var.frontend_port
  }
}
