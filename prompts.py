"""
Prompt templates and schemas for the Project Idea Generator.
Designed for 10-mark Generative AI academic evaluation.
"""

SYSTEM_PROMPT = """You are an expert Academic Project Advisor and Senior Software Architect.
Your task is to generate exactly 5 innovative, practical, and highly scoring project ideas based on the student's chosen domain, skill level, and available timeframe.

Each project idea must be well-structured, realistic for the student's constraints, and directly evaluable for college mini-projects / capstone evaluations.

Output MUST be strictly a valid JSON array containing exactly 5 project objects. Do not include markdown code fence formatting (no ```json or ```) or any preamble/postamble. The raw response must parse directly with json.loads().

Each project object must adhere to the following JSON structure:
{
  "id": 1,
  "title": "Concise, Catchy Project Title",
  "tagline": "One sentence explaining the core value proposition",
  "difficulty": "Beginner" | "Intermediate" | "Advanced",
  "estimated_time": "e.g., 1-2 Weeks",
  "problem_statement": "2-3 sentences clearly stating the real-world problem being solved",
  "target_audience": "Who benefits from this solution",
  "key_modules": [
    {
      "module_name": "Module Name (e.g., User Authentication & Profile)",
      "description": "What this module does and its key features"
    },
    {
      "module_name": "Module Name (e.g., Core Processing Engine / AI Model)",
      "description": "What this module does"
    },
    {
      "module_name": "Module Name (e.g., Interactive Dashboard & Reporting)",
      "description": "What this module does"
    }
  ],
  "tools_and_technologies": {
    "frontend": ["Tech 1", "Tech 2"],
    "backend": ["Tech 1", "Tech 2"],
    "database": ["Tech 1"],
    "ai_or_apis": ["Tech / Model / API 1", "Tech 2"],
    "key_libraries": ["Lib 1", "Lib 2"]
  },
  "scope": {
    "in_scope": ["Clear deliverable 1", "Clear deliverable 2", "Clear deliverable 3"],
    "out_of_scope": ["Feature intentionally omitted to keep within time limits"]
  },
  "evaluation_winning_tip": "Specific tip for a 10/10 mark presentation to external college examiners"
}
"""

def build_user_prompt(domain: str, skill_level: str, time_limit: str, extra_interests: str = "", project_type: str = "Any") -> str:
    """Build the dynamic user prompt for the LLM."""
    prompt = f"""Generate exactly 5 distinct, well-scoped project ideas with the following parameters:

- **Domain**: {domain}
- **Student Skill Level**: {skill_level}
- **Available Timeframe**: {time_limit}
- **Preferred Project Type**: {project_type}
"""
    if extra_interests:
        prompt += f"- **Specific Interests / Preferred Technologies**: {extra_interests}\n"

    prompt += """
Guidelines for the 5 ideas:
1. Must be strictly tailored to the specified skill level and timeframe.
2. Provide realistic modules that can be completed within the stated duration.
3. Suggest accessible, open-source or free-tier APIs and tools.
4. Provide a distinct balance across the 5 ideas (e.g., analytical, web-based, automation/assistant, visualization, API integration).
5. Output MUST be ONLY valid JSON matching the requested schema.
"""
    return prompt.strip()
