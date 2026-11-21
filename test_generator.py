"""
Automated Test Suite for Project Idea Generator (Problem #49)
Runs 5 distinct test cases across diverse domains, skill levels, and timeframes.
Saves JSON outputs into `sample_outputs/` directory.
"""

import os
import json
import logging
from generator import generate_project_ideas

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

TEST_CASES = [
    {
        "id": 1,
        "name": "healthcare_telemedicine",
        "domain": "Healthcare & Telemedicine",
        "skill_level": "Beginner",
        "time_limit": "1-2 Weeks",
        "extra_interests": "Python, Streamlit, Free APIs",
        "project_type": "Full-Stack Web App"
    },
    {
        "id": 2,
        "name": "cybersecurity_threat_detection",
        "domain": "Cybersecurity & Threat Detection",
        "skill_level": "Intermediate",
        "time_limit": "1 Month",
        "extra_interests": "FastAPI, Packet Analysis, Log Parsing",
        "project_type": "Monitoring & Automation"
    },
    {
        "id": 3,
        "name": "edtech_personalized_learning",
        "domain": "EdTech & Personalized Learning",
        "skill_level": "Advanced",
        "time_limit": "3 Months",
        "extra_interests": "LangChain, Vector DB, RAG, PyTorch",
        "project_type": "Conversational RAG / Assistant"
    },
    {
        "id": 4,
        "name": "fintech_fraud_detection",
        "domain": "FinTech & Fraud Detection",
        "skill_level": "Intermediate",
        "time_limit": "1-2 Weeks",
        "extra_interests": "Scikit-Learn, Pandas, Plotly Dash",
        "project_type": "AI/ML Model & API"
    },
    {
        "id": 5,
        "name": "environmental_sustainability",
        "domain": "Environmental Sustainability & Smart Energy",
        "skill_level": "Beginner",
        "time_limit": "2-3 Weeks",
        "extra_interests": "Streamlit, OpenWeather API, Solar Data",
        "project_type": "Full-Stack Web App"
    }
]

def run_tests():
    output_dir = os.path.join(os.path.dirname(__file__), "sample_outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info("Starting test execution for 5 sample inputs...")
    total_passed = 0

    for tc in TEST_CASES:
        logger.info(f"--- Running Test Case {tc['id']}: {tc['domain']} ({tc['skill_level']}, {tc['time_limit']}) ---")
        
        projects = generate_project_ideas(
            provider="fallback",  # Deterministic test execution
            domain=tc["domain"],
            skill_level=tc["skill_level"],
            time_limit=tc["time_limit"],
            extra_interests=tc["extra_interests"],
            project_type=tc["project_type"]
        )
        
        # Assertions
        assert isinstance(projects, list), f"Test Case {tc['id']} failed: Output is not a list"
        assert len(projects) == 5, f"Test Case {tc['id']} failed: Expected 5 ideas, got {len(projects)}"
        
        for idx, p in enumerate(projects, 1):
            assert "title" in p, f"Project {idx} missing 'title'"
            assert "tagline" in p, f"Project {idx} missing 'tagline'"
            assert "difficulty" in p, f"Project {idx} missing 'difficulty'"
            assert "key_modules" in p and len(p["key_modules"]) >= 3, f"Project {idx} missing adequate key_modules"
            assert "tools_and_technologies" in p, f"Project {idx} missing 'tools_and_technologies'"
            assert "scope" in p, f"Project {idx} missing 'scope'"
            assert "evaluation_winning_tip" in p, f"Project {idx} missing 'evaluation_winning_tip'"

        # Save to file
        file_path = os.path.join(output_dir, f"test_case_{tc['id']}_{tc['name']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "test_case_metadata": tc,
                "generated_ideas_count": len(projects),
                "projects": projects
            }, f, indent=2)
            
        logger.info(f"Test Case {tc['id']} PASSED! Output saved to: {file_path}")
        total_passed += 1

    print("\n" + "=" * 60)
    print(f"TEST SUITE SUMMARY: {total_passed}/{len(TEST_CASES)} TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_tests()
