# CS Skins Marketplace Scraper

**Real-time marketplace scraper to track and find favorite items**

## 🛠 How It Works

Project designed to continuously monitoring multiple marketplaces in real time, instantly detecting new listings that match your filters. The system WILL:

1. **Scrape new listings** from supported marketplaces the moment they appear.
2. **Provide real-time insights** via the frontend, showing the newest listings as soon as they're available.
3. **Filter items** based on customizable criteria (e.g., price, condition, stickers, trade status, etc.).
4. **Display marketplace scraping status**, so you always know if data is up to date.

## Currently Supported Marketplaces

CSFloat, Skinport, SkinBid, DMarket

## Tech Stack

This project is built using modern technologies to ensure speed, scalability, and ease of deployment. Currently consisting of:

- **Backend:** Go (Gin, WebSockets)
- **Scraper:** Custom-built Python script (requests, websocket)
- **Frontend:** React (TypeScript)
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Testing:** TBD

## Upcoming Features

**Several Marketplaces Integrations** – Expanding support for additional platforms

**Advanced Filtering** – Define precise criteria for the perfect deals

**Price Tracking** – Monitor item prices over time to recognize undervalued listings

**Instant Notifications** – Alerts when a targeted item appears

**Item Base Price Indicator** – Calculate listing's real value

**WebSocket Live Updates** – See new listings pop up in real time

**Full API Support** – Integrate the scraper into your own projects

## Running Tests

TBD

## 📌 Status

Project still in development.

## 🚀 How to Run the App

You can run the project locally (each service on your host) or fully containerized using Docker Compose.

> **Note:**  
> Make sure your `.env` file in the root directory is set up with the correct environment variables for local development (see `.env.example`).

---

### Running Locally (Development)

**1. Database**

You need a running PostgreSQL instance.  
Create the database and table using the provided SQL script:

```bash
# Start your local PostgreSQL server
psql -U <your_user> -d <your_database> -f database/01_create_table.sql
```

**2. Backend**

```bash
cd backend
go mod tidy
go run main.go
```

**3. Frontend**

```bash
cd frontend
npm install
npm run dev
```

**4. Scrapers**

Open a terminal for each scraper you want to run:

```bash
cd scraper
pip install -r requirements.txt
python -m main_csfloat
python -m main_skinport
python -m main_dmarket
python -m main_skinbid
```

---

### Running with Docker Compose

This will start **all services** (database, backend, frontend, scrapers) in containers.

```bash
docker compose build --no-cache
docker compose up -d
```

- All environment variables are managed via the `.env` file and `docker-compose.yml`.
