import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

_model = None
_tokenizer = None

def load_gpt2_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        model_name = "gpt2"
        _tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        _model = GPT2LMHeadModel.from_pretrained(model_name)
        _model.eval()
        if _tokenizer.pad_token is None:
            _tokenizer.pad_token = _tokenizer.eos_token
    return _model, _tokenizer

def generate_text(prompt, max_length=80, temperature=0.8, top_k=50, top_p=0.92, repetition_penalty=1.2, seed=None):
    model, tokenizer = load_gpt2_model()
    if seed is not None:
        torch.manual_seed(seed)
    
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]
    
    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_length,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            pad_token_id=tokenizer.eos_token_id
        )
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_text

# The 5 designated benchmark experiments required by Assignment 2:
BENCHMARK_PROMPTS = [
    {
        "id": 1,
        "category": "Creative Product Description",
        "prompt": "Introducing the AuraGlow Smart Lamp: Designed with quantum-dot ambient lighting,",
        "temperature": 0.5,
        "top_k": 10,
        "focus": "High Coherence & Low Hallucination"
    },
    {
        "id": 2,
        "category": "Creative Sci-Fi Story",
        "prompt": "Deep within the orbital station of Kepler-186f, the automated diagnostic system detected an unknown frequency,",
        "temperature": 0.8,
        "top_k": 50,
        "focus": "Balanced Creativity & Plot Consistency"
    },
    {
        "id": 3,
        "category": "Song Lyrics (Cyberpunk)",
        "prompt": "[Verse 1] Neon shadows wash across the city wire, synthetic memories burning like neon fire,",
        "temperature": 1.2,
        "top_k": 50,
        "focus": "Maximum Expressiveness & Rhyme Variance"
    },
    {
        "id": 4,
        "category": "E-Commerce Promotional Campaign",
        "prompt": "Exclusive Summer Tech Festival: Upgrade your creative workspace today with",
        "temperature": 0.5,
        "top_k": 50,
        "focus": "Structured Marketing Copy & High Precision"
    },
    {
        "id": 5,
        "category": "Fantasy Worldbuilding Narrative",
        "prompt": "The ancient Archivist opened the celestial grimoire, where constellations were inscribed in molten silver,",
        "temperature": 1.2,
        "top_k": 10,
        "focus": "Constrained High-Temperature Vocabulary"
    }
]
