PLIST = $(HOME)/Library/LaunchAgents/com.rutinerad.recept.plist

.PHONY: load unload start stop logs start-dev

load:
	cp com.rutinerad.recept.plist $(PLIST)
	launchctl bootout gui/$(shell id -u) $(PLIST) 2>/dev/null || true
	launchctl bootstrap gui/$(shell id -u) $(PLIST)

unload:
	launchctl bootout gui/$(shell id -u) $(PLIST)

start:
	launchctl start com.rutinerad.recept

stop:
	launchctl stop com.rutinerad.recept

logs:
	tail -f /tmp/mela-browser.log

start-dev:
	uv run python -m mela_browser --debug
