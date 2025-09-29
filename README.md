# MERI DIET - A Personalized Diet Planning Web Application

MERI DIET is a full-stack web application built with Django that allows users to generate, manage, and follow personalized diet plans. It features an AI-powered chatbot for custom plans and a library of pre-made diet charts for various health goals, all deployed live on a cloud platform.

### Live Demo: **[https://meri-diet.onrender.com/](https://meri-diet.onrender.com/)**



---

## Key Features

* **Secure User Authentication:** Full user registration (with email and phone number), login, and logout system.
* **AI Chatbot for Personalized Plans:** An interactive form that gathers user metrics (age, weight, height), goals, food preferences, and health conditions (like Diabetes, High BP, etc.) to generate a tailored diet plan.
* **Browseable Diet Library:** A collection of expert-curated, pre-made diet plans for different objectives such as Weight Loss, Muscle Gain, and General Wellness.
* **Personal Dashboard ("My Diet List"):** A central hub where users can view all their saved plans in a clean, collapsible accordion layout.
* **Full Plan Management:** Users can add plans from the AI chatbot or the public library to their personal list and can delete any plan at any time.
* **Auto-Expiring Plans:** A dynamic system where any plan with "7-Day" in its title is automatically removed from a user's list after 7 days, with a dashboard notification 24 hours before deletion.
* **Dynamic UI:** The user interface, including the main "GET STARTED" button and the navigation bar, changes intelligently based on the user's login status.
* **Static Pages:** Includes professional Support, Privacy Policy, and Terms & Conditions pages to build user trust.
* **Responsive Design:** The UI is built with Bootstrap 5 and custom CSS, making it fully responsive for both desktop and mobile devices.

---

## Technology Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Database:** PostgreSQL (Production), SQLite3 (Development)
* **Web Server:** Gunicorn
* **Static Files:** WhiteNoise
* **Deployment:** Render
* **Version Control:** Git & GitHub

---

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have Python and Git installed on your system.
* Python 3.10+
* pip
* git

### Installation

1.  **Clone the repo**
    ```sh
    git clone [https://github.com/Soyam14/meri-diet-project.git](https://github.com/Soyam14/meri-diet-project.git)
    ```
2.  **Navigate to the project directory**
    ```sh
    cd meri-diet-project
    ```
3.  **Create and activate a virtual environment**
    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  **Install the required packages**
    ```sh
    pip install -r requirements.txt
    ```
5.  **Apply database migrations**
    ```sh
    python manage.py migrate
    ```
6.  **Create a superuser (for admin access)**
    ```sh
    python manage.py createsuperuser
    ```
7.  **Run the development server**
    ```sh
    python manage.py runserver
    ```
    Your project will be available at `http://127.0.0.1:8000/`.

---

## Deployment

This application is configured for production deployment on Render. Key settings such as `SECRET_KEY`, `DEBUG`, and `DATABASE_URL` are managed via environment variables for security. The build process automatically handles static file collection and database migrations.
