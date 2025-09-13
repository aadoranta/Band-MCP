from fastmcp import FastMCP
import pathlib

mcp = FastMCP("test")
SONGS_PATH = pathlib.Path("data/resume_faangpath.txt")


@mcp.prompt()
def purpose() -> str:
    """Global instruction for test model"""
    return f"""You are a virtual assistant for a band.

    All set lists are created based on the band's song library.
    We tailor our set lists to each event we play. 
    The vibe of any event is dictated by the communication we have with the event's organizer via email.
    You should always vary the style and key of songs in a set list to keep the audience engaged.
    We usually play 8 songs per set, of which a set lasts about 45 minutes.
    We always take a break between sets.
    Do not choose songs without keys associated with them.
    """


@mcp.tool()
def read_songs_library() -> str:
    """Reads the resume file and returns its content."""
    with open(SONGS_PATH, "r") as file:
        return file.read()


if __name__ == "__main__":
    mcp.run(transport="stdio")
