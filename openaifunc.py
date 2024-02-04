import openai 

openai.api_key = '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'

async def send(text):
                completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.5, 
                max_tokens=200,
                messages=[{"role": "user", "content": text},]
                )
                return completion.choices[0].message.content
            