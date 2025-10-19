# app/core/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = Field(default="Cricket Odds API", description="Application name")
    VERSION: str = Field(default="1.0.0", description="Application version")
    
    # Server configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes")
    
    # CORS configuration - reads from .env file
    # Format in .env: ALLOWED_DOMAINS=http://localhost,http://127.0.0.1,https://yourdomain.com
    ALLOWED_DOMAINS: str = Field(
        default="http://localhost,http://127.0.0.1",
        description="Comma-separated list of allowed domains for CORS"
    )
    
    # Scraping configuration
    BASE_URL: str = Field(
        default="https://api.radheexch.xyz",
        description="Base URL for cricket data API"
    )
    SCRAPE_INTERVAL: int = Field(
        default=3,
        description="How often to refresh live match data (in seconds)"
    )
    
    # Optional external integration
    LIVE_MATCH_ODDS_PUSH_URL: Optional[str] = Field(
        default=None,
        description="External webhook URL to push live match data"
    )
    
    # Proxy configuration (for cloud deployments to bypass IP blocking)
    USE_PROXY: bool = Field(
        default=False,
        description="Enable proxy for external API requests"
    )
    PROXY_URL: Optional[str] = Field(
        default=None,
        description="Proxy server URL (e.g., http://user:pass@proxy:port or ScraperAPI URL)"
    )
    SCRAPER_API_KEY: Optional[str] = Field(
        default=None,
        description="ScraperAPI key for proxy service (alternative to PROXY_URL)"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    @property
    def allowed_domains_list(self) -> List[str]:
        """Convert comma-separated ALLOWED_DOMAINS string to list"""
        if isinstance(self.ALLOWED_DOMAINS, str):
            return [domain.strip() for domain in self.ALLOWED_DOMAINS.split(',') if domain.strip()]
        return self.ALLOWED_DOMAINS
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
