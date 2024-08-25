black:
	black bet_maker_service line_provider_service

isort:
	isort bet_maker_service line_provider_service

ruff-check:
	ruff check bet_maker_service line_provider_service

ruff-format:
	ruff check bet_maker_service line_provider_service --fix

format: isort black ruff-format

up:
	docker compose up --remove-orphans --build \
		bsw_bet_maker \
		bsw_line_provider \
		bsw_rabbitmq \
		bsw_bet_maker_postgres_db \
