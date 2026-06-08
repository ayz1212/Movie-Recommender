import ollama

def ask_agent(prompt):
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']