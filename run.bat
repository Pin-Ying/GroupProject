cd C:\Users\Pinling\OneDrive\Desktop\Python\Alvin C\GroupProject

python manage.py upload_database --model movies

python manage.py upload_database --model shows

python manage.py upload_database --model comments

git add db.sqlite3

git commit -m "auto upload_database."

git push
pause