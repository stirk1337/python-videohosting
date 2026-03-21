locals {
  db_container_name    = "python-videohosting-db"
  cache_container_name = "python-videohosting-cache"
}

resource "docker_network" "backend" {
  name     = var.network_name
  driver   = "bridge"
  internal = true
}

resource "docker_volume" "db_data" {
  name = var.db_volume_name
}

resource "docker_volume" "uploads_data" {
  name = var.uploads_volume_name
}

resource "docker_image" "app" {
  name         = var.app_image
  keep_locally = true

  build {
    context    = var.app_build_context
    dockerfile = var.app_dockerfile
  }
}

resource "docker_image" "db" {
  name         = var.db_image
  keep_locally = true
}

resource "docker_image" "cache" {
  name         = var.cache_image
  keep_locally = true
}

resource "docker_container" "db" {
  name  = local.db_container_name
  image = docker_image.db.image_id

  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
  ]

  ports {
    internal = var.db_internal_port
    external = var.db_port
  }

  networks_advanced {
    name = docker_network.backend.name
  }

  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }
}

resource "docker_container" "cache" {
  name    = local.cache_container_name
  image   = docker_image.cache.image_id
  command = ["redis-server", "--save", "60", "1", "--loglevel", "warning"]

  ports {
    internal = var.cache_internal_port
    external = var.cache_port
  }

  networks_advanced {
    name = docker_network.backend.name
  }
}

resource "docker_container" "app" {
  count = var.app_replicas

  name  = "python-videohosting-app-${count.index + 1}"
  image = docker_image.app.image_id

  env = [
    "APP_ENV=${var.app_env}",
    "APP_HOST=${var.app_host}",
    "APP_PORT=${var.app_internal_port}",
    "SECRET_KEY=${var.secret_key}",
    "DATABASE_URL=postgresql://${var.postgres_user}:${var.postgres_password}@${local.db_container_name}:${var.db_internal_port}/${var.postgres_db}",
    "REDIS_URL=redis://${local.cache_container_name}:${var.cache_internal_port}/0",
    "UPLOAD_DIR=${var.upload_dir}",
    "MAX_VIDEO_SIZE_MB=${var.max_video_size_mb}",
  ]

  ports {
    internal = var.app_internal_port
    external = var.app_port + count.index
  }

  networks_advanced {
    name = docker_network.backend.name
  }

  volumes {
    volume_name    = docker_volume.uploads_data.name
    container_path = var.upload_dir
  }

  depends_on = [
    docker_container.db,
    docker_container.cache,
  ]
}
