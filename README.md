# University Research Opportunity Portal

A web application where faculty members can post, view, update and manage research opportunities in one place.
Built for Computer Networks, Assignment 1.

GitHub Repository: https://github.com/zafarkhan01/research-opportunity-portal

## Tech Stack

- Backend: Python (Flask), REST API
- Database: MySQL (XAMPP)
- Frontend: HTML, CSS, JavaScript
- API testing: Bruno

## Project Structure

```
research-opportunity-portal/
├── backend/        Flask API (app.py, db.py, requirements.txt, .env.example)
├── frontend/       index.html (frontend, talks to the API)
├── database/       schema.sql, sample_data.sql
├── postman/        Exported Bruno collection
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- XAMPP (MySQL and phpMyAdmin)
- A web browser

## Setup and Run Instructions (Windows)

### 1. Start MySQL

Open XAMPP Control Panel and click **Start** next to MySQL.

### 2. Create the database

1. Open http://localhost/phpmyadmin
2. Go to the **SQL** tab, paste the contents of `database/schema.sql` and click **Go**
3. (Optional) Run `database/sample_data.sql` the same way to add sample records

### 3. Configure the backend

1. Open the `backend` folder
2. Copy `.env.example` and rename the copy to `.env`
3. Default XAMPP values (empty password) are already in the example:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=research_portal
```

### 4. Install dependencies and start the server

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

On Linux or Mac, activate with `source venv/bin/activate`.

If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

The server runs at http://localhost:5000. Test it at http://localhost:5000/api/health

### 5. Open the frontend

Open `frontend/index.html` in a browser (double-click it). Keep the backend running.

## API Endpoints

| Method | Endpoint | Description | Success | Errors |
|---|---|---|---|---|
| POST | `/api/opportunities` | Create an opportunity | 201 | 400, 500 |
| GET | `/api/opportunities` | Get all opportunities | 200 | 500 |
| GET | `/api/opportunities/:id` | Get one opportunity | 200 | 404, 500 |
| PUT | `/api/opportunities/:id` | Update an opportunity | 200 | 400, 404, 500 |
| DELETE | `/api/opportunities/:id` | Delete an opportunity | 200 | 404, 500 |

### Opportunity fields

`id`, `title`, `description`, `research_area`, `faculty_name`, `department`, `required_skills`, `positions`, `deadline` (YYYY-MM-DD), `status` (`Open` or `Closed`)

### Status codes used

- 200 OK: request succeeded
- 201 Created: new opportunity created
- 400 Bad Request: missing or invalid data
- 404 Not Found: no opportunity with that ID
- 500 Internal Server Error: server or database problem

## API Testing

The Bruno collection is in the `postman/` folder. In Bruno, use **Open Collection** and select `postman/research-portal-api`. Start the backend first.

## Notes

- All data is stored in MySQL, nothing is hard-coded in the frontend.
- Credentials are kept in `.env`, which is not uploaded to GitHub. Use `.env.example` as a template.