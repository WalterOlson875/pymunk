# pymunk

A Python physics simulation project using pymunk and pygame.

## Setup

### Option 1: Automated Setup with Git Hooks (Recommended)

This repository includes git hooks that automatically manage your Python virtual environment!

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pymunk
   ```

2. The `post-checkout` hook will automatically:
   - Create a virtual environment (`venv/`)
   - Install all dependencies from `requirements.txt`
   - Show you how to activate the environment

That's it! The git hooks will handle environment setup for you.

### Option 2: Manual Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pymunk
   ```

2. Set up git hooks (optional but recommended):
   ```bash
   ./setup-hooks.sh
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

Run the tutorial:
```bash
python tutorial.py
```

## Git Hooks Features

This repository includes automated git hooks that make development easier:

- **post-checkout**: Automatically sets up virtual environment and installs dependencies when you clone or switch branches
- **post-merge**: Updates dependencies when `requirements.txt` changes after `git pull` or merges  
- **pre-commit**: Checks your environment setup and provides helpful warnings before commits

### Manual Hook Installation

If the hooks didn't install automatically, run:
```bash
./setup-hooks.sh
```

## Dependencies

- pymunk: Python physics library
- pygame: Game development library
- cffi & pycparser: Dependencies for pymunk

## Development

### Activating Environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Updating Dependencies
```bash
pip freeze > requirements.txt
```

### Deactivating
```bash
deactivate
```
