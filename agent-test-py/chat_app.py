import time
from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse
from queue import Queue
import threading # Import threading

app = FastAPI()

# Creating the queue
streamer_queue = Queue()

# The generation process (now runs in a thread)
def start_generation(query):
    for i in range(1, 10): # Simulate generating 9 chunks
        # Format as Server-Sent Events (SSE) data
        streamer_queue.put(f"data: {i}\n\n")
        time.sleep(0.5) # Simulate work being done

    # Signal end of stream for SSE clients
    streamer_queue.put("data: [DONE]\n\n")
    # Internal sentinel to stop the async generator loop
    streamer_queue.put(None)

# Generation initiator and response server
async def response_generator(query):
    # Start the generation process in a separate thread
    thread = threading.Thread(target=start_generation, args=(query,))
    thread.start()

    while True:
        # Get value from the queue (this blocks the thread, but not the event loop)
        value = streamer_queue.get()
        if value is None: # Check for the internal sentinel
            break
        yield value # Yield the SSE formatted string
        streamer_queue.task_done() # Mark the task as done in the queue
        await asyncio.sleep(0.01) # Yield control to the event loop

    streamer_queue.task_done() # Mark the None sentinel as done

@app.get('/query-stream/')
async def stream(query: str):
    print(f'Query received: {query}')
    return StreamingResponse(response_generator(query), media_type='text/event-stream')

