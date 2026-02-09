from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """__summary__ 
    Add two numbers
    """
    return a+b


@mcp.tool()
def multiple(a: int, b: int) -> int:
    """__summary__
    Multiply two numbers
    """
    return a*b


if __name__ == "__main__":
    # Run the MCP server over stdio so the LangChain MCP client
    # can launch this process with `python mathServer.py`.
    mcp.run(transport="stdio")

