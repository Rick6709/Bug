# Current Project Status & Architecture Context

## What Has Been Decided & Discussed:
- **Project Goal**: Create a minimum viable product (MVP) for a crypto tracking/trading platform for Binance Futures (BTCUSDT pair).
- **Infrastructure**: Google Cloud Compute Engine VM (`e2-micro`, Ubuntu 24.04 LTS). **Final Region**: `asia-east1` (Taiwan) - selected for Binance API compatibility and low latency.
- **Frontend Architecture**: Completely decoupled from the backend. Written in vanilla HTML/JS and hosted free on GitHub Pages (repository: Rick6709/Bug).
- **Backend Architecture**: FastAPI application running asynchronously. Two main background tasks:
  1. A periodic async task (REST API every 30-60s) to monitor the account balance.
  2. A persistent WebSocket connection to Binance to stream real-time price updates.
  - **Current Implementation**: 
    - Basic FastAPI structure created.
    - In-memory state management implemented.
    - WebSocket price streaming (Binance Futures) integrated.
- **Data Flow**: The backend stores the latest price and balance in memory (global state / variables) and serves this fresh data to the frontend via simple HTTP endpoints.

## Current Next Step:
1. **Persistence**: Ensure the backend runs in a `screen` session on the Taiwan VM.
2. **UI Polish**: Improve dashboard styling and add a "Last Updated" timestamp.