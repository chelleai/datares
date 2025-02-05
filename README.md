# datares

## Setup Instructions

1. Install Miniconda
   - Download and install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
   - Follow the installation instructions for your operating system

2. Create and activate virtual environment
   ```bash
   # Create new environment named 'goose'
   conda create -n goose python=3.9
   
   # Activate the environment
   conda activate goose
   ```

3. Install required packages
   ```bash
   # Install packages using conda
   conda install -c conda-forge --file requirements.txt
   ```

Remember to always activate the 'goose' environment before working on the project:
```bash
conda activate goose
```
