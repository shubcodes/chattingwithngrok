from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store connected clients in a set
connected_clients = set()

# Store chat messages in a list of tuples
chat_messages = []

# Define WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            # Get user name from X-Forwarded-User header
            user_name = websocket.headers.get("X-Forwarded-User")
            # Store message and user name in chat_messages list
            chat_messages.append((user_name, message))
            # Send message to all connected clients
            for client in connected_clients:
                await client.send_text(f"{user_name}: {message}")
    except:
        connected_clients.remove(websocket)

# Define index page endpoint
@app.get("/")
async def get(request: Request):
    # Render index.html template and pass chat messages to it
    content = templates.TemplateResponse("index.html", {"request": request, "chat_messages": chat_messages})
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
