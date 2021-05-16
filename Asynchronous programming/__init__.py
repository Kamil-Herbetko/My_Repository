import asyncio

async def data():
    print('start fetching')
    await asyncio.sleep(2)
    print('done fetching')
    return {'data':1}

async def numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)

async def main():
    task1 = asyncio.create_task(data())
    task2 = asyncio.create_task(numbers())

    value = await task1
    print(value)
    await task2

asyncio.run(main())










