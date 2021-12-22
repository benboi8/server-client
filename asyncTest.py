import asyncio
import datetime as dt



async def SayAfter(delay, text):
	await asyncio.sleep(delay)
	print(text)


async def Main1():
	task1 = asyncio.create_task(SayAfter(1, "Hello"))
	task2 = asyncio.create_task(SayAfter(2, "World"))

	startTime = dt.datetime.now()
	print(f"Started at {startTime}")

	await task1
	await task2

	print(f"Finished at {dt.datetime.now()}. Time taken: {dt.datetime.now() - startTime}")


async def Nested():
	return 42

async def Main2():
	task = asyncio.create_task(Nested())

	print(await task)


# asyncio.run(Main1())
asyncio.run(Main2())
