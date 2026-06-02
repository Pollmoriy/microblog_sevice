# Corporate Microblog Service

### Backend-сервис корпоративной платформы микроблогов, вдохновлённой Twitter/X

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-316192?style=for-the-badge&logo=postgresql" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Pytest-Testing-success?style=for-the-badge&logo=pytest" />
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" />
</p>

---

### 📌 Учебный backend-проект корпоративного сервиса микроблогов

Реализован в рамках практического задания по backend-разработке на Python.  
Проект демонстрирует навыки построения REST API, работы с PostgreSQL, Docker, тестирования, Swagger-документации и клиент-серверной архитектуры.

</div>

---

# 📖 Описание проекта

**Microblog Service** — это backend-часть корпоративного сервиса микроблогов, аналогичного Twitter/X.

Сервис позволяет пользователям:

- публиковать твиты;
- удалять собственные твиты;
- подписываться на других пользователей;
- ставить лайки;
- просматривать персональную ленту;
- загружать изображения;
- получать информацию о профилях пользователей.

Frontend уже был предоставлен отдельно, поэтому основной задачей являлась реализация полноценного backend API под готовый клиент.

---

# ✨ Основные возможности

## 📝 Работа с твитами

- создание твитов;
- удаление собственных твитов;
- прикрепление изображений;
- получение ленты твитов.

---

## ❤️ Система лайков

- постановка лайка;
- удаление лайка;
- защита от повторных лайков.

---

## 👥 Система подписок

- подписка на пользователей;
- отписка;
- получение списка followers/following;
- защита от подписки на самого себя.

---

## 🖼 Работа с медиа

- загрузка изображений;
- хранение media_id;
- привязка файлов к твитам.

---

## 🔐 Авторизация

В проекте используется корпоративная схема авторизации через `api-key`.

Frontend автоматически передаёт ключ пользователя в HTTP-заголовке:

```http
api-key: user_api_key
```

Backend валидирует ключ и определяет текущего пользователя.

---

# 🏗 Архитектура проекта

Проект построен по принципам клиент-серверной архитектуры.

## Основные компоненты:

| Компонент | Назначение |
|---|---|
| FastAPI | REST API |
| PostgreSQL | Хранение данных |
| SQLAlchemy Async | ORM |
| Docker Compose | Развёртывание |
| Pytest | Тестирование |
| Swagger/OpenAPI | Документация API |

---

# 🧱 Структура проекта

```text
microblog_service/
│
├── backend/
│   ├── tests/
│   ├── utils/
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── routers.py
│   ├── schemas.py
│   └── services.py
│
├── frontend/
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🗄 Структура базы данных

## Основные сущности:

| Таблица | Описание |
|---|---|
| users | Пользователи |
| tweets | Твиты |
| likes | Лайки |
| followers | Подписки |
| medias | Загруженные изображения |

---

# 🔌 Реализованные API endpoints

## Tweets

| Метод | Endpoint | Описание |
|---|---|---|
| POST | `/api/tweets` | Создать твит |
| DELETE | `/api/tweets/{id}` | Удалить твит |
| GET | `/api/tweets` | Получить ленту |

---

## Likes

| Метод | Endpoint |
|---|---|
| POST | `/api/tweets/{id}/likes` |
| DELETE | `/api/tweets/{id}/likes` |

---

## Follow

| Метод | Endpoint |
|---|---|
| POST | `/api/users/{id}/follow` |
| DELETE | `/api/users/{id}/follow` |

---

## Users

| Метод | Endpoint |
|---|---|
| GET | `/api/users/me` |
| GET | `/api/users/{id}` |
| POST | `/api/users` |

---

## Media

| Метод | Endpoint |
|---|---|
| POST | `/api/medias` |

---

# 📚 Swagger Documentation

После запуска проекта документация автоматически доступна по адресу:

```text
http://localhost:8000/docs
```

Также доступен альтернативный интерфейс OpenAPI:

```text
http://localhost:8000/redoc
```

---

# 🧪 Тестирование

Проект покрыт unit-тестами с использованием `pytest`.

Проверяются:

- создание пользователей;
- создание твитов;
- лайки;
- подписки;
- работа API;
- обработка ошибок;
- авторизация;
- удаление твитов.

---

# 🐳 Docker Compose

Проект полностью разворачивается через Docker Compose.

Используются контейнеры:

- PostgreSQL
- Backend (FastAPI)
- Frontend

---

# ⚙️ Инструкция по запуску

# 1️⃣ Клонирование репозитория

```bash
git clone https://github.com/<your-username>/<repository>.git
cd <repository>
```

---

# 2️⃣ Запуск Docker Compose

```bash
docker-compose up -d --build
```

---

# 3️⃣ Проверка работы

## Frontend:

```text
http://localhost:8080
```

## Backend API:

```text
http://localhost:8000
```

## Swagger:

```text
http://localhost:8000/docs
```

---

# 🔑 Тестовые пользователи

Для демонстрации работы приложения можно создать тестовых пользователей через endpoint:

```http
POST /api/users
```

После создания пользователь получает:

```json
{
  "id": 1,
  "name": "Polina",
  "api_key": "generated_api_key"
}
```

Этот `api_key` используется для авторизации.

---

# 🧹 Проверка линтерами

## Black

```bash
black backend1
```

## Isort

```bash
isort backend1
```

## Flake8

```bash
flake8 backend1
```

## Mypy

```bash
mypy backend1
```

---

# 🧪 Запуск тестов

## ⚙️ Важно перед запуском

Тесты используют отдельную тестовую базу данных:

```bash
TEST_DATABASE_URL=postgresql+asyncpg://admin:admin@localhost:5433/test_microblog
```

Убедитесь, что:

- запущен PostgreSQL (через docker-compose)
- создана база `test_microblog`
- backend контейнер может подключиться к БД

---

## 🐳 Рекомендуемый способ запуска (Docker)

### ▶️ Запуск всех тестов

```bash
docker-compose run --rm backend1 pytest -vv -s
```

---

### ▶️ Запуск конкретного файла тестов

```bash
docker-compose run --rm backend pytest tests/test_users.py -vv -s
```

---

## 🧠 Проверка окружения

```bash
docker ps
echo $TEST_DATABASE_URL
```

---

## ✅ Ожидаемый результат

```
collected 3 items

tests/test_users.py ... [100%]

3 passed
```

---

# 🛠 Используемые технологии

| Технология | Назначение |
|---|---|
| Python 3.11 | Backend |
| FastAPI | REST API |
| PostgreSQL | База данных |
| SQLAlchemy Async | ORM |
| Docker | Контейнеризация |
| Docker Compose | Оркестрация |
| Pytest | Тестирование |
| Pydantic | Валидация данных |

---

# 📌 Особенности проекта

✅ Асинхронный backend  
✅ REST API  
✅ Swagger/OpenAPI  
✅ Docker Compose  
✅ PostgreSQL  
✅ Unit tests  
✅ Линтеры и типизация  
✅ Архитектура service layer  
✅ Работа с медиа  
✅ Система подписок и лайков

---

<div align="center">

# ⭐ Спасибо за просмотр проекта!

</div>
