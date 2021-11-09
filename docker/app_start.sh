if [ "$ENV"  = "localdev" ]
then

  source "/app/bin/activate"
  cd /app
  python manage.py migrate
  python manage.py loaddata major_data.json
  python manage.py loaddata special_program_data.json
  python manage.py loaddata student_data.json

fi
