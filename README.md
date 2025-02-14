# Goose Evaluation by DataRes

## Installation

1. Install `uv`
    - For Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - For MacOS: `brew install uv`
    - For Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Ensure you're using Python 3.12
    - `uv python install 3.12`
3. Install the dependencies, namely Goose
    - `uv sync --all-extras`
4. Populate your `.env` file
    - The Gemini API key will be provided to you

## Getting Started

Check out the examples in the `examples` folder for some basic use-cases for Goose (and some more advanced ones!).

To run an example: `uv run python examples/<example>.py`.

To start, try running the Meal Planner example: `uv run python examples/generate_meal_plan.py`

## A Good Starting Point

- [ ] `examples/generate_meal_plan.py`
- [ ] `examples/refine_meal_plan.py`

Create you own refine_meal_plan.py file that updates lunch and dinner after creating the new breakfast.

## Next Steps

Identify a domain that is of interest to you and create a new example file that demonstrates how to use Goose to solve a problem in that domain.

Goose can support document upload.