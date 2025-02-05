if [ "$ENV" = "localdev" ]
then

  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  source "/app/bin/activate"

  cd /app
  python manage.py initialize_db
  python manage.py migrate
  python manage.py load_rad_data --loadall --reload

fi
