from fastmcp import FastMCP
from gmail import get_email_contents_from_subject
import pathlib

mcp = FastMCP("bandmcp")
SONGS_PATH = pathlib.Path("data/song_library.txt")


@mcp.tool()
def get_songs_library() -> str:
    """Location of all songs that we play together. This is the sole source for songs
    that should be arranged into a setlist."""
    with open(SONGS_PATH, "r") as file:
        return file.read()


@mcp.tool()
def get_email_from_subject_line(subject_line: str) -> dict:
    """
    subject_line: The subject line of the email to read

    Returns the content of the email thread with that subject line.
    """

    content = get_email_contents_from_subject(subject_line)
    return content


@mcp.tool()
def save_set_list(set_list: str, subject_line: str) -> dict:
    """
    set_list: The set list to save
    subject_line: The subject line of the email to associate with the set list

    Returns a confirmation message.
    """
    # Here you would implement the logic to save the set list
    with open(f"data/set_list_{subject_line}.txt", "w") as file:
        file.write(set_list)
    return {"status": "success", "message": "Set list saved successfully."}


if __name__ == "__main__":
    mcp.run(transport="stdio")
