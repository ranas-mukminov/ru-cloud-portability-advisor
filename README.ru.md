# ru-cloud-portability-advisor

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)

🇷🇺 Русская версия | 🇬🇧 [English version](README.md)

**ru-cloud-portability-advisor** — это CLI-инструмент для анализа инфраструктурного кода (Terraform) и манифестов Kubernetes с целью планирования миграции от зарубежных облачных провайдеров (AWS, GCP, Hetzner) на российские платформы (Yandex Cloud, VK Cloud, Cloud.ru, Selectel).

Инструмент парсит существующую конфигурацию, идентифицирует ресурсы, сопоставляет их с локальными аналогами и генерирует подробный отчет о миграции с указанием совместимости и потенциальных проблем.

## Основные возможности

- **Мультиоблачный анализ**: Парсинг файлов Terraform (`.tf`, `.hcl`) и Kubernetes (`.yaml`) для обнаружения вычислительных ресурсов, баз данных, хранилищ и сетей.
- **Умное сопоставление**: Автоматический маппинг исходных ресурсов (например, `aws_instance`, `google_sql_database`) в целевые эквиваленты (например, `yandex_compute_instance`, `vk_mdb_postgresql`).
- **Рекомендации по миграции**: Подсветка отсутствующих функций, несовместимости версий и необходимых изменений в конфигурации.
- **Гибкая отчетность**: Генерация отчетов в форматах JSON, Markdown или HTML.
- **Расширяемые правила**: Логика маппинга описана в YAML-файлах, что позволяет пользователям добавлять свои правила или поддержку новых провайдеров.
- **Приватность**: Работает полностью локально; ваш код инфраструктуры никогда не отправляется на внешние серверы.

## Архитектура и компоненты

Инструмент состоит из следующих модулей:

- **Discovery Engine**: Сканирует директории на наличие файлов Terraform и Kubernetes, используя `python-hcl2` и `PyYAML`.
- **Advisor Core**: Сопоставляет найденные ресурсы с библиотекой правил маппинга (`src/ru_cloud_portability_advisor/mapping/rules`).
- **Reporting Module**: Преобразует результаты анализа в читаемые форматы (Markdown, HTML) или машиночитаемый JSON.
- **CLI Interface**: Построен на базе `typer` для удобного взаимодействия.

## Требования

- **ОС**: Linux, macOS или Windows.
- **Python**: 3.10 или выше.
- **Зависимости**:
  - `terraform` (опционально, для более точного контекста парсинга HCL).
  - `kubectl` (опционально, для валидации манифестов).
- **Дисковое пространство**: Минимальное (<100 МБ).

## Быстрый старт

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/ranas-mukminov/ru-cloud-portability-advisor.git
   cd ru-cloud-portability-advisor
   ```

2. **Установите пакет**:
   ```bash
   pip install .
   ```

3. **Запустите анализ**:
   ```bash
   # Анализ Terraform-проекта и вывод в JSON
   ru-cloud-advisor analyze-project \
     --tf-path ./examples/terraform \
     --out analysis_result.json
   ```

4. **Сгенерируйте читаемый отчет**:
   ```bash
   # Конвертация JSON-анализа в Markdown-отчет
   ru-cloud-advisor generate-report \
     --input analysis_result.json \
     --format markdown \
     --output MIGRATION_PLAN.md
   ```

## Установка

### Из исходного кода

Рекомендуется для разработчиков и доступа к последним функциям:

```bash
git clone https://github.com/ranas-mukminov/ru-cloud-portability-advisor.git
cd ru-cloud-portability-advisor
pip install .
```

### Для разработки

Для установки вместе с инструментами тестирования и линтинга:

```bash
pip install -e ".[dev]"
```

## Настройка

Вы можете настроить параметры анализа с помощью конфигурационного YAML-файла. Это позволяет указать исходных/целевых провайдеров и предпочтения по регионам.

**Пример конфига (`config.yaml`):**

```yaml
# Исходный провайдер (aws, gcp, hetzner)
source_provider: aws

# Целевые провайдеры для рассмотрения
target_providers:
  - yandex
  - vk
  - selectel

# Предпочтительный целевой регион
region_preference: ru-central1

# Опционально: Путь к кастомным данным о ценах
pricing_file: ./custom_pricing.yaml

# Заметки для отчета
notes: "Проект миграции платежного шлюза"
```

Передайте этот конфиг анализатору:

```bash
ru-cloud-advisor analyze-project \
  --tf-path ./my-infra \
  --config ./config.yaml \
  --out report.json
```

## Использование

### Анализ гибридного проекта

Если у вас есть и Terraform, и Kubernetes файлы:

```bash
ru-cloud-advisor analyze-project \
  --tf-path ./terraform \
  --k8s-path ./k8s \
  --out full_analysis.json
```

### Просмотр поддерживаемых маппингов

Чтобы увидеть, какие ресурсы могут быть автоматически сопоставлены:

```bash
ru-cloud-advisor print-mapping-table
```

### Генерация HTML-отчета

Для отчета, который можно показать стейкхолдерам:

```bash
ru-cloud-advisor generate-report \
  --input full_analysis.json \
  --format html \
  --output migration_report.html
```

## Обновление

Для обновления до последней версии из репозитория:

```bash
git pull origin main
pip install . --upgrade
```

Если вы устанавливали через `pip install -e`, достаточно просто получить последний код (`git pull`).

## Логи и устранение неполадок

- **Ошибки парсинга**: Если инструмент не может распарсить `.tf` файл, убедитесь, что это валидный HCL. Инструмент использует `python-hcl2`, который надежен, но может спотыкаться на сложных динамических блоках.
- **Отсутствующие маппинги**: Если ресурс отображается как "Unknown" или "No mapping found", проверьте `src/ru_cloud_portability_advisor/mapping/rules`. Вы можете добавить новые правила туда.
- **Подробный вывод**: В настоящее время инструмент выводит ошибки в stderr.

## Замечания по безопасности

- **Локальное выполнение**: Этот инструмент анализирует файлы локально. Никакой код или учетные данные не загружаются в облако.
- **Секреты**: Инструмент не извлекает значения из блоков `variable` или файлов `secrets.yaml`, но всегда следите за тем, чтобы не коммитить реальные секреты в репозиторий.
- **Зависимости**: Регулярно обновляйте зависимости для устранения уязвимостей:
  ```bash
  pip-audit
  ```

## Структура проекта

- `src/ru_cloud_portability_advisor/` — Исходный код пакета.
  - `advisor/` — Логика анализа.
  - `mapping/rules/` — YAML-определения для маппинга ресурсов.
  - `cli/` — Точки входа интерфейса командной строки.
  - `render/` — Логика генерации отчетов.
- `examples/` — Примеры проектов Terraform и Kubernetes для тестирования.
- `tests/` — Модульные и интеграционные тесты.

## Как внести вклад

Мы приветствуем вклад в развитие проекта!

1. Форкните репозиторий.
2. Создайте ветку для фичи (`git checkout -b feature/new-mapping`).
3. Добавьте свои изменения (например, новые правила маппинга в `src/.../mapping/rules`).
4. Запустите тесты: `pytest`.
5. Закоммитьте и запушьте: `git push origin feature/new-mapping`.
6. Откройте Pull Request.

## Лицензия

Этот проект лицензирован под [Apache 2.0 License](LICENSE).

## Автор и коммерческая поддержка

**Автор**: [Ranas Mukminov](https://github.com/ranas-mukminov)

Для внедрения в продакшене, настройки под вашу инфраструктуру и аудита безопасности вы можете обратиться за коммерческой поддержкой на сайте **[run-as-daemon.ru](https://run-as-daemon.ru)** или связаться с автором через профиль GitHub.
