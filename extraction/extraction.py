import openai
import json
from docx import Document

openai.api_key = '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'

# Define the filename for the JSON file
filename = 'notification_dataset.json'

# Read the announcements from the Word document
doc = Document('announcements.docx')
announcements = [p.text for p in doc.paragraphs]

# Loop over each announcement
for announcement in announcements:
    messages = [
        {
            "role": "system",
            "content": """You are an AI that converts user input into a dataset. The output should be in the following format: 
            {"query_text": "When is the registration deadline for MCA Integrated S4 (S) Examination May/June 2023 and MCA Integrated S6 (S) Examination May/June 2023?",
        "query_type": "Exam Registration",
        "relevant_keywords": ["registration", "deadline", "mca", "integrated", "s4", "examination", "may/june", "2023"],
        "relevant_information": "Registration deadline is 14-05-2023"
            }"""
        },
        {"role": "user", "content": announcement}
    ]
    
    chat = openai.ChatCompletion.create(
        model="text-davinci-002", messages=messages
    )
    reply = chat.choices[0].text
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
    
    # Save the chat reply as a dataset to a JSON file
    dataset = {"input": announcement, "output": reply}  # Define the dataset format based on your specific use case
    with open(filename, 'a') as f:  # Use 'a' mode to append to the file instead of overwriting it
        json.dump(dataset, f)
        f.write('\n')  # Add a newline character after each dataset to separate them
