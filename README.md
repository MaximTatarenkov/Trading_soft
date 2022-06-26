# Trading_soft
1. Создать DataBase
2. Провести миграцию (описание миграции ниже) (возможно нужно добавить в db.py и models.py "." в импортах)
3. Создать группу "S&P 500"
4. Запустить скрипт filling.py

Migrations: alembic revision --autogenerate -m "message"
            alembic upgrade head
            alembic downgrade Revision-id -1
