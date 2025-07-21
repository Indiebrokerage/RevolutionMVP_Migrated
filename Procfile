web: cd backend && python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

