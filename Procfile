release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: cd backend && python3 -m gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

