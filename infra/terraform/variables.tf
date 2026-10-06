variable "docker_host" {
  description = "Docker Engine endpoint used by the Docker provider."
  type        = string
  default     = "npipe:////.//pipe//docker_engine"

  validation {
    condition     = length(trimspace(var.docker_host)) > 0
    error_message = "docker_host must not be empty."
  }
}

variable "backend_image" {
  description = "Existing local backend image to run."
  type        = string
  default     = "url-shortener-backend:dev"

  validation {
    condition     = length(trimspace(var.backend_image)) > 0
    error_message = "backend_image must not be empty."
  }
}

variable "redis_image" {
  description = "Tagged or digest-pinned Redis image."
  type        = string
  default     = "redis:7-alpine"

  validation {
    condition     = can(regex(":[^/:]+$", var.redis_image)) || can(regex("@sha256:[0-9a-f]{64}$", var.redis_image))
    error_message = "redis_image must include an explicit image tag or sha256 digest."
  }
}

variable "redis_maxmemory" {
  description = "Redis maxmemory limit. Full Redis rejects writes instead of evicting URL records."
  type        = string
  default     = "256mb"

  validation {
    condition     = can(regex("^[1-9][0-9]*(kb|mb|gb)$", var.redis_maxmemory))
    error_message = "redis_maxmemory must be a positive integer followed by kb, mb, or gb."
  }
}

variable "backend_port" {
  description = "Host port published for the backend API."
  type        = number
  default     = 8000

  validation {
    condition     = var.backend_port >= 1 && var.backend_port <= 65535 && floor(var.backend_port) == var.backend_port
    error_message = "backend_port must be an integer between 1 and 65535."
  }
}

variable "frontend_image" {
  description = "Existing local frontend image to run."
  type        = string
  default     = "url-shortener-frontend:dev"

  validation {
    condition     = length(trimspace(var.frontend_image)) > 0
    error_message = "frontend_image must not be empty."
  }
}

variable "frontend_port" {
  description = "Host port published for the frontend."
  type        = number
  default     = 3000

  validation {
    condition     = var.frontend_port >= 1 && var.frontend_port <= 65535 && floor(var.frontend_port) == var.frontend_port
    error_message = "frontend_port must be an integer between 1 and 65535."
  }
}
