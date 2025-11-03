# 🐍 Flask Production Deployment & Hybrid Database Model

**Project Goal:** To build a robust, production-ready Flask application while mastering the transition from local development to a secure, professional cloud environment.

***

###  Key Technical Achievement: Hybrid Deployment Architecture

The most significant achievement of this project is the implementation of a **seamless, dual-database environment**, enabling clean development and secure production.

* **Zero-Edit Workflow:** The application code automatically detects its execution environment:
    * **Local Development (`FLASK_ENV=development`):** Connects to a local **SQLite** database and loads all secrets from the local `.env` file.
    * **Production (DigitalOcean App Platform):** Connects to a **Managed MySQL Cluster** using secure, injected environment variables.

* **Security:** All sensitive data (database URI, SECRET\_KEY, API keys) are stored outside the codebase via **Encrypted Environment Variables** on DigitalOcean. Passwords are secured using **scrypt hashing** via `werkzeug.security`.

***

###  Core Functionality & Features

The live application demonstrates standard and external service integrations:

* **Robust Authentication:** Features full user sign-up and login capabilities with detailed feedback:
    * Validation checks if a **username or email is already taken** during registration.
    * Login validation handles scenarios where **no user exists** or the **password is incorrect**.
* **Twitch API Integration:** Connects to the Twitch API to **check if a specified streamer is live**.
* **Email Notifications:** Sends an email notification to the administrator upon new user sign-up.
* **Titanfall Network Database:** Table of all 400000+ Networks in titanfall.

***

### ⚙️ Get Started Locally

To run this application locally and begin development:

1.  **Setup:** Activate your virtual environment and install dependencies.
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run:** Set the development flag and start the server.
    ```bash
    $env:FLASK_ENV="development"
    flask run
    ```
3.  **Initialize DB (One-Time):** If running for the first time, open a separate terminal to create tables:
    ```bash
    flask shell
    # >>> from app import db; with app.app_context(): db.create_all()
    ```
