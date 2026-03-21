network_name        = "videohosting-backend"
db_volume_name      = "videohosting-db-data"
uploads_volume_name = "videohosting-uploads-data"

app_image   = "ghcr.io/stirk1337/python-videohosting:latest"
app_build_context = ".."
app_dockerfile    = "Dockerfile"
db_image    = "postgres:16-alpine"
cache_image = "redis:7-alpine"

app_replicas = 1

app_port            = 8000
app_internal_port   = 8000
db_port             = 5432
db_internal_port    = 5432
cache_port          = 6379
cache_internal_port = 6379

app_env           = "production"
app_host          = "0.0.0.0"
secret_key        = "local-terraform-secret" # pragma: allowlist secret
upload_dir        = "/app/uploads"
max_video_size_mb = 500

postgres_db       = "videohosting"
postgres_user     = "videohosting"
postgres_password = "videohosting" # pragma: allowlist secret
