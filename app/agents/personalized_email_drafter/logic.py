import ollama

def generate_email_(user_input: str) -> str:
    prompt = f"""
You are a highly skilled assistant trained to write professional, effective, and well-structured emails for a wide range of purposes.

Instructions:
- Understand the user's intent from the input.
- Determine the appropriate tone and style (e.g., formal, friendly, promotional, apologetic).
- Add structure and missing context if needed.
- Make the email concise, personalized, and ready to send.
- If the user input lacks specific details (e.g., recipient name, product, date), fill in with [Placeholders] like [Product Name], [Manager’s Name], etc.
- For scheduling or meeting-related emails, always include:
  - A placeholder for proposed date/time: [Proposed Date/Time]
  - A placeholder link or instruction for availability: [Click here to view proposed time slots] or [Please share your availability]

Use the following standard format for the email:

---
Subject: [Clear and relevant subject line]

Dear [Recipient Name/Team/Customer/etc.],

[Opening line - greeting or brief context]

[Main body - explain purpose, details, or call to action clearly]

[Closing line - wrap up with thanks, invitation, or next steps]

Best regards,  
[Your Name]  
[Your Title or Company Name]  
---

User Input:  
"{user_input}"

Now write the complete email using the above format.
"""
    try:
        response = ollama.chat(model='mistral', messages=[
            {"role": "system", "content": "You are an expert in writing professional communication."},
            {"role": "user", "content": prompt}
        ])
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error: Unable to generate draft. Details: {str(e)}"
