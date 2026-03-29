# python-videohosting
## Infrastructure as Code (Terraform)

Репозиторий содержит Terraform-конфигурацию в `terraform/` для запуска стека:
- `app` - приложение `python-videohosting`
- `db` - PostgreSQL
- `cache` - Redis

## Структура Terraform

- `terraform/providers.tf` - Docker provider и версии
- `terraform/main.tf` - сеть, тома, образы, контейнеры
- `terraform/variables.tf` - переменные инфраструктуры
- `terraform/terraform.tfvars` - значения переменных для окружения
- `terraform/outputs.tf` - результаты развертывания (имена, порты, IP)

## Быстрый запуск

```bash
cd terraform
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

После `apply` Terraform покажет outputs с именами контейнеров и портами.

## Остановка и удаление

```bash
cd terraform
terraform destroy
```

## Параметры

Основные настройки меняются в `terraform/terraform.tfvars`:
- `app_image`, `db_image`, `cache_image`
- `app_build_context`, `app_dockerfile`
- `app_replicas`
- `app_port`, `db_port`, `cache_port`
- `secret_key`, `postgres_user`, `postgres_password`

Примечание для Apple Silicon (`arm64`): приложение собирается локально через `docker_image.build`, чтобы избежать ошибки `no matching manifest` при pull образа без arm64-манифеста.

## Drift Detection

Если изменить контейнер вручную через Docker CLI, следующий `terraform plan` покажет расхождения между фактическим и целевым состоянием и предложит действия для восстановления.

## Важно

Terraform state и служебные файлы исключены из git через `.gitignore`:
- `.terraform/`
- `terraform.tfstate*`
- `*.tfplan`
