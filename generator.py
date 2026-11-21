"""
Core Project Idea Generator Engine.
Supports Google Gemini, Groq/OpenAI, and Intelligent Offline Fallback mode.
"""

import os
import re
import json
import logging
from typing import List, Dict, Any, Optional
from prompts import SYSTEM_PROMPT, build_user_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_json_from_response(raw_text: str) -> List[Dict[str, Any]]:
    """Clean and parse JSON array from raw LLM output."""
    text = raw_text.strip()
    
    # Remove markdown code fences if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # Try direct parse
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "projects" in data:
            return data["projects"]
    except json.JSONDecodeError:
        pass

    # Regex search for the outermost JSON array [...]
    match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError as e:
            logger.warning(f"Regex extracted text failed JSON decode: {e}")

    raise ValueError(f"Could not parse valid JSON array from response. Raw response snippet: {text[:200]}...")


def generate_with_gemini(api_key: str, domain: str, skill_level: str, time_limit: str, extra_interests: str = "", project_type: str = "Any") -> List[Dict[str, Any]]:
    """Call Google Gemini API using the modern google.genai SDK."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    user_prompt = build_user_prompt(domain, skill_level, time_limit, extra_interests, project_type)
    
    # Using gemini-2.5-flash or gemini-1.5-flash with JSON mode
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
            response_mime_type="application/json"
        )
    )
    
    return extract_json_from_response(response.text)


def generate_with_openai_compatible(api_key: str, base_url: Optional[str], model: str, domain: str, skill_level: str, time_limit: str, extra_interests: str = "", project_type: str = "Any") -> List[Dict[str, Any]]:
    """Call OpenAI or Groq (OpenAI compatible) API."""
    import openai
    
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    user_prompt = build_user_prompt(domain, skill_level, time_limit, extra_interests, project_type)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"} if "groq" not in (base_url or "").lower() else None
    )
    
    raw_content = response.choices[0].message.content
    return extract_json_from_response(raw_content)


def generate_offline_fallback(domain: str, skill_level: str, time_limit: str, extra_interests: str = "", project_type: str = "Any") -> List[Dict[str, Any]]:
    """
    Intelligent dynamic offline generator.
    Guarantees that students and evaluators can experience rich, relevant project cards
    even without network access or active API keys.
    """
    domain_clean = domain.strip().title() if domain else "Artificial Intelligence"
    skill = skill_level.strip().title() if skill_level else "Intermediate"
    time_str = time_limit.strip() if time_limit else "1-2 Weeks"

    # Pre-crafted templates tailored to domain and skill
    templates = [
        {
            "title_pattern": "Smart {domain} Assistant & Predictive Dashboard",
            "tagline": "An end-to-end interactive decision support platform for {domain} with predictive analytics.",
            "type": "Full-Stack Web App",
            "mod1": "Data Ingestion & Cleaning Pipeline",
            "mod1_desc": "Collects, validates, and preprocesses domain datasets (CSV/JSON/APIs) with automated anomaly filtering.",
            "mod2": "Predictive Modeling / LLM Analysis Engine",
            "mod2_desc": "Processes domain trends, summarizes risks, and generates contextual recommendations.",
            "mod3": "Interactive Streamlit / React Dashboard",
            "mod3_desc": "Visualizes key performance indicators (KPIs), metric graphs, and exportable summary cards.",
            "tip": "Demonstrate live data filtering and show the exact accuracy/evaluation metrics to impress examiners."
        },
        {
            "title_pattern": "Automated {domain} Report Generator & Summarizer",
            "tagline": "Transform complex domain documents into executive summaries and structured infographics.",
            "type": "NLP / Document Processing",
            "mod1": "Document Parser & Vector Indexing",
            "mod1_desc": "Extracts text from multi-page PDFs/reports and indexes chunks into FAISS/ChromaDB.",
            "mod2": "Contextual Retrieval & Prompt Synthesizer",
            "mod2_desc": "Retrieves relevant sections and generates section-wise structured executive summaries.",
            "mod3": "One-Click Report Export Engine",
            "mod3_desc": "Exports formatted PDF/HTML briefs with cited sources and confidence scores.",
            "tip": "Show a side-by-side comparison between the raw 30-page PDF and the generated 1-page structured brief."
        },
        {
            "title_pattern": "Real-Time {domain} Anomaly & Alert Monitoring System",
            "tagline": "Continuous stream monitoring to flag abnormal incidents and trigger instant notifications.",
            "type": "Monitoring & Automation",
            "mod1": "Live Event Stream Simulator",
            "mod1_desc": "Simulates continuous streaming telemetry/event logs with injected outlier incidents.",
            "mod2": "Rule-Based & ML Anomaly Detector",
            "mod2_desc": "Evaluates incoming data points against dynamic thresholds and isolation forests.",
            "mod3": "Alert Dispatcher & Audit Log Viewer",
            "mod3_desc": "Triggers webhook/email alerts with severity classification and root-cause notes.",
            "tip": "Trigger a live synthetic anomaly during the viva presentation to show the real-time card alert."
        },
        {
            "title_pattern": "Interactive {domain} Knowledge Bot with Citations",
            "tagline": "Domain-specialized conversational agent providing verifiable answers with grounded sources.",
            "type": "Conversational RAG Bot",
            "mod1": "Domain Knowledge Base Builder",
            "mod1_desc": "Curates guidelines, documentation, and research FAQs into an embedded knowledge graph.",
            "mod2": "Semantic Search & Grounded Generation",
            "mod2_desc": "Leverages hybrid keyword + vector retrieval to prevent hallucinations and cite sources.",
            "mod3": "Chat UI with Follow-up Suggestions",
            "mod3_desc": "Clean messaging interface with suggested prompt chips and feedback logging.",
            "tip": "Highlight the hallucination-prevention mechanism and show source page references in the card."
        },
        {
            "title_pattern": "{domain} Workflow Automation & Task Scheduler",
            "tagline": "End-to-end task orchestrator designed to eliminate repetitive operational bottlenecks in {domain}.",
            "type": "Workflow Automation",
            "mod1": "Trigger & Webhook Ingestion Engine",
            "mod1_desc": "Listens for domain events (new records, status updates, or time schedules).",
            "mod2": "Action Execution Pipeline",
            "mod2_desc": "Applies business logic, executes data transformations, and calls external services.",
            "mod3": "Execution History & Performance Analytics",
            "mod3_desc": "Logs execution runtimes, error fallbacks, and task throughput metrics.",
            "tip": "Quantify efficiency: state 'Reduces manual task handling time by 80%' on your presentation slide."
        }
    ]

    # Adjust tech stack based on skill level
    if skill == "Beginner":
        frontend = ["Streamlit", "HTML5/CSS3"]
        backend = ["Python (FastAPI / Flask)"]
        database = ["SQLite", "JSON File Storage"]
        ai_apis = ["Free Gemini API", "Hugging Face Inference API"]
        libs = ["Pandas", "Scikit-Learn", "Matplotlib"]
        scope_in = ["Core feature MVP", "Local database persistence", "Clean single-page card UI"]
        scope_out = ["Multi-tenant authentication", "Distributed microservices", "Kubernetes deployment"]
    elif skill == "Intermediate":
        frontend = ["Streamlit / Gradio", "Tailwind CSS components"]
        backend = ["FastAPI", "Python 3.12+"]
        database = ["PostgreSQL / SQLite", "ChromaDB (Vector DB)"]
        ai_apis = ["Gemini 2.5 Flash", "LangChain / LlamaIndex", "Groq LLaMA 3"]
        libs = ["Pandas", "Pydantic", "SQLAlchemy", "Plotly"]
        scope_in = ["Vector search pipeline", "Full CRUD operations", "Interactive visual analytics", "Export to PDF/JSON"]
        scope_out = ["Custom model pretraining from scratch", "Hardware IoT edge flashing"]
    else:  # Advanced
        frontend = ["React / Next.js or Modern Streamlit", "Plotly Dash"]
        backend = ["FastAPI Async", "Celery / Redis Worker"]
        database = ["PostgreSQL with pgvector", "Redis Cache"]
        ai_apis = ["Gemini 2.5 / OpenAI GPT-4o", "LangGraph Multi-Agent", "ChromaDB"]
        libs = ["PyTorch", "Transformers", "Pydantic v2", "Docker Compose"]
        scope_in = ["Multi-agent collaboration", "Asynchronous task queue", "Vector similarity evaluation", "Comprehensive test suite"]
        scope_out = ["Multi-region geo-redundant cluster"]

    projects = []
    for idx, t in enumerate(templates, start=1):
        title = t["title_pattern"].replace("{domain}", domain_clean)
        tagline = t["tagline"].replace("{domain}", domain_clean)
        
        projects.append({
            "id": idx,
            "title": title,
            "tagline": tagline,
            "difficulty": skill,
            "estimated_time": time_str,
            "problem_statement": f"In the {domain_clean} domain, practitioners and users face high overhead and fragmentation. This project delivers an automated, user-friendly solution to streamline operations and provide actionable intelligence.",
            "target_audience": f"{domain_clean} professionals, researchers, students, and organizations seeking efficiency.",
            "key_modules": [
                {"module_name": t["mod1"], "description": t["mod1_desc"]},
                {"module_name": t["mod2"], "description": t["mod2_desc"]},
                {"module_name": t["mod3"], "description": t["mod3_desc"]}
            ],
            "tools_and_technologies": {
                "frontend": frontend,
                "backend": backend,
                "database": database,
                "ai_or_apis": ai_apis,
                "key_libraries": libs
            },
            "scope": {
                "in_scope": scope_in,
                "out_of_scope": scope_out
            },
            "evaluation_winning_tip": t["tip"]
        })

    return projects


def generate_project_ideas(
    provider: str = "gemini",
    api_key: Optional[str] = None,
    domain: str = "Healthcare",
    skill_level: str = "Intermediate",
    time_limit: str = "1-2 Weeks",
    extra_interests: str = "",
    project_type: str = "Any",
    base_url: Optional[str] = None,
    model: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Unified entry point for generating project ideas.
    Falls back gracefully to intelligent offline generation if API keys are missing or invalid.
    """
    # Check if API key is provided directly or in environment
    if not api_key:
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        elif provider in ["openai", "groq"]:
            api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")

    # If no key, run offline fallback immediately
    if not api_key:
        logger.info(f"No API key provided for {provider}. Using intelligent offline fallback.")
        return generate_offline_fallback(domain, skill_level, time_limit, extra_interests, project_type)

    try:
        if provider == "gemini":
            return generate_with_gemini(
                api_key=api_key,
                domain=domain,
                skill_level=skill_level,
                time_limit=time_limit,
                extra_interests=extra_interests,
                project_type=project_type
            )
        elif provider in ["openai", "groq"]:
            if provider == "groq" and not base_url:
                base_url = "https://api.groq.com/openai/v1"
            if not model:
                model = "llama-3.3-70b-versatile" if provider == "groq" else "gpt-4o-mini"
            return generate_with_openai_compatible(
                api_key=api_key,
                base_url=base_url,
                model=model,
                domain=domain,
                skill_level=skill_level,
                time_limit=time_limit,
                extra_interests=extra_interests,
                project_type=project_type
            )
        else:
            return generate_offline_fallback(domain, skill_level, time_limit, extra_interests, project_type)
    except Exception as e:
        logger.error(f"Error calling {provider} API: {e}. Falling back to offline generator.")
        fallback_ideas = generate_offline_fallback(domain, skill_level, time_limit, extra_interests, project_type)
        return fallback_ideas
