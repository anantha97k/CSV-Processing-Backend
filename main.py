from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from queue_conn import task_queue
from async_queue import async_tasks
import asyncio
from typing import AsyncGenerator


from websocket_conn import ConnectionManager
from redis_pubsub import redis_listener, pub

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    asyncio.create_task(redis_listener(manager))
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
    pub.publish("processing", f"{job.id}.csv")


@app.post("/file")
async def file_read(file: UploadFile):

    try:
        task_queue.enqueue(
            async_tasks.file_process,
            file.file,
            file.filename,
            on_success=success,
            job_id=file.filename.split(".")[0],
        )

        return JSONResponse(
            content={
                "status": "pending",
                "message": "File queued for processing",
                "filename": file.filename,
            },
            status_code=202,
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
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
