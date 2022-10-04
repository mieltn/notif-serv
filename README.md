# Notification Service
Django API for creating and managing mailings, and sending them to different clients to external endpoint.

## How to start the API from Docker

1. `git clone https://github.com/mieltn/notifserv.git`
2. `docker compose build` to build Docker images. You need to have Docker and Docker Compose installed.
3. `docker compose up` to start the app. It will be available on `http://0.0.0.0:8000/`

## Functionality and testing

- API documentation can be found in 
- To test different views <i>manualtests.py</i> can be run. It uses <i>testdata.json</i> to populate database and schedules several mailings to test main logic. Since service uses Celery to handle scheduling, tasks might be not completed immediately. Monitor docker compose log in terminal.
- After running manual tests, execute `bash enterdb.sh` to enter the backend database and explore the results with SQL.
- For client views unit tests using Django Testing framework are also created.
- Custom requests to API endpoints can be sent using any other tools like Postman, curl etc.
