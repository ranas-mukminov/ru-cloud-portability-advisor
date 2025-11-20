# ru-cloud-portability-advisor (расширенная версия)

## Кратко
- CLI/библиотека для анализа Terraform и Kubernetes манифестов, чтобы спланировать миграцию из AWS/GCP/Hetzner в российские облака (Yandex/VK/Cloud.ru/Selectel).
- Генерирует карту соответствий сервисов, рекомендации по рефакторингу и черновики Terraform/K8s под целевые облака. Стоимость оценивается по упрощенной модели с тарифами, которые задает пользователь.

## Возможности
- Детектирование провайдера по Terraform/K8s и нормализация в единую доменную модель ресурсов.
- Каталог маппингов по направлениям: storage, БД, Kubernetes, балансировщики, очереди, функции.
- Отчет: что маппится 1:1, где нужен рефакторинг, где нет аналога; список рисков и технических рекомендаций.
- Рендеринг отчета в JSON/Markdown/HTML (см. `examples/reports`).
- AI-слой через интерфейс `AIProvider`: по умолчанию — заглушки; можно подключить свой LLM через env/конфиг.
- Примерная оценка стоимости «как есть» и «после миграции», без скрейпа тарифов (тарифы передает пользователь через YAML/JSON).

## Быстрый старт
```bash
pip install ru-cloud-portability-advisor

# Анализ Terraform+K8s проекта
ru-cloud-advisor analyze-project \
  --tf-path ./infra/terraform \
  --k8s-path ./infra/k8s \
  --config ./config/aws-to-yc.yaml \
  --out ./out/report.json

# Рендер отчета
ru-cloud-advisor generate-report \
  --input ./out/report.json \
  --format markdown \
  --output ./out/report.md

# Таблица маппингов
ru-cloud-advisor print-mapping-table
```

## Конфигурация
- Схема: `src/ru_cloud_portability_advisor/config/schema.yaml`.
- Примеры: `src/ru_cloud_portability_advisor/config/examples/*.yaml` и `examples/pricing/*.yaml`.
- Ключевые поля:
  - `source_provider`: aws|gcp|hetzner;
  - `target_providers`: yandex|vk|cloud_ru|selectel;
  - `pricing_file`: путь к YAML/JSON с ценами (опционально).

## Структура репозитория (сокращенно)
```
src/ru_cloud_portability_advisor/
  discovery/    # парсеры Terraform/K8s и детекторы провайдеров
  mapping/      # каталог правил и маппер
  cost/         # модели и оценка стоимости
  advisor/      # сборка анализа и отчета
  render/       # Markdown/HTML рендереры
  cli/          # команды Typer
  ai/           # интерфейс и заглушки AI
examples/       # готовые конфиги, манифесты и отчеты
scripts/        # lint, security, perf
tests/          # unit/integration
```

## Практические кейсы
- AWS → Yandex Cloud: `examples/terraform/aws_sample` + конфиг `config/examples/aws_to_yc_simple.yaml` → отчет `examples/reports/aws_to_yc_sample.md`.
- GCP → VK Cloud: `examples/terraform/gcp_sample` + конфиг `config/examples/gcp_to_vk_medium.yaml`.
- Hetzner → Selectel: `examples/terraform/hetzner_sample` показано для compute/LB/volume.

## Ограничения и комплаенс
- Проект не обходит санкции/экспортный контроль и не содержит скрейпа тарифов: цены вводит пользователь.
- Нет гарантий юридического соответствия (152-ФЗ и др.), выводы — ориентир для архитектурных решений.
- Не храните реальные секреты/ключи в репозитории; перед анализом анонимизируйте чувствительные данные.
- При работе с конфигами, содержащими ПДн или коммерческую тайну, соблюдайте локальные законы и внутренние политики.
- Юридические детали и ограничения использования описаны в `LEGAL.md`.

## Профессиональные услуги – run-as-daemon.ru
Проект развивается DevOps/DevSecOps-инженером с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Можно заказать:
- аудит и план миграции AWS/GCP/Hetzner → Yandex/VK/Cloud.ru/Selectel;
- оценку рисков/точек отказа и план минимизации даунтайма;
- оптимизацию затрат и сопровождение пилотной миграции.

## Лицензия
Apache-2.0. Свободно используйте в коммерческих проектах при сохранении уведомлений о лицензии. См. `LICENSE`.
