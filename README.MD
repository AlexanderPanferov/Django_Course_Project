Курсовая работа: Сервис для рассылки почты клиентам

    Содержимое проекта:
        - Главная страница(актуальная информация по клиентам, рассылкам и случайные статьи из блога)
        - Блог с возможностью просмотра, удаления, редактирования, добавления только у менеджера блога
        - Клиенты, Сообщения, Рассылки и логи - с возможностью просмотра, удаления, редактирования, добавления
                с разграничением для разных групп пользователей
        - Для пользователя реализована возможность входа, регистрации по почте, просмотра и удаления профиля, генерации
                пароля.
        - Для менеджера реализована возможность блокировки пользователя и просмотра списка пользователей через Dj-Admin
        - Возможность запускать рассылки по расписанию с помощью 'django_crontab'


Для запуска проекта требуется:
- Создать виртуальное окружение
- Установить зависимости из файла requirements.txt
- Создать суперюзера python3 manage.py csu
- Выполнить миграции
- Загрузить данные в БВ из файлов .json
- запустить проект

Для переодического запуска рассылок используйте команду: python3 manage.py crontab add
Для отключения рассылок используйте команду: python3 manage.py crontab remove
Для просмотра текущих активных задач используйте команду: python manage.py crontab show



Версия Python: 3.11.14
Версия Django: 4.2.5
Полный список модулей содержится в файле requirements.txt
