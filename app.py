"""
Project Idea Generator - Streamlit Web Application
Roll No / Project Topic #49: Project Idea Generator
Mini Project for Generative AI (10-Mark Academic Evaluation)
"""

import streamlit as st
import json
import os
from dotenv import load_dotenv
from generator import generate_project_ideas

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Project Idea Generator | GenAI Studio",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Card UI & Theme-Adaptive Styling
st.markdown("""
<style>
    /* Main container header */
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 1.6rem 1.8rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.3);
    }
    .main-header h1 {
        color: white !important;
        font-weight: 800;
        font-size: 2.1rem;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #e0e7ff;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Project Card Styling with Adaptive Contrast */
    .project-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -2px rgba(0, 0, 0, 0.2);
        border-color: #818cf8;
    }
    
    /* Light Theme Overrides */
    @media (prefers-color-scheme: light) {
        .project-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .project-title {
            color: #0f172a !important;
        }
        .project-tagline {
            color: #475569 !important;
        }
        .project-body {
            color: #334155 !important;
        }
    }
    
    /* Dark Theme Overrides */
    @media (prefers-color-scheme: dark) {
        .project-card {
            background: #1e293b;
            border: 1px solid #334155;
        }
        .project-title {
            color: #f8fafc !important;
        }
        .project-tagline {
            color: #94a3b8 !important;
        }
        .project-body {
            color: #cbd5e1 !important;
        }
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 700;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 0.5rem;
    }
    .badge-beginner {
        background-color: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
    }
    .badge-intermediate {
        background-color: #dbeafe;
        color: #1d4ed8;
        border: 1px solid #93c5fd;
    }
    .badge-advanced {
        background-color: #fef3c7;
        color: #b45309;
        border: 1px solid #fcd34d;
    }
    .badge-time {
        background-color: #f3e8ff;
        color: #7e22ce;
        border: 1px solid #d8b4fe;
    }
    
    /* Tech chip tags */
    .tech-tag {
        display: inline-block;
        background-color: rgba(99, 102, 241, 0.12);
        color: #818cf8;
        border-radius: 6px;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
        border: 1px solid rgba(99, 102, 241, 0.25);
    }
    
    .tip-box {
        background: rgba(168, 85, 247, 0.1);
        border-left: 4px solid #a855f7;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-top: 1rem;
        font-size: 0.88rem;
        color: #d8b4fe;
    }
    
    .scroll-hint {
        background: linear-gradient(90deg, rgba(79, 70, 229, 0.15), rgba(124, 58, 237, 0.15));
        border: 1px dashed #818cf8;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="main-header">
    <h1>💡 Project Idea Generator</h1>
    <p>AI-Powered Academic & Final-Year Project Advisor | Domain & Skill Tailored Recommendations</p>
    <div style="margin-top: 0.6rem; font-size: 0.85rem; opacity: 0.95;">
        <span>🎯 Problem #49</span> &bull; 
        <span>📚 GenAI Mini Project (10-Mark Evaluation)</span> &bull; 
        <span>⚡ 5 Cards Layout with Modules & Stack</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ LLM Configuration")
    provider = st.selectbox(
        "LLM Provider",
        options=["Google Gemini (Recommended)", "Groq (Fast Open-Source)", "OpenAI", "Smart Offline Demo (No API Key)"],
        index=0
    )
    
    api_key_input = ""
    model_name = ""
    
    if "Gemini" in provider:
        provider_code = "gemini"
        default_key = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
        api_key_input = st.text_input(
            "Gemini API Key",
            value=default_key,
            type="password",
            help="Get a free key from Google AI Studio (aistudio.google.com)"
        )
        model_name = "gemini-2.5-flash"
    elif "Groq" in provider:
        provider_code = "groq"
        default_key = os.getenv("GROQ_API_KEY", "")
        api_key_input = st.text_input(
            "Groq API Key",
            value=default_key,
            type="password",
            help="Get a free key from console.groq.com"
        )
        model_name = "llama-3.3-70b-versatile"
    elif "OpenAI" in provider:
        provider_code = "openai"
        default_key = os.getenv("OPENAI_API_KEY", "")
        api_key_input = st.text_input(
            "OpenAI API Key",
            value=default_key,
            type="password"
        )
        model_name = "gpt-4o-mini"
    else:
        provider_code = "fallback"
        st.info("ℹ️ Running in **Smart Offline Mode**. No API key needed. Generates rich tailored ideas instantly.")

    st.markdown("---")
    st.subheader("📋 Evaluation Rubric")
    st.caption("• **Inputs Handled**: Domain, Skill Level, Timeframe\n• **Outputs**: 5 structured ideas with scope, modules & tools\n• **Display**: Responsive card components\n• **Evaluation**: Tailored winning presentation tips")
    
    st.markdown("---")
    st.caption("Developed for GenAI Mini Project Evaluation &bull; Roll No / Topic #49")

# Main Input Section
col1, col2, col3 = st.columns([1.5, 1, 1])

with col1:
    domain_options = [
        "Artificial Intelligence & Machine Learning",
        "Healthcare & Telemedicine",
        "Cybersecurity & Threat Detection",
        "FinTech & Algorithmic Finance",
        "EdTech & Personalized Learning",
        "E-Commerce & Recommendation Systems",
        "IoT & Smart Home Automation",
        "Environmental Sustainability & Clean Energy",
        "Blockchain & Web3 Decentralized Apps",
        "Custom (Enter your own)"
    ]
    selected_domain = st.selectbox("Select Project Domain", domain_options, index=6)
    
    if selected_domain == "Custom (Enter your own)":
        domain_input = st.text_input("Enter Custom Domain", placeholder="e.g., Autonomous Drones, Robotics, Agritech")
    else:
        domain_input = selected_domain

with col2:
    skill_level = st.select_slider(
        "Student Skill Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Advanced"
    )

with col3:
    time_limit = st.selectbox(
        "Available Timeframe",
        options=[
            "1-2 Weeks (Mini Project)",
            "3-4 Weeks (Extended Mini)",
            "2-3 Months (Semester Project)",
            "6 Months (Capstone / Final Year)"
        ],
        index=3
    )

# Optional Advanced Inputs
with st.expander("🛠️ Optional Project Preferences (Filters)"):
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        project_type = st.selectbox(
            "Preferred Project Architecture",
            ["Any (Balanced Mix)", "Full-Stack Web Application", "AI/ML Model & API", "Conversational RAG / Assistant", "Automation Script / CLI Tool"],
            index=0
        )
    with exp_col2:
        extra_interests = st.text_input(
            "Specific Technologies or Interests",
            placeholder="e.g., Python, Streamlit, PyTorch, MongoDB, FastAPI"
        )

# Action Button
generate_btn = st.button("🚀 Generate 5 Project Ideas", type="primary", use_container_width=True)

# Generation and Display State
if "generated_projects" not in st.session_state:
    st.session_state.generated_projects = None

if generate_btn:
    if not domain_input.strip():
        st.error("Please specify a valid domain.")
    else:
        with st.spinner("🧠 AI Architect is synthesizing 5 tailored project ideas..."):
            try:
                results = generate_project_ideas(
                    provider=provider_code,
                    api_key=api_key_input.strip() if api_key_input else None,
                    domain=domain_input.strip(),
                    skill_level=skill_level,
                    time_limit=time_limit,
                    extra_interests=extra_interests.strip(),
                    project_type=project_type,
                    model=model_name
                )
                st.session_state.generated_projects = results
                st.session_state.current_meta = {
                    "domain": domain_input,
                    "skill_level": skill_level,
                    "time_limit": time_limit
                }
                st.success(f"✨ Successfully generated {len(results)} tailored project ideas!")
            except Exception as e:
                st.error(f"Generation error: {str(e)}")

# Display Generated Project Cards
if st.session_state.generated_projects:
    projects = st.session_state.generated_projects
    meta = st.session_state.get("current_meta", {})
    
    st.markdown(f"### 🎯 5 Project Ideas for **{meta.get('domain', '')}** ({meta.get('skill_level', '')} &bull; {meta.get('time_limit', '')})")
    
    # Helpful Scroll Hint
    st.markdown("""
    <div class="scroll-hint">
        👇 <strong>5 Project Cards Ready!</strong> Scroll down below to review each card, expand modules, and view evaluation tips.
    </div>
    """, unsafe_allow_html=True)
    
    # Export and Action Bar
    top_col1, top_col2 = st.columns([3, 1])
    with top_col2:
        json_str = json.dumps(projects, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"project_ideas_{meta.get('domain', 'projects').replace(' ', '_').lower()}.json",
            mime="application/json",
            use_container_width=True
        )

    # Render each project card
    for p in projects:
        difficulty = p.get("difficulty", "Intermediate")
        diff_class = f"badge-{difficulty.lower()}"
        
        with st.container():
            # Card header HTML
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                    <div>
                        <span class="badge {diff_class}">{difficulty}</span>
                        <span class="badge badge-time">⏱️ {p.get('estimated_time', '1-2 Weeks')}</span>
                        <h2 class="project-title" style="margin: 0.5rem 0 0.2rem 0; font-size: 1.45rem; font-weight: 700;">#{p.get('id', 1)} {p.get('title', 'Project Title')}</h2>
                        <p class="project-tagline" style="font-style: italic; font-size: 0.95rem; margin-bottom: 0.8rem;">"{p.get('tagline', '')}"</p>
                    </div>
                </div>
                
                <div class="project-body" style="margin-bottom: 0.8rem;">
                    <strong>📌 Problem Statement:</strong>
                    <p style="margin-top: 0.2rem; font-size: 0.93rem; line-height: 1.5;">{p.get('problem_statement', '')}</p>
                </div>
                
                <div class="project-body" style="margin-bottom: 0.8rem;">
                    <strong>👥 Target Audience:</strong>
                    <span style="font-size: 0.93rem;"> {p.get('target_audience', 'General Users')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Module Breakdown & Tech Details Expander
            with st.expander(f"🔍 Click to View Modules, Tech Stack & Evaluation Tip for Idea #{p.get('id', 1)}", expanded=False):
                mod_col1, mod_col2 = st.columns([1.3, 1])
                
                with mod_col1:
                    st.markdown("#### 🧩 Key System Modules")
                    modules = p.get("key_modules", [])
                    for idx, mod in enumerate(modules, start=1):
                        name = mod.get("module_name", f"Module {idx}")
                        desc = mod.get("description", "")
                        st.markdown(f"**{idx}. {name}**")
                        st.caption(desc)
                        
                    st.markdown("#### 🎯 Project Scope")
                    scope = p.get("scope", {})
                    in_scope = scope.get("in_scope", [])
                    out_scope = scope.get("out_of_scope", [])
                    
                    if in_scope:
                        st.markdown("**In-Scope (Deliverables):**")
                        for item in in_scope:
                            st.markdown(f"- ✅ {item}")
                    if out_scope:
                        st.markdown("**Out-of-Scope (Deferred):**")
                        for item in out_scope:
                            st.markdown(f"- ⏳ {item}")
                
                with mod_col2:
                    st.markdown("#### 🛠️ Recommended Tools & Stack")
                    tools = p.get("tools_and_technologies", {})
                    
                    if "frontend" in tools and tools["frontend"]:
                        st.markdown("**Frontend:**")
                        tags = " ".join([f"<span class='tech-tag'>{t}</span>" for t in tools["frontend"]])
                        st.markdown(tags, unsafe_allow_html=True)
                        
                    if "backend" in tools and tools["backend"]:
                        st.markdown("**Backend:**")
                        tags = " ".join([f"<span class='tech-tag'>{t}</span>" for t in tools["backend"]])
                        st.markdown(tags, unsafe_allow_html=True)
                        
                    if "database" in tools and tools["database"]:
                        st.markdown("**Database / Storage:**")
                        tags = " ".join([f"<span class='tech-tag'>{t}</span>" for t in tools["database"]])
                        st.markdown(tags, unsafe_allow_html=True)
                        
                    if "ai_or_apis" in tools and tools["ai_or_apis"]:
                        st.markdown("**AI / APIs:**")
                        tags = " ".join([f"<span class='tech-tag'>{t}</span>" for t in tools["ai_or_apis"]])
                        st.markdown(tags, unsafe_allow_html=True)
                        
                    if "key_libraries" in tools and tools["key_libraries"]:
                        st.markdown("**Key Libraries:**")
                        tags = " ".join([f"<span class='tech-tag'>{t}</span>" for t in tools["key_libraries"]])
                        st.markdown(tags, unsafe_allow_html=True)
                        
                    # Evaluation Winning Tip
                    tip = p.get("evaluation_winning_tip", "")
                    if tip:
                        st.markdown(f"""
                        <div class="tip-box">
                            <strong>🏆 10-Mark Presentation Tip:</strong><br/>
                            {tip}
                        </div>
                        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem 0;">
    Generative AI Mini Project &bull; Problem Statement #49: Project Idea Generator &bull; Designed for 10-Mark Evaluation
</div>
""", unsafe_allow_html=True)
