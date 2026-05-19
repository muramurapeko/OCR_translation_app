# OCR Translation App

OCR Translation App is a lightweight application to capture screen regions, run OCR on images, and translate detected text — focused for research and experiments with local LLM/vision models.

## Features
- Capture a screen region or full screen using `core/screen_capture.py`.
- Extract text via OCR and pass it to translator modules in `core/`.
- Multiple translator implementations (`translator.py`, `translator2.py`, `translator3.py`, `translator4.py`) for experimentation.
- Minimal UI components under `ui/` for displaying OCR results and translations.

## Quickstart
Requirements: Python 3.10+ and a virtual environment.

1. Create and activate a venv:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies. This project contains model-related dependencies in `llama-models/requirements.txt`:

```bash
pip install -r llama-models/requirements.txt
```

3. Run the app:

```bash
python main.py
```

Notes:
- Ensure any local models are placed under the `models/` directory as expected by the code.
- Some translator implementations may require additional model files or API keys — check the specific translator file for details.

## Project Structure
- `main.py` — application entry point.
- `core/` — core modules:
  - `screen_capture.py` — screen capture helpers.
  - `translator*.py` — translator implementations.
  - `tempCodeRunnerFile.py` — temporary/test runner file.
- `ui/` — UI components for OCR and translation display.
- `models/` — place model files and related assets here.
- `llama-models/` — bundled model utilities and requirements used by some translator implementations.

## Usage Tips
- For quick experiments, run `main.py` and use the UI windows to capture regions.
- If results are empty, check the model paths in `models/` and confirm required tokenizer/model files exist.

## Contributing
Contributions and experiments welcome. Create issues or PRs on the main branch. Keep changes focused and include a short README update for any new features.

## License
See the repository `LICENSE` files included in `llama-models/` and subfolders for model and code licensing details.

---
Created for research and experimentation; contact the maintainer for model access or integration questions.
