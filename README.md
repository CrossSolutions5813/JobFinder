# JobFinder

**Discover your interests. Explore your future.**

JobFinder is a Windows desktop career-exploration app designed to feel welcoming to younger children without feeling childish to older kids and teens.

## Features

- Select one or more favorite school subjects.
- Answer progressively specific questions about interests, activities, personality, strengths, and work environments.
- Explore career matches and see why each career appeared.
- Open career profiles with a typical day, helpful skills, education and training, work settings, approximate U.S. pay, and related careers.
- Save a polished PDF report showing the choice path and career matches.
- Read the About and Privacy information from the Help menu.
- Responsive question scrolling and progress indicators.

## Branding

The JobFinder hat-and-question-mark logo is used on the home screen, PDF reports, and Windows executable icon. Logo assets are stored in `assets/`.

## Privacy

JobFinder does not create an online account, send answers to a server, or collect analytics. Answers stay in the app while it is running. Nothing is saved automatically. If a user chooses **Save results**, the app writes a PDF report to the location they select. That file can contain the selected subjects, answers, and career matches; keep it private if it includes a child's information.

The app opens an external website only when a user chooses a career-information link.

## Run from source

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Build a Windows executable

Run `build_windows.bat` on a Windows PC. It installs PyInstaller and creates:

`dist\JobFinder.exe`

The target computer does not need Python installed.

## Publish on GitHub

1. Create a repository named `JobFinder`.
2. Upload `main.py`, `requirements.txt`, `README.md`, `.gitignore`, and `build_windows.bat`.
3. Run the build script on Windows.
4. Create a GitHub Release and attach `dist\JobFinder.exe` or a ZIP containing it.
5. Share the repository for source code and the Release page for downloads.

## Career and salary information

Career profiles are educational summaries. Salary ranges are broad U.S. estimates, not guarantees or starting-pay promises. Actual pay varies by location, experience, employer, specialty, and work hours. Use the linked U.S. Bureau of Labor Statistics Occupation Finder for current occupation-specific information.

## Important note

JobFinder is an educational exploration tool, not a career aptitude test. A match is a conversation starter, not a prediction or limit on what someone can become.
