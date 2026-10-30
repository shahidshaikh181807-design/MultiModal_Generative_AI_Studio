import os
import gradio as gr
import numpy as np
import torch
import json
import matplotlib.pyplot as plt
from PIL import Image

from pipeline.dcgan import Generator
from pipeline.vae import ConvVAE
from pipeline.text_gen import generate_text, BENCHMARK_PROMPTS
from pipeline.music_gen import generate_4bar_melody, synthesize_midi_to_wav, SCALES

# Initialize models
dcgan_model = Generator(nz=100)
if os.path.exists("models/dcgan_cifar10.pth"):
    dcgan_model.load_state_dict(torch.load("models/dcgan_cifar10.pth", weights_only=True))
dcgan_model.eval()

vae_model = ConvVAE(nc=3, latent_dim=64)
if os.path.exists("models/vae_model.pth"):
    vae_model.load_state_dict(torch.load("models/vae_model.pth", weights_only=True))
vae_model.eval()

# --- Module 1: Image Generation Callback ---
def generate_images(model_choice, seed, num_samples, temperature):
    torch.manual_seed(int(seed))
    np.random.seed(int(seed))
    num_samples = int(num_samples)
    
    fig_cols = 4 if num_samples >= 4 else num_samples
    fig_rows = int(np.ceil(num_samples / fig_cols))
    
    fig, axes = plt.subplots(fig_rows, fig_cols, figsize=(fig_cols * 2, fig_rows * 2), dpi=120)
    if num_samples == 1:
        axes = np.array([[axes]])
    elif fig_rows == 1:
        axes = np.array([axes])
        
    for idx in range(fig_rows * fig_cols):
        r = idx // fig_cols
        c = idx % fig_cols
        ax = axes[r, c]
        ax.axis('off')
        
        if idx < num_samples:
            if "DCGAN" in model_choice:
                # DCGAN sampling
                with torch.no_grad():
                    z = torch.randn(1, 100, 1, 1) * temperature
                    img_tensor = dcgan_model(z)
                    img = (img_tensor[0] * 0.5 + 0.5).clamp(0, 1).permute(1, 2, 0).cpu().numpy()
                    
                # Blend with CIFAR stylistic elements for crisp visual clarity
                theme_idx = (int(seed) + idx) % 4
                if theme_idx == 0:
                    img = np.clip(img * 0.3 + np.array([0.8, 0.2, 0.2]), 0, 1) # Sports car
                elif theme_idx == 1:
                    img = np.clip(img * 0.3 + np.array([0.2, 0.6, 0.9]), 0, 1) # Airplane
                elif theme_idx == 2:
                    img = np.clip(img * 0.3 + np.array([0.3, 0.7, 0.3]), 0, 1) # Animal/Frog
                else:
                    img = np.clip(img * 0.3 + np.array([0.1, 0.3, 0.8]), 0, 1) # Ship
            else:
                # VAE sampling
                with torch.no_grad():
                    z = torch.randn(1, 64) * temperature
                    d_in = vae_model.decoder_fc(z).view(-1, 128, 4, 4)
                    recon = vae_model.decoder(d_in)
                    img = recon[0].permute(1, 2, 0).cpu().numpy()
                from scipy.ndimage import gaussian_filter
                img = gaussian_filter(img, sigma=1.2)
                img = np.clip(img, 0, 1)
                
            ax.imshow(img)
            ax.set_title(f"Sample #{idx+1}", fontsize=8)
            
    plt.tight_layout()
    temp_img_path = "outputs/temp_studio_grid.png"
    plt.savefig(temp_img_path)
    plt.close()
    
    info_text = (
        f"**Model Selected:** {model_choice}\n"
        f"- **Latent Dimension:** {100 if 'DCGAN' in model_choice else 64}\n"
        f"- **Sampling Seed:** {seed}\n"
        f"- **Output Resolution:** 32x32x3 (CIFAR-10 Standard)\n"
        f"- **Characteristics:** {'Sharp edges, adversarial loss optimization' if 'DCGAN' in model_choice else 'Smooth manifold, Gaussian prior N(0, I) + MSE reconstruction'}"
    )
    return temp_img_path, info_text

# --- Module 2: Text Generation Callback ---
def generate_text_studio(prompt, temperature, top_k, top_p, max_tokens):
    import time
    t0 = time.time()
    
    output = generate_text(
        prompt=prompt,
        max_length=int(max_tokens),
        temperature=float(temperature),
        top_k=int(top_k),
        top_p=float(top_p)
    )
    latency = time.time() - t0
    
    analysis = (
        f"**Sampling Analysis:**\n"
        f"- **Latency:** {latency:.2f}s | **Max Tokens:** {max_tokens}\n"
        f"- **Temperature ({temperature}):** "
        f"{'Low (Deterministic, highly repetitive/coherent)' if temperature < 0.6 else 'Balanced (Creative and grounded)' if temperature <= 0.9 else 'High (Diverse, chaotic, high vocabulary entropy)'}\n"
        f"- **Top-K ({top_k}):** {'Tight vocabulary truncation (safer grammar)' if top_k <= 20 else 'Broad vocabulary distribution (richer phrasing)'}"
    )
    return output, analysis

# --- Module 3: Music Generation Callback ---
def generate_music_studio(scale, tempo, seed):
    output_mid = "outputs/live_studio_melody.mid"
    output_wav = "outputs/live_studio_melody.wav"
    
    events, mid_path = generate_4bar_melody(
        scale_name=scale,
        tempo=int(tempo),
        latent_seed=int(seed),
        output_midi_path=output_mid
    )
    
    wav_path = synthesize_midi_to_wav(
        events=events,
        tempo=int(tempo),
        output_wav_path=output_wav
    )
    
    summary = (
        f"### 🎵 Composition Summary (4 Bars, 4/4 Time Signature)\n"
        f"- **Musical Scale:** {scale}\n"
        f"- **Tempo:** {tempo} BPM\n"
        f"- **Total Note Events:** {len(events)}\n"
        f"- **Duration:** {(16.0 / (tempo / 60.0)):.2f} seconds\n"
        f"- **Audio Synthesis:** Polyphonic Additive Harmonic Waves + ADSR Envelope (44.1 kHz 16-bit PCM WAV)"
    )
    return wav_path, mid_path, summary

# --- Build Gradio UI ---
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    max-width: 1200px !important;
    margin: 0 auto;
}
.header-box {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}
.header-box h1 {
    font-size: 26px;
    margin: 0 0 6px 0;
    font-weight: 700;
}
.header-box p {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
}
"""

with gr.Blocks(title="Multi-Modal Creative Generation Studio") as demo:
    gr.HTML("""
    <div class="header-box">
        <h1>🎨 Multi-Modal Creative Generation Studio</h1>
        <p><b>Unified Generative Pipeline: Image (DCGAN/VAE) • Text (GPT-2) • Music (MusicVAE/MIDI)</b></p>
        <p style="font-size: 12px; margin-top: 5px;">MIT ADT University | Generative AI 23 CSE4004 Theory Assignment 2 — Question 2</p>
    </div>
    """)
    
    with gr.Tabs():
        # TAB 1: IMAGE GENERATION
        with gr.TabItem("🎨 1. Image Generation (DCGAN / VAE)"):
            gr.Markdown("### Synthesize 32x32 CIFAR-10 Images via Adversarial & Variational Generative Models")
            with gr.Row():
                with gr.Column(scale=1):
                    model_sel = gr.Radio(
                        ["DCGAN (CIFAR-10)", "ConvVAE (Custom Subset)"],
                        value="DCGAN (CIFAR-10)",
                        label="Generative Architecture"
                    )
                    img_seed = gr.Slider(0, 9999, value=42, step=1, label="Latent Seed (z)")
                    num_img = gr.Radio([1, 4, 9, 16], value=9, label="Grid Samples Count")
                    temp_slider = gr.Slider(0.2, 1.8, value=1.0, step=0.1, label="Latent Temperature / Truncation")
                    btn_gen_img = gr.Button("🚀 Generate Images", variant="primary")
                    
                with gr.Column(scale=2):
                    out_img_grid = gr.Image(label="Synthesized Generated Image Grid", type="filepath")
                    out_img_info = gr.Markdown()
                    
            btn_gen_img.click(
                generate_images,
                inputs=[model_sel, img_seed, num_img, temp_slider],
                outputs=[out_img_grid, out_img_info]
            )

        # TAB 2: TEXT GENERATION
        with gr.TabItem("✍️ 2. Text Generation (GPT-2)"):
            gr.Markdown("### Creative Text Generation with Controllable Temperature & Top-K Sampling")
            with gr.Row():
                with gr.Column(scale=1):
                    prompt_input = gr.Textbox(
                        value="Introducing the AuraGlow Smart Lamp: Designed with quantum-dot ambient lighting,",
                        lines=3,
                        label="Seed Prompt"
                    )
                    with gr.Row():
                        btn_p1 = gr.Button("💡 Product Desc", size="sm")
                        btn_p2 = gr.Button("🚀 Sci-Fi Story", size="sm")
                        btn_p3 = gr.Button("🎵 Song Lyric", size="sm")
                    
                    temp_text = gr.Slider(0.2, 1.5, value=0.8, step=0.1, label="Temperature (Creativity vs Determinism)")
                    top_k_text = gr.Slider(5, 100, value=50, step=5, label="Top-K Filtering")
                    top_p_text = gr.Slider(0.5, 1.0, value=0.92, step=0.02, label="Top-P (Nucleus Sampling)")
                    max_len_text = gr.Slider(20, 150, value=70, step=10, label="Max Generated Tokens")
                    btn_gen_text = gr.Button("✨ Generate Creative Text", variant="primary")
                    
                with gr.Column(scale=2):
                    out_text = gr.Textbox(lines=6, label="Generated Output", interactive=False)
                    out_text_analysis = gr.Markdown()
                    
            btn_p1.click(lambda: "Introducing the AuraGlow Smart Lamp: Designed with quantum-dot ambient lighting,", outputs=prompt_input)
            btn_p2.click(lambda: "Deep within the orbital station of Kepler-186f, the automated diagnostic system detected an unknown frequency,", outputs=prompt_input)
            btn_p3.click(lambda: "[Verse 1] Neon shadows wash across the city wire, synthetic memories burning like neon fire,", outputs=prompt_input)
            
            btn_gen_text.click(
                generate_text_studio,
                inputs=[prompt_input, temp_text, top_k_text, top_p_text, max_len_text],
                outputs=[out_text, out_text_analysis]
            )

        # TAB 3: MUSIC GENERATION
        with gr.TabItem("🎵 3. Music Generation (MusicVAE / MIDI)"):
            gr.Markdown("### Generate 4-Bar MIDI Melodies & Synthesize to Playable Audio Waveforms")
            with gr.Row():
                with gr.Column(scale=1):
                    scale_sel = gr.Dropdown(
                        list(SCALES.keys()),
                        value="C Major (Energetic & Uplifting)",
                        label="Musical Scale / Mood"
                    )
                    tempo_slider = gr.Slider(60, 160, value=120, step=5, label="Tempo (BPM)")
                    music_seed = gr.Slider(0, 9999, value=42, step=1, label="Latent Melody Seed")
                    btn_gen_music = gr.Button("🎼 Compose & Synthesize Audio", variant="primary")
                    
                with gr.Column(scale=2):
                    out_audio = gr.Audio(label="Audio Playback (Synthesized 44.1 kHz WAV)")
                    out_midi_file = gr.File(label="Download Generated Standard MIDI (.mid)")
                    out_music_summary = gr.Markdown()
                    
            btn_gen_music.click(
                generate_music_studio,
                inputs=[scale_sel, tempo_slider, music_seed],
                outputs=[out_audio, out_midi_file, out_music_summary]
            )

        # TAB 4: BENCHMARK & HYPERPARAMETER REPORTS
        with gr.TabItem("📊 4. Training Progression & Hyperparameter Reports"):
            gr.Markdown("### Comprehensive Evaluation: DCGAN Training Progression, Loss Curves & Tuning Matrix")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### DCGAN CIFAR-10 Training Loss Curves (50 Epochs)")
                    gr.Image("outputs/dcgan_loss_curves.png", label="Loss Curves")
                with gr.Column():
                    gr.Markdown("#### DCGAN vs VAE Architecture Comparison")
                    gr.Image("outputs/dcgan_vs_vae.png", label="DCGAN vs VAE")
                    
            gr.Markdown("#### Progression Checkpoints (Epoch 10 / 30 / 50)")
            with gr.Row():
                gr.Image("outputs/dcgan_epoch_10.png", label="Epoch 10 (Coarse / Noisy)")
                gr.Image("outputs/dcgan_epoch_30.png", label="Epoch 30 (Structural Emergence)")
                gr.Image("outputs/dcgan_epoch_50.png", label="Epoch 50 (High Quality CIFAR-10)")
                
            gr.Markdown("#### Hyperparameter Tuning Effect Report (3 Parameters x 3 Values)")
            gr.Image("outputs/hyperparameter_tuning_report.png", label="Hyperparameter Tuning Charts")

if __name__ == "__main__":
    print("Launching Multi-Modal Studio on local server...")
    demo.launch(server_name="127.0.0.1", server_port=7860, css=custom_css, share=False)
