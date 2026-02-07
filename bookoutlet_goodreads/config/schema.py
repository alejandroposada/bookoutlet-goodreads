"""Configuration schema using Pydantic for validation."""

from typing import Literal
from pydantic import BaseModel, Field, field_validator


class MatchingWeights(BaseModel):
    """Fuzzy matching algorithm weights (must sum to 1.0)."""
    ratio: float = Field(default=0.15, ge=0.0, le=1.0)
    partial_ratio: float = Field(default=0.20, ge=0.0, le=1.0)
    token_sort_ratio: float = Field(default=0.25, ge=0.0, le=1.0)
    token_set_ratio: float = Field(default=0.40, ge=0.0, le=1.0)

    @field_validator('token_set_ratio')
    @classmethod
    def validate_sum(cls, v, info):
        """Ensure all weights sum to 1.0."""
        values = info.data
        total = values.get('ratio', 0) + values.get('partial_ratio', 0) + values.get('token_sort_ratio', 0) + v
        if abs(total - 1.0) > 0.001:  # Allow small floating point errors
            raise ValueError(f'Weights must sum to 1.0, got {total}')
        return v


class MatchingConfig(BaseModel):
    """Matching algorithm configuration."""
    threshold: int = Field(default=90, ge=0, le=100)
    use_isbn: bool = Field(default=True)
    require_author_match: bool = Field(default=False, description="Require author similarity > 50% for fuzzy matches")
    weights: MatchingWeights = Field(default_factory=MatchingWeights)


class ParallelConfig(BaseModel):
    """Parallel processing configuration."""
    enabled: bool = Field(default=True)
    workers: int = Field(default=5, ge=1, le=20)
    delay_ms: int = Field(default=100, ge=0, le=5000, description="Delay between requests in milliseconds")


class InputConfig(BaseModel):
    """Input file configuration."""
    csv_path: str = Field(default="goodreads_library_export.csv")
    bookshelf: str = Field(default="to-read")


class OutputConfig(BaseModel):
    """Output configuration."""
    path: str = Field(default="output")
    format: Literal["text", "json", "csv", "markdown", "html"] = Field(default="text")


class DisplayConfig(BaseModel):
    """Display configuration."""
    show_progress: bool = Field(default=True)
    color: bool = Field(default=True)
    verbose: bool = Field(default=False)


class Config(BaseModel):
    """Main configuration model."""
    input: InputConfig = Field(default_factory=InputConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    matching: MatchingConfig = Field(default_factory=MatchingConfig)
    parallel: ParallelConfig = Field(default_factory=ParallelConfig)
    display: DisplayConfig = Field(default_factory=DisplayConfig)
