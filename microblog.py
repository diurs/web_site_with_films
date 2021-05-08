from app import app, db
from app.models import User, Add_films

'''
 функция контекста оболочки
 когда набираем flask shell, то она будет выхывать эту ф-ю и регистрировать элементы
 которые возвразаются ей в сеансе оболочки

Теперь можно работать с объектами БД без их импорта

''' 


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Add_films' : Add_films}