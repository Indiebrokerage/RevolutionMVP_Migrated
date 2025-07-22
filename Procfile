release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput && DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@revolutionrealty.com DJANGO_SUPERUSER_PASSWORD=RevolutionAdmin2024! python manage.py createsuperuser --noinput || echo "Admin user already exists"
web: cd backend && python3 -m gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

