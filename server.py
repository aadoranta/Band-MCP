from fastmcp import FastMCP
from gmail import get_email_contents_from_subject
import pathlib

mcp = FastMCP("bandmcp")
SONGS_PATH = pathlib.Path("data/song_library.txt")


@mcp.prompt()
def purpose() -> str:
    """Global instruction for test model"""
    return f"""You are a virtual assistant for a band. Based on an input prompt, you will create
    a setlist for a concert. You have access to a library of songs stored in {SONGS_PATH}.

    REPLY WITH ONLY THE SETLIST, DO NOT REPEAT THE INSTRUCTIONS.
    """


@mcp.tool()
def read_songs_library() -> str:
    """Location of all songs that we play together. This is the sole source for songs
    that should be arranged into a setlist."""
    with open(SONGS_PATH, "r") as file:
        return file.read()


@mcp.tool()
def read_email_from_subject_line(subject_line: str) -> dict:
    """
    subject_line: The subject line of the email to read

    Returns the content of the email thread with that subject line.
    """

    content = get_email_contents_from_subject(subject_line)
    return content


if __name__ == "__main__":
    mcp.run(transport="stdio")
