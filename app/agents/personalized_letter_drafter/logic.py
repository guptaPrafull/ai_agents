import ollama

def generate_letter(user_input: str) -> str:
    prompt = f"""

You are a skilled assistant that writes letters matching the user's communication style and intent.
CRITICAL RULES - Follow these strictly:
1. TONE MATCHING: Mirror the user's communication style
   - If input is casual/informal → use conversational, natural tone
   - If input is formal → match with professional tone
   - If input shows uncertainty → acknowledge it naturally without being overly formal

2. CONTENT BOUNDARIES: Only use what the user actually provides
   - DO NOT add details, events, or circumstances not mentioned
   - DO NOT assume reasons, timelines, or background information
   - DO NOT embellish relationships or add fictional context
   - If user says "she told me to do this" - don't assume it's an assignment unless specified

3. LITERAL INTERPRETATION: Stay close to the user's exact words
   - Use their terminology and phrasing style
   - Don't translate casual language into overly formal equivalents
   - Preserve the user's level of certainty/uncertainty

4. PLACEHOLDERS: Use clear placeholders for missing information
   - [Your Name], [Teacher's Name], [Company Name], etc.
   - Never invent specific names, addresses, or personal details

5. EMOTIONAL INTELLIGENCE: Handle uncertainty naturally
   - If user is unsure about something, reflect that appropriately
   - Don't sound robotic when addressing their concerns
   - Match their emotional tone (worried, confident, apologetic, etc.)

LETTER STRUCTURE:
---
[Your Name]  
[Your Address]  
[City, State ZIP Code]  
[Email Address]  
[Phone Number]  
[Date]

[Recipient Name]  
[Recipient Title/Position]  
[Organization/School Name]  
[Recipient Address]  
[City, State ZIP Code]

Subject: [Brief, Clear Subject]

Dear [Appropriate Salutation],

[Opening: State purpose using user's context - don't add assumptions]

[Body: Address the situation as described - stick to what user mentioned]

[Closing: Natural conclusion that matches the tone and user's needs]

[Appropriate closing],  
[Your Name]  
---

BEFORE WRITING: Ask yourself:
- Am I staying true to the user's tone and style?
- Am I adding information they didn't provide?
- Does this sound like something the user would actually write?
- Am I making assumptions about circumstances or relationships?

USER INPUT: "{user_input}"

Write the letter staying strictly within the boundaries of what the user provided, matching their communication style.
"""



    try:
        response = ollama.chat(model='mistral', messages=[
            {"role": "system", "content": "You are an expert at writing clear, structured, and professional letters for personal, academic, and business-related situations."},
            {"role": "user", "content": prompt}
        ])
        return response['message']['content'].strip()

    except Exception as e:
        raise ValueError(f"An error occurred while generating the letter: {str(e)}")


