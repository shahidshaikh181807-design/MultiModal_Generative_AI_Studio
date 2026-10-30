import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvVAE(nn.Module):
    def __init__(self, nc=3, latent_dim=64):
        super(ConvVAE, self).__init__()
        self.latent_dim = latent_dim
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(nc, 32, kernel_size=4, stride=2, padding=1), # 16x16
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=1), # 8x8
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1), # 4x4
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        self.fc_mu = nn.Linear(128 * 4 * 4, latent_dim)
        self.fc_logvar = nn.Linear(128 * 4 * 4, latent_dim)
        
        # Decoder
        self.decoder_fc = nn.Linear(latent_dim, 128 * 4 * 4)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1), # 8x8
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1), # 16x16
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.ConvTranspose2d(32, nc, kernel_size=4, stride=2, padding=1), # 32x32
            nn.Sigmoid()
        )
        
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        features = self.encoder(x)
        features = features.view(features.size(0), -1)
        mu = self.fc_mu(features)
        logvar = self.fc_logvar(features)
        z = self.reparameterize(mu, logvar)
        d_in = self.decoder_fc(z).view(-1, 128, 4, 4)
        recon_x = self.decoder(d_in)
        return recon_x, mu, logvar

    def sample(self, num_samples=16, device="cpu"):
        with torch.no_grad():
            z = torch.randn(num_samples, self.latent_dim).to(device)
            d_in = self.decoder_fc(z).view(-1, 128, 4, 4)
            samples = self.decoder(d_in)
            return samples.permute(0, 2, 3, 1).cpu().numpy()

def vae_loss_function(recon_x, x, mu, logvar):
    recon_loss = F.mse_loss(recon_x, x, reduction='sum')
    # Kingma and Welling: -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    kld = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + kld, recon_loss, kld
