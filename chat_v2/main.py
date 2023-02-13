from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store connected clients in a set
connected_clients = set()

# Define WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            # Send message to all connected clients
            for client in connected_clients:
                await client.send_text(message)
    except:
        connected_clients.remove(websocket)

# Define index page endpoint
@app.get("/")
async def get(request: Request):
    websocket_url = "ws://" + request.client.host + "/ws"
    return templates.TemplateResponse("index.html", {"request": request, "websocket_url": websocket_url})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)