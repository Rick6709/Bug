# Current Project Status & Architecture Context

## What Has Been Decided & Discussed:
- **Project Goal**: Create a minimum viable product (MVP) for a crypto tracking/trading platform for Binance Futures (BTCUSDT pair).
- **Infrastructure**: Google Cloud Compute Engine VM (`e2-micro`, Ubuntu 24.04 LTS, location: `us-central1`) is successfully initialized and ready to host the backend.
- **Frontend Architecture**: Completely decoupled from the backend. Written in vanilla HTML/JS and hosted free on GitHub Pages (repository: Rick6709/Bug).
- **Backend Architecture**: FastAPI application running asynchronously. It will handle two main background tasks:
  1. A periodic async task (REST API every 30-60s) to monitor the account balance.
  2. A persistent WebSocket connection to Binance to stream real-time price updates.
- **Data Flow**: The backend stores the latest price and balance in memory (global state / variables) and serves this fresh data to the frontend via simple HTTP endpoints.

## Current Next Step:
We need to initialize the repository structure. The immediate task for the AI assistant is to generate the base directory tree, set up environment protection, and write the initial async FastAPI scaffolding.