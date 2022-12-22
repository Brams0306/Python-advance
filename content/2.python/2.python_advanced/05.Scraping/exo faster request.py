
from httpx import AsyncClient
import asyncio
import time


api_url = "https://api.quotable.io/random"


async def session_request_async(url: str, session: AsyncClient):
    # Instead of using request.get, we use our session
    response = await session.get(url)
    response_json = response.json()
    print(response_json["content"])
    return response_json


async def session_loop_request_async(url: str):
    # Create shared session for all of your requests
    async with AsyncClient() as session:
        # Create a list of empty tasks
        tasks = []
        # Query 50 times the API
        for _ in range(50):
            # Add a request to tasks
            tasks.append(
                asyncio.create_task(
                    session_request_async(url, session)        
                )
            )
        # Now that all the tasks are registred, run them
        responses = await asyncio.gather(*tasks)
            
            


start = time.perf_counter()

# We need to use asyncio.run to run the async function
asyncio.run(session_loop_request_async(api_url))

end = time.perf_counter()
execution_time = round((end - start), 2)
print(f'session_loop_request_async took {execution_time} sec')
```
!python3 ./assets/async_requests.py
### Results
It only took me **0.8 sec for 50 requests**! That's impressive.

But as you can see, it is harder to write, structure and debug. So make sure you **really** need it if you consider using this method.
## Summary

If we gather all our results:

| Method                     | Execution time for 50 requests |
|----------------------------|--------------------------------|
| `requests.get` loop        | 17.06 sec                  |
| `requests` with `Session`  | 5.99 sec                   |
| `httpx` with `AsyncClient` | 0.8 sec                   |
