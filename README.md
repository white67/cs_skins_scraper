# CS Skins Scraper

**Real-time marketplace scraper to track and find favorite items**

## 🛠 How It Works

Project designed to continuously monitoring multiple marketplaces in real time, instantly detecting new listings that match your filters. The system:

1. **Scrapes new listings** from supported marketplaces the moment they appear.
2. **Filters items** based on customizable criteria (e.g., price, condition, stickers, trade status, etc.).
3. **Displays marketplace scraping status**, so you always know if data is up to date.
4. **Provides real-time insights** via the frontend, showing the newest listings as soon as they're available.

## Currently Supported Marketplaces

CSFloat

## Tech Stack

This project is built using modern technologies to ensure speed, scalability, and ease of deployment:

- **Backend:** Go (Gin, WebSockets)
- **Scraper:** Custom-built Python script with requests
- **Frontend:** React (TypeScript)
- **Database:** PostgreSQL for storage & caching
- **Infrastructure:** Docker
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