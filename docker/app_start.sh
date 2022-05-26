if [ "$ENV"  = "localdev" ]
then

  source "/app/bin/activate"
  cd /app
  python manage.py migrate

fi
