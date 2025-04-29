# CS Skins Marketplace Scraper

**Real-time marketplace scraper to track and find favorite items**

## 🛠 How It Works

Project designed to continuously monitoring multiple marketplaces in real time, instantly detecting new listings that match your filters. The system WILL:

1. **Scrape new listings** from supported marketplaces the moment they appear.
2. **Provide real-time insights** via the frontend, showing the newest listings as soon as they're available.
3. **Filter items** based on customizable criteria (e.g., price, condition, stickers, trade status, etc.).
4. **Display marketplace scraping status**, so you always know if data is up to date.

## Currently Supported Marketplaces

CSFloat, Skinport

## Tech Stack

This project is built using modern technologies to ensure speed, scalability, and ease of deployment. Currently consisting of:

- **Backend:** Go (Gin, WebSockets)
- **Scraper:** Custom-built Python script with requests/websocket
- **Frontend:** React (TypeScript)
- **Database:** PostgreSQL
- **Infrastructure:** TBD
- **Testing:** TBD

## Upcoming Features

**Several Marketplaces Integrations** – Expanding support for additional platforms

**Advanced Filtering** – Define precise criteria for the perfect deals

**Price Tracking** – Monitor item prices over time to recognize undervalued listings

**Instant Notifications** – Alerts when a targeted item appears

**Item Base Price Indicator** – Calculate listing's real value

**WebSocket Live Updates** – See new listings pop up in real time

**Full API Support** – Integrate the scraper into your own projects

## Deployment with Docker

TBD

## Running Tests

TBD

## 📌 Status

Project still in development.

## 🚀 How to Run the App

To run the project locally, follow these steps:

**Frontend**  
Navigate to the `frontend` directory and start the development server:
```bash
cd frontend
npm install
npm run dev
```

**Backend**  
Navigate to the `backend` directory and run the Go server:
```bash
cd backend
go run main.go
```

**Scraper**  
Make sure you have Python 3.11+ installed. Run the scraper module:
```bash
python -m scraper.main
```
Note: Ensure all dependencies are installed (`npm install` for frontend, `go mod tidy` for backend, and `pip install -r requirements.txt` for scraper).
