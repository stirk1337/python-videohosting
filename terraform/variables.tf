variable "network_name" {
  description = "Name of the internal Docker network"
  type        = string
  default     = "videohosting-backend"
}

variable "db_volume_name" {
  description = "Volume name for PostgreSQL data"
  type        = string
  default     = "videohosting-db-data"
}

variable "uploads_volume_name" {
  description = "Volume name for uploaded files"
  type        = string
  default     = "videohosting-uploads-data"
}

variable "app_image" {
  description = "Application image reference"
  type        = string
}

variable "app_build_context" {
  description = "Build context for the app Docker image"
  type        = string
  default     = ".."
}

variable "app_dockerfile" {
  description = "Path to Dockerfile relative to app build context"
  type        = string
  default     = "Dockerfile"
}

variable "db_image" {
  description = "PostgreSQL image reference"
  type        = string
  default     = "postgres:16-alpine"
}

variable "cache_image" {
  description = "Redis image reference"
  type        = string
  default     = "redis:7-alpine"
}

variable "app_replicas" {
  description = "Number of application containers"
  type        = number
  default     = 1

  validation {
    condition     = var.app_replicas >= 1
    error_message = "app_replicas must be greater than or equal to 1."
  }
}

variable "app_port" {
  description = "Host base port for app containers"
  type        = number
  default     = 8000
}

variable "app_internal_port" {
  description = "App container internal port"
  type        = number
  default     = 8000
}

variable "db_port" {
  description = "Host port for PostgreSQL"
  type        = number
  default     = 5432
}

variable "db_internal_port" {
  description = "PostgreSQL internal port"
  type        = number
  default     = 5432
}

variable "cache_port" {
  description = "Host port for Redis"
  type        = number
  default     = 6379
}

variable "cache_internal_port" {
  description = "Redis internal port"
  type        = number
  default     = 6379
}

variable "app_env" {
  description = "Application runtime environment"
  type        = string
  default     = "production"
}

variable "app_host" {
  description = "Application bind host"
  type        = string
  default     = "0.0.0.0"
}

variable "secret_key" {
  description = "Application secret key"
  type        = string
  sensitive   = true
}

variable "upload_dir" {
  description = "Upload directory inside app container"
  type        = string
  default     = "/app/uploads"
}

variable "max_video_size_mb" {
  description = "Maximum upload size in MB"
  type        = number
  default     = 500
}

variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "videohosting"
}

variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "videohosting"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}
