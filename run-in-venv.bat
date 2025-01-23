@echo off

REM Check if virtual environment exists
IF NOT EXIST ".venv\" (
    echo Virtual environment not found, creating...
    python -m venv .venv
) ELSE (
    echo Virtual environment found.
)

REM Activate the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Check if frontend libraries are installed
python -c "import sys; try: import streamlit, pandas, xlsxwriter; except ImportError: sys.exit(1)" >nul 2>&1
IF %ERRORLEVEL% EQU 1 (
    echo One or more frontend libraries are missing, installing from requirements-frontend.txt...
    python -m pip install -r requirements-frontend.txt
) ELSE (
    echo All frontend libraries are installed
)

REM Check if backend libraries are installed
python -c "import sys; try: import azure.storage.blob, langchain, openai, langchain_openai, azure.identity, langchain_community.retrievers, azure.search.documents, azure.core.credentials, langchain_text_splitters; except ImportError: sys.exit(1)" >nul 2>&1
IF %ERRORLEVEL% EQU 1 (
    echo One or more backend libraries are missing, installing from requirements-backend.txt...
    python -m pip install -r requirements-backend.txt
) ELSE (
    echo All backend libraries are installed.
)