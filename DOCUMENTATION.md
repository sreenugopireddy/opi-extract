1. Local Setup Guide (The “How-To”)
 Prerequisites

Python 3.10+ installed

Git installed

 Steps to run locally

Clone the repository

git clone https://github.com/<your-username>/opti-extract.git
cd opti-extract


Create and activate a virtual environment

Windows:

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1



Install dependencies

pip install -r requirements.txt


Run the FastAPI server

python -m uvicorn app.main:app --reload


Dependencies (as listed in requirements.txt)

fastapi

uvicorn

sqlalchemy

aiosqlite

python-multipart

pydantic

 2. Project Overview & Rationale (The “Why”)
 Project Overview


This project simulates a file ingestion services It allows users to upload files through a web interface. The backend stores the file locally with a unique system-generated name and records metadata in an SQLite database, which can be viewed from a separate page.

Project Structure

app/ — all backend code (FastAPI routes, database models, etc.)

templates/ — HTML frontend pages

static/ — CSS and JavaScript files

uploaded_files/ — local directory where uploaded files are stored

requirements.txt — dependency list

DOCUMENTATION.md — project setup and explanation

Explain that you separated logic (models, CRUD, routes) for clarity and maintainability.

Design Choices

a. Unique System Filename:
— it prevents filename conflicts when multiple users upload files with the same name, and it’s lightweight and guaranteed unique.
Example: uuid.uuid4().hex + original_extension

b. File & Database Synchronization:

If the DB write fails, you delete the saved file — this keeps the system consistent.

Installing dependencies on Windows PowerShell

Fixing environment activation issues

Handling file read/write safely in FastAPI

Avoiding memory overload by reading uploads in chunks

Ensuring the history page updates properly
