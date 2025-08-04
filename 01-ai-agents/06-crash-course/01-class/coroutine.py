# aise to ham phas gaye infinite loop me har async function ko execute karne ke liye aik or async fun banana parega kiu ke await ke bagher
# async func execute nahi hota or await sirf async function me hi use karsakte hen

"""
async def hello(user:str) -> str:
    return f"Hello {user}"

async def main():
    greet = await hello("Huzair")
    print(greet)
main() - Error
"""

# Solution: asyncio.run()

# ye aik event loop banadega or sab async functions usme schedule kardega!

import asyncio

async def hello(user:str) -> str:
    return f"Hello {user}"

async def main():
    greet = await hello("Huzair")
    print(greet)
    
asyncio.run(main())