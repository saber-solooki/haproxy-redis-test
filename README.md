**Description:** This repo provides the whole infrastructure to test how HA proxy can help the python application to always connect to the correct master instance.


**How to use:** Use `docker-compose up` for bring up whole services.

You can use this command to make some delay on Master to see how the switch will happen on sentinel side: `redis-cli -p MASRER_PORT debug sleep 7`
