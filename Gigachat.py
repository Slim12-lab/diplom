from gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

async def send(text):
        chat = GigaChat(credentials="YTk0N2ZlNTUtNGYzYy00ZDkzLWE1YjYtZWUzNzY0YTlmYzg5OmNiZTdmYzM2LTlmZTgtNDMwZi05YjgzLThhZDY0ZjE1OTBmNA==", verify_ssl_certs=False)

        messages = [
            SystemMessage(
                content="Ты клоун который поздравляет людей с праздниками"
            )
        ]

        user_input = text
        messages.append(HumanMessage(content=user_input))
        res = chat(messages)
        messages.append(res)
        return res.content