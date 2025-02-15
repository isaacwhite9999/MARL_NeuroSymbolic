# tests/test_pipeline.py

import pytest
from app.pipeline import run_pipeline

def test_pipeline_runs():
    """
    Test that the pipeline runs without errors.
    """
    # Run with a minimal number of episodes for testing
    run_pipeline(num_episodes=1, epsilon=0.1)
