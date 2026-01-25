from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from test import q
from qq import queue_file
from typing import List
import asyncio
from redis import Redis
from typing import AsyncGenerator


pub = Redis()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


async def redis_listener():
    pubsub = pub.pubsub()
    pubsub.subscribe('processing', 'completed')
    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            try:
                data = message['data']
                data = data.decode('utf-8')
                if message['channel'] == b'processing':
                    response = {
                        'status' : 'processing',
                        'filename' : data
                    }
                    await manager.broadcast(response)
                elif message['channel'] == b'completed' :
                    response = {
                        'status' : 'completed',
                        'filename' : data
                    }
                    await manager.broadcast(response)   
            except BaseException:
                pass
        await asyncio.sleep(10)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    asyncio.create_task(redis_listener())
    yield
    # app teardown

app = FastAPI(lifespan=lifespan)


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def success(job, connection, result):
    # f.enqueue(db.db_insert, result)
    pub.publish('processing', job.id)


@app.post("/file")
async def file_read(file: UploadFile):
    try:
        job = q.enqueue(
            queue_file.file_process,
            file.file,
            file.filename,
            on_success=success,
            job_id=file.filename,
        )

        return JSONResponse(
            content={
                "status": "pending",
                "message": "File queued for processing",
                "filename": file.filename
            },
            status_code=202
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Just keep the connection alive, don't block
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
