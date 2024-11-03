# Переменные для Poetry и команд
POETRY = poetry
ALEMBIC = $(POETRY) run alembic

# Запуск сервера FastAPI
start:
	$(POETRY) run uvicorn src.main:app --reload 

# Команда для автогенерации новой миграции с Alembic
makemigrations:
	$(ALEMBIC) revision --autogenerate -m "Auto migration"

# Команда для применения миграций к базе данных
migrate:
	$(ALEMBIC) upgrade head
	
# Откат миграций на 1...
downgradedb:
	$(ALEMBIC) downgrade -1
	
# Проверка статуса миграций
statusdb:
	$(ALEMBIC) current
