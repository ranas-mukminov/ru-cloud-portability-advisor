# ru-cloud-portability-advisor
Бренд / сайт автора: https://run-as-daemon.ru
# ru-cloud-portability-advisor

[![CI](https://github.com/run-as-daemon/ru-cloud-portability-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/run-as-daemon/ru-cloud-portability-advisor/actions/workflows/ci.yml)
[![Security](https://github.com/run-as-daemon/ru-cloud-portability-advisor/actions/workflows/security.yml/badge.svg)](https://github.com/run-as-daemon/ru-cloud-portability-advisor/actions/workflows/security.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

## English
CLI/library that analyzes Terraform and Kubernetes manifests, maps AWS/GCP/Hetzner resources to Russian clouds (Yandex/VK/Cloud.ru/Selectel), and builds migration hints with draft IaC. Features: service mapping table, migration findings, optional cost approximation (user-provided prices), and AI-ready stubs (no keys included). See `README.ru.md` for the detailed guide.

Quick start:

```bash
pip install ru-cloud-portability-advisor

ru-cloud-advisor analyze-project \
  --tf-path ./infra/terraform \
  --k8s-path ./infra/k8s \
  --config ./config/aws-to-yc.yaml \
  --out ./out/report.json

ru-cloud-advisor generate-report \
  --input ./out/report.json \
  --format markdown \
  --output ./out/report.md
```

---

## Русский

### Что это
- Анализатор Terraform/K8s для миграций из AWS/GCP/Hetzner в российские облака (Yandex/VK/Cloud.ru/Selectel).
- Отчет по тому, что маппится 1:1, где нужен рефакторинг, а где нет аналога.
- Черновики Terraform-модулей и K8s-манифестов под целевые облака, плюс ориентировочная оценка стоимости по заданным пользователем тарифам.

Полное руководство и примеры: `README.ru.md`.

### Зачем российскому бизнесу
- Санкции и уход западных провайдеров требуют локальных альтернатив.
- Требования по хранению персональных данных в РФ и близости сервисов к клиентам.
- Нужны быстрые отчеты о рисках, зонах рефакторинга и возможной экономии.

### Как использовать (пример)
```bash
pip install ru-cloud-portability-advisor

ru-cloud-advisor analyze-project \
  --tf-path ./infra/terraform \
  --k8s-path ./infra/k8s \
  --config ./config/aws-to-yc.yaml \
  --out ./out/report.json

ru-cloud-advisor generate-report \
  --input ./out/report.json \
  --format markdown \
  --output ./out/report.md
```

### Возможности
- Каталог маппингов AWS/GCP/Hetzner → Yandex/VK/Cloud.ru/Selectel для storage/DB/K8s/LB/очередей/функций.
- Отчет о миграции: 1:1, требуется рефакторинг, нет аналога; ключевые риски и рекомендации.
- Черновики Terraform/K8s под RU-облака с `TODO` для ручного заполнения.
- Приблизительная оценка стоимости: «как есть» и после миграции (по предоставленным пользователем тарифам, без скрейпа).
- AI-слой через интерфейс/заглушки: подключайте свои провайдеры LLM по желанию.

### Профессиональные услуги – run-as-daemon.ru
Проект развивается DevOps/DevSecOps-инженером с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Если вам нужно:
- спланировать миграцию из AWS/GCP/Hetzner в Yandex/VK/Cloud.ru/Selectel;
- оценить риски и возможные точки отказа;
- оптимизировать затраты в российских облаках,

вы можете заказать консалтинг, пилотный проект или миграцию «под ключ».

### Лицензия и дисклеймеры
- Лицензия: Apache-2.0 (см. `LICENSE`).
- Инструмент не гарантирует юридическое соответствие (152-ФЗ и др.), оценки стоимости примерные.
- Не содержит обходов санкций или экспортного контроля; цены задаются пользователем. Подробнее в `LEGAL.md`.
