//! Alpaca Markets REST client stub — extend when promoting a strategy.

use serde::Deserialize;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AlpacaError {
    #[error("missing API credentials")]
    MissingCredentials,
    #[error("http error: {0}")]
    Http(#[from] reqwest::Error),
}

#[derive(Debug, Clone, Deserialize)]
pub struct AlpacaConfig {
    pub api_key: String,
    pub secret_key: String,
    pub base_url: String,
}

impl AlpacaConfig {
    pub fn from_env() -> Result<Self, AlpacaError> {
        let api_key = std::env::var("ALPACA_API_KEY").map_err(|_| AlpacaError::MissingCredentials)?;
        let secret_key =
            std::env::var("ALPACA_SECRET_KEY").map_err(|_| AlpacaError::MissingCredentials)?;
        let base_url = match std::env::var("ALPACA_ENV").as_deref() {
            Ok("live") => "https://api.alpaca.markets".to_string(),
            _ => "https://paper-api.alpaca.markets".to_string(),
        };
        Ok(Self {
            api_key,
            secret_key,
            base_url,
        })
    }
}

#[derive(Debug, Clone)]
pub struct AlpacaClient {
    config: AlpacaConfig,
    http: reqwest::Client,
}

impl AlpacaClient {
    pub fn new(config: AlpacaConfig) -> Self {
        Self {
            config,
            http: reqwest::Client::new(),
        }
    }

    pub fn from_env() -> Result<Self, AlpacaError> {
        Ok(Self::new(AlpacaConfig::from_env()?))
    }

    pub fn base_url(&self) -> &str {
        &self.config.base_url
    }

    /// Health check: account endpoint (not yet implemented).
    pub async fn ping(&self) -> Result<(), AlpacaError> {
        let _ = (&self.config, &self.http);
        Ok(())
    }
}
