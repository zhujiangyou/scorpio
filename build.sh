cd /root/scorpio

git fetch origin
git merge origin/master

cd /root/scorpio/scorpio

python3 manage.py migrate --settings=scorpio.settings_test
python3 manage.py collectstatic --no-input --settings=scorpio.settings_test

supervisorctl restart scorpio

service nginx restart