import json

PROMPT_VERSION_DAILY = "daily_v1"

DAILY_SCHEMA = {
  "type": "object",
  "additionalProperties": False,
  "required": [
    "yesterday_summary",
    "score",
    "what_went_well",
    "what_needs_improving",
    "today_focus",
    "motivation",
    "confidence"
  ],
  "properties": {
    "yesterday_summary": {
      "type": "string"
    },
    "score": {
      "type": "string"
    },
    "what_went_well": {
      "type": "array",
      "items": {"type": "string"}
    },
    "what_needs_improving": {
      "type": "array",
      "items": {"type": "string"}
    },
    "today_focus": {
      "type": "array",
      "items": {"type": "string"}
    },
    "motivation": {
      "type": "string"
    },
    "confidence": {
      "type": "number"
    }
  }
}

def build_daily_prompt(payload_dict: dict) -> str:
    """
    Returns the full prompt text to send to OpenAI.
    """
    # Keep the prompt stable; only payload changes day-to-day.
    return (
        "You are an experienced endurance coach and nutrition analyst.\n"
        "You will receive a single day's fitness and nutrition log as JSON.\n"
        "Your task is to ANALYSE the day, and give a SHORT, MOTIVATIONAL daily review.\n"
        "You are expected to interpret the data, identify patterns, and provide judgement in this format.\n"
        "1. Yesterday Summary Give a quick overview: Estimated Calories (rough) Protein level (low / ok / high) Key issue (if any).\n"
        "2. Score Score the day out of 10 Score: X/10.\n" 
        "3. What went well ✔ List 2–3 positives.\n" 
        "4. What needs improving ❌ List 2–3 key issues only (be honest and direct).\n" 
        "5. Today’s Focus (MOST IMPORTANT) Give 2–3 clear actions for today based on yesterday. These must be: simple practical behaviour-based Examples: No alcohol today, Hit 130g protein, Control evening snacks.\n" 
        "6. Motivation End with a short, direct coaching message based on progress and goals. Tone: Direct, honest, slightly firm Not too long Focus on keeping momentum Goal: Keep me consistent, improve my running performance, and help me lose fat gradually..\n"
        "Output MUST strictly match this JSON structure exactly:\n"
        "{\n"
        '  "yesterday_summary": string,\n'
        '  "score": string,\n'
        '  "what_went_well": array of strings,\n'
        '  "what_needs_improving": array of strings,\n'
        '  "today_focus": array of strings,\n'
        '  "motivation": string,\n'
        '  "confidence": number\n'
        "}\n"
        "Do NOT rename any fields.\n"
        
        #"Make reasonable inferences based on the data provided, but do not invent new events.\n"
        #"Rules:\n"
        #"- Analyse ONLY the provided data\n"
        #"- You MAY infer quality, balance, risks, and likelihoods\n"
        #"- Do NOT invent foods, workouts, or metrics\n"
        #"- If data is missing, state that clearly\n"
        #"- Output MUST be valid JSON matching the schema\n"
        #"- Do NOT include markdown or non-JSON text\n"
        #"- Confidence reflects how reliable your analysis is based on data completeness (0.0–1.0)\n"
        #"For each section:\n"
        #"- Identify positives\n"
        #"- Identify negatives\n"
        #"- Explain why they matter\n"
        #"- Be concise, direct, and coach-like\n"
        "Here is the daily log JSON:\n"

        + json.dumps(payload_dict, ensure_ascii=False)
    )