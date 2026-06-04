Launch FreeCAD application from Claude Code.

Run the following PowerShell command to start FreeCAD in the background:

```powershell
Start-Process "C:\Program Files\FreeCAD 1.1\bin\FreeCAD.exe"
```

After running the command, report to the user:
1. That FreeCAD has been launched successfully
2. Remind them to start the MCP RPC server inside FreeCAD by clicking "Start RPC" in the MCP toolbar (the toolbar appears automatically if auto-start is enabled)
3. The freecad-mcp MCP server will connect to FreeCAD on localhost:9875 by default
4. Once FreeCAD's RPC server is running, they can use MCP tools like `create_document`, `create_object`, `execute_code`, etc.
