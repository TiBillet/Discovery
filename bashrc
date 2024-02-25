alias mm="poetry run python /DjangoFiles/manage.py migrate"
alias rsp="poetry run python /DjangoFiles/manage.py runserver 0.0.0.0:8000"
alias sp="poetry run python /DjangoFiles/manage.py shell_plus"
alias notebook="poetry run python /DjangoFiles/manage.py shell_plus --notebook"
alias rcel="poetry run celery -A Cashless worker -l INFO"
alias guni="poetry run gunicorn primary_server.wsgi --capture-output --reload -w 3 -b 0.0.0.0:8000"


load_sql() {
export PGPASSWORD=$POSTGRES_PASSWORD
export PGUSER=$POSTGRES_USER
export PGHOST=cashless_postgres

psql --dbname $POSTGRES_DB -f $1

echo "SQL file loaded : $1"
}

load_recent_sql() {

export PGPASSWORD=$POSTGRES_PASSWORD
export PGUSER=$POSTGRES_USER
export PGHOST=cashless_postgres
gz=$(ls -t $1 | head -n1)
gzip -d $gz
psql --dbname $POSTGRES_DB -f $1/$(ls -t $1 | head -n1)

echo "SQL file loaded : $1$(ls -t $1 | head -n1)"

}
