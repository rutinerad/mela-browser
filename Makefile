.PHONY: start-dev follow-logs docker-build docker-up docker-logs docker-down

start-dev:
	uv run python -m mela_browser --debug

follow-logs:
	tail -f /tmp/mela-browser.log

docker-build:
	docker compose build

docker-up:
	docker compose up -d --build

docker-logs:
	docker compose logs -f

docker-down:
	docker compose down
