"""Configuration management for BookOutlet-Goodreads matcher."""

from .loader import load_config
from .schema import Config

__all__ = ['load_config', 'Config']
