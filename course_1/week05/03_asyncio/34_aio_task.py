import asyncio

async def sleep_task(num):
    for i in range(5):
        print("process task: {} iter: {}".format(num, i))
        await asyncio.sleep(1)
    return num

loop = asyncio.get_event_loop()

task_list = [loop.create_task(sleep_task(i)) for i in range(2)]
loop.run_until_complete(asyncio.wait(task_list))
loop.run_until_complete(loop.create_task(sleep_task(3)))
rsp = loop.run_until_complete(asyncio.gather(
    sleep_task(10),
    sleep_task(20),
))
print(rsp)