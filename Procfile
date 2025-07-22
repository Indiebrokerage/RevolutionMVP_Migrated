release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py create_superuser --username admin --email admin@revolutionrealty.com --password RevolutionAdmin2024! || echo "Release phase completed with warnings"
web: cd backend && gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

