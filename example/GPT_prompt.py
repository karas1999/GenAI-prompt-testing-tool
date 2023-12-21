# GPT Prompt example
# This file must include a "run_test(case)" function. The return of this function must be a list of dict. 

import json
from openai import AsyncOpenAI

OpenAI_Key = "fill the API key here"

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=OpenAI_Key
)

def convert_case_to_prompt(case):
    # system prompt
    messages = [
        {
            "role": "system",
            "content":"..."
        } 
    ]
    
    # context prompt
    for index, article in enumerate(case.context):
        messages.append(
            {
                "role": "user",
                "content": f'''... {index+1}\n\n{article}'''
            }
        )
        messages.append(
            {
                "role": "assistant",
                "content": f"..."
            }
        )

    # pre prompt
    pre_prompt = [
        {
            "role": "user",
            "content": '''...'''
        },
        {
            "role": "assistant",
            "content": '''...'''
        }
    ]

    messages.extend(pre_prompt)

    # history prompt
    for message in case.history:
        messages.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )
    
    # last message
    message = case.question + '''...'''    
    
    messages.append(
        {"role": "user", "content": message}
    )

    return messages

async def run_test(case):
        
    messages = convert_case_to_prompt(case)
    chat_completion = await client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0,
        top_p=0
    )

    reply = chat_completion.choices[0].message.content

    case_result = {
        'ID': case.id,
        'Source': case.source,
        'Source URL': case.source_url,
        'Question': case.question,
        'Expected Answer': case.expected_answer,
        'Confidence': case.confidence,
        'History': case.history,
        'Input': json.dumps(messages),
        'Output': reply
        # Add more attributes as needed
    }

    
    return case_result
