import asyncio
import random

def myCoroutine(id):
    print("Coroutine: {}, has successfully completed after {} seconds".format(id, random.randint(1,5)))

async def main():
    tasks = []
    for i in range(10):
        tasks.append(myCoroutine(i))

    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
