.PHONY: start-dev follow-logs

start-dev:
	uv run python -m mela_browser --debug

follow-logs:
	tail -f /tmp/mela-browser.log