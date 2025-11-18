import asyncio
from fastmcp import Client

async def main():
    port = input("Enter the port to access mcp server locally: ")
    async with Client(f"http://localhost:{port}/mcp") as client:
        await client.ping()
        tools_functions = await client.list_tools()
        tools = {tool.name: tool for tool in tools_functions}

        print("Available tools:")
        for name in tools:
            print(" -", name)

        print("\nPress 'q' to exit\n")

        while True:
            user_input = input("Choose a tool or 'q' to exit: ").strip()
            if user_input.lower() == "q":
                break
            if user_input not in tools:
                print("Invalid tool name")
                continue

            tool = tools[user_input]
            args = {}

            for param in tool.inputSchema.get("required", []):
                value = input(f"Enter value for required '{param}': ")
                args[param] = value

            try:
                result = await client.call_tool(tool.name, args)
                print("Result:", result.content[0].text)
            except Exception as e:
                print("Error calling tool:", e)

asyncio.run(main())