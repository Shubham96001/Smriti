<div align="center">

# 🧠 SmritiSaathi
**An elderly-friendly platform for cognitive games, memory notes, routine reminders, and consent-based caregiver support.**

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

*Developed for the MEDHA Hackathon Problem Statement*

<br>

> **Intended Use & Assessment Notice:** The application provides supportive activities and organization tools. It is **not** a diagnostic medical system. The seeded English items under `placeholder-v1` are generic development placeholders, not the real RUDAS. They have no clinical scoring or diagnostic interpretation.
</div>

---

## 📖 What is SmritiSaathi? (Project Details)

SmritiSaathi (meaning "Memory Companion") is a comprehensive digital platform specifically designed to support elderly individuals, particularly those navigating cognitive decline or early-stage dementia. 

The goal of this project is to foster independence for patients while providing peace of mind for their families. It bridges the gap between daily cognitive exercises and structured caregiving through an accessible, elderly-friendly interface.

**How it helps:**
*   **For Patients:** Offers a simplified dashboard to play adaptive cognitive games (like Memory Match), read personal memory notes, and view daily routine reminders.
*   **For Caregivers:** Provides a secure, consent-based portal to monitor activity, send reminders, and stay connected with the patient's daily routine.
*   **Accessibility First:** Features large touch targets, keyboard focus indicators, and a forgiving UI designed for users with limited digital literacy or physical dexterity.

---

## 🛠️ Technology & Architecture

*   **Frontend:** React, Vite, and plain CSS.
*   **Backend:** Python, FastAPI, Pydantic, psycopg, and PostgreSQL. 
*   **Security:** Passwords use `bcrypt` and access tokens use signed HS256 JWTs.

## 📂 Repository Map

*   `backend/`: New backend modules are flat domain packages.
*   `backend/sql/`: Contains PostgreSQL migrations.
*   `frontend/src/`: Frontend routes, contexts, games, services, offline support, and styles.
*   `docs/`: Project documentation (`architecture.md`, `api.md`, `security.md`, `demo.md`).
*   `tests/`: Integration and unit tests.
*   *Note: The retired nested backend files and local database files remain pending cleanup.*

---

## 🚀 Environment Setup & Configuration

**System Requirements:**
*   Python 3.10 or newer
*   Node.js 20.19+ or 22.12+ and npm
*   Local PostgreSQL server
*   Current browser with IndexedDB support for offline scaffolding

### 1️⃣ Backend Setup
1. From the repository root, create and activate a virtual environment, then install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

### 2️⃣ Frontend Setup
From the `frontend/` directory, install packages and start Vite:
   ```bash
   cd frontend
   npm install
   npm run dev
