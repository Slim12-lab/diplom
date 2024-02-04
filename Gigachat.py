from gigachat import GigaChat

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные
with GigaChat(credentials="YTk0N2ZlNTUtNGYzYy00ZDkzLWE1YjYtZWUzNzY0YTlmYzg5OmNiZTdmYzM2LTlmZTgtNDMwZi05YjgzLThhZDY0ZjE1OTBmNA==", verify_ssl_certs=False) as giga:
    while(1):
        response = giga.chat(input())
        print(response.choices[0].message.content)