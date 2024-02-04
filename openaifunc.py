import openai 

openai.api_key = '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'

async def send(text):
            try:
                completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.5, 
                max_tokens=200,
                messages=[{"role": "user", "content": text},]
                )
                return completion.choices[0].message.content
            except openai.error.OpenAIError as e:
                print(f"OpenAI API Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")