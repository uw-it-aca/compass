if [ "$ENV" = "localdev" ]
then

  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  source "/app/bin/activate"

  cd /app
  python manage.py migrate
  python manage.py initialize_person_db
  python manage.py load_rad_data --loadall --reload

  python manage.py loaddata --app compass --database uw_person \
    adviser.json employee.json person.json student.json transcript.json

  fixtures=""
  for fixture in \
    access-groups.json \
    affiliations.json \
    app-user.json \
    cohorts.json \
    contact-methods.json \
    contact-topics.json \
    contact-types.json \
    eligibility-types.json \
    specialprogram.json \
    student.json \
    student-affiliations.json \
    visit.json \
    visit-types.json
  do
    fixtures="$fixtures initial_data/$fixture"
  done

  python manage.py loaddata --app compass --database default $fixtures

fi
