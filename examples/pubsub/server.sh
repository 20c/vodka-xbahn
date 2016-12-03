. venv27/bin/activate
export VODKA_HOME=/home/dev/sandbox/vodka-xbahn-test
uwsgi -H $VIRTUAL_ENV --socket=server.sock -w vodka.runners.wsgi:application --enable-threads
