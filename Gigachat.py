from gigachat import GigaChat

async def send(text):
    with GigaChat(credentials="YTk0N2ZlNTUtNGYzYy00ZDkzLWE1YjYtZWUzNzY0YTlmYzg5OmNiZTdmYzM2LTlmZTgtNDMwZi05YjgzLThhZDY0ZjE1OTBmNA==", verify_ssl_certs=False) as giga:
        response = giga.chat(text)
        return response.choices[0].message.content