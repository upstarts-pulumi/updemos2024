import os
import openai

def tell_joke():
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": 
                """
                Tell me a short joke about cloud infrastructure.  
                Don't respond to this comment - just tell the joke!
                """
            }
        ]
    )
    joke = response.choices[0].message.content or ""
    return joke.strip()

if __name__ == "__main__":
    print(tell_joke())