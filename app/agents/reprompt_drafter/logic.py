import ollama

def reprompt_input(raw_prompt: str) -> str:

    system_prompt = f"""You are an expert prompt engineer with deep knowledge of LLM optimization. Your task is to improve prompts following these principles:

IMPROVEMENT CRITERIA:
1. Clarity: Remove ambiguity, use precise language
2. Specificity: Add concrete details or options without over-constraining
3. Structure: Organize with clear sections, formatting
4. Role Definition: Define the AI's role when useful
5. Output Format: Suggest clear formats (e.g., list, step-by-step, bullet points)
6. Context: Add background information if needed
7. Variants: Offer multiple improved versions when there’s more than one useful interpretation
8. Preserve Intent: Maintain the user's original goal and level of openness

{f"FOCUS AREA: Pay special attention to clarity"}

ORIGINAL PROMPT:
{raw_prompt}

INSTRUCTIONS:
- Provide your analysis of issues with the original prompt
- Then provide 2–3 improved versions, if applicable (e.g., general and role-specific)
- Explain what changes you made and why

FORMAT YOUR RESPONSE AS:
ANALYSIS:
[Brief analysis of weaknesses]

IMPROVED PROMPTS:
1. [Improved version 1]
2. [Improved version 2]
3. [Optional version 3]
4. [Optional version 4]
5. [Optional version 5]

CHANGES MADE:
[Summary of key improvements and reasoning]
"""

    try:
        response = ollama.chat(model='llama3', messages=[
            {"role": "system", "content": "You help rephrase prompts while preserving their original meaning and intent."},
            {"role": "user", "content": system_prompt}
        ])

        return response['message']['content'].strip()
    except Exception as e:
        raise ValueError(f"Error reprompting input: {str(e)}")
