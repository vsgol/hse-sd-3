# Запуск приложения
1. Предварительно должны быть установленны .NET 6.0 и RabbitMQ
2. Перейти в `src/workers` и выполнить `dotnet run`, так запускается обработчик посылок. Их можно запустить сколько нужно
3. Перейти в `src/web` и выполнить `dotnet run`, так запускается веб-приложение. Переходя по адресу, который выведет команда можно попасть в само приложение.
4. Перейти в `src/api` и выполнить `dotnet run`, так запускается веб-приложение. Чтобы можно получить доступ к API необходимо дописать к выводимому адресу `/api`, чтобы получилось `ip:port/api`. Далее можно использовать `API`.

# API
Доступны следующие действия:
* GET/POST `api/Attempt`
* GET/PUT/DELETE `api/Attempt/{id}`
* GET/POST `api/Task`
* GET/PUT/DELETE `api/Task/{id}`