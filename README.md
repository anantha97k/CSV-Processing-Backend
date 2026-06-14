# File Upload Backend

A backend service for handling file uploads asynchronously, with real-time job status updates via WebSocket.

## Architecture

- **API Server** — Accepts file uploads via `POST /upload` and manages WebSocket connections
- **Redis** — Acts as the message broker: job queue (via RQ) and pub/sub channel for status events
- **RQ Worker** — Processes uploaded files in the background
- **File Storage** — Stores processed files (S3 or local disk)
- **Database** — Persists job metadata and results

## How It Works

1. Client uploads a file via `POST /file`
2. API server saves the file and enqueues a background job in Redis
3. Client opens a WebSocket connection to receive real-time updates
4. RQ worker picks up the job, processes the file, and publishes status events to Redis
5. WebSocket handler forwards those events to the connected client

## Getting Started

### Prerequisites

- Python 3.10+
- Redis server running locally or via Docker

### Installation

```bash
uv sync
```

### Running Redis

```bash
docker run -d -p 6379:6379 redis
```

### Start the API Server

```bash
python main.py
```

### Start the RQ Worker

```bash
rq worker --with-scheduler
```

## API Reference

### `POST /file`

Upload a file for background processing.

**Request:** `multipart/form-data` with a `file` field

**Response:**
```json
{
  "job_id": "abc123",
  "status": "queued"
}
```

### WebSocket `/ws/<job_id>`

Connect to receive real-time job status events.

**Events:**
| Event | Description |
|-------|-------------|
| `queued` | Job has been added to the queue |
| `started` | Worker has picked up the job |
| `progress` | Processing update with percentage |
| `done` | Job completed successfully |
| `failed` | Job encountered an error |
