# Band-MCP

## Overview

Using [mcp-client-for-ollama](https://github.com/jonigl/mcp-client-for-ollama) together with [FastMCP](https://gofastmcp.com/getting-started/welcome), **Band-MCP** provides a standalone platform for running a local model that can:

- Summarize emails  
- Prepare set lists based on email constraints  
- Save and manage set lists  

This setup allows you to leverage local LLMs with the MCP (Model Context Protocol) for flexible, private, and efficient workflows.

---

## To Use

1. **Obtain Gmail API credentials**  
   - Follow [Google’s guide](https://developers.google.com/workspace/guides/create-credentials) to create OAuth credentials.  
   - Save the file as `/auth/credentials.json`.  

2. **Download the Qwen3 model with Ollama**  
   - Visit [Ollama’s Qwen3 library](https://ollama.com/library/qwen3).  
   - At minimum, use the **Qwen3-4B** parameter model (larger models recommended if resources allow).  

3. **Install dependencies**  
   - Install Python dependencies using the provided `requirements.txt`:  
     ```bash
     pip install -r requirements.txt
     ```

4. **Install ollmcp**  
   - Follow the guide at [mcp-client-for-ollama](https://github.com/jonigl/mcp-client-for-ollama) to install **ollmcp**.  

5. **Run the MCP server**  
   - Start the server with your chosen model:  
     ```bash
     ollmcp -s ./src/server.py -m <your_model>
     ```
   > **Note:** The first time you run this, the Gmail API will automatically generate a `token.json` file.  
   > Store this file in `/auth` alongside your `credentials.json`.  
