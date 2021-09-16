if [ "$ENV"  = "localdev" ]
then

  . /scripts/app_deploy.sh
  python manage.py loaddata major_data.json
  python manage.py loaddata student_data.json

fi
