# Set up FreeCAD MCP for Gridfinity Designer

This guide uses [neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp) as one concrete option, not a bundled dependency. Instructions were checked against upstream documentation on 2026-09-20; follow its current requirements when versions change. This is documentation, not an installation script.

## 1. Install the prerequisites

Install [FreeCAD](https://www.freecad.org/downloads.php) and [uv/uvx](https://docs.astral.sh/uv/getting-started/installation/).

The external MCP package requires Python 3.12+, while the addon uses FreeCAD's own Python. Do not install the MCP package into FreeCAD's bundled environment. [Upstream installation guide](https://github.com/neka-nat/freecad-mcp/blob/main/docs/installation.md).

## 2. Add the FreeCAD workbench

Clone the upstream repository:

```sh
git clone https://github.com/neka-nat/freecad-mcp.git
```

In FreeCAD, open **View → Panels → Python console** and locate the active installation's user directory:

```python
from pathlib import Path
print(Path(FreeCAD.getUserAppDataDir()) / "Mod")
```

Copy the checkout's `addon/FreeCADMCP` folder there. The resulting structure must contain `Mod/FreeCADMCP/InitGui.py`, without an extra nested directory. This avoids guessing version-specific Windows/macOS/Linux paths.

Restart FreeCAD, select **MCP Addon**, and click **Start RPC Server**. Keep FreeCAD open. See the [illustrated addon instructions](https://github.com/neka-nat/freecad-mcp/blob/main/docs/installation.md#install-the-addon).

## 3. Register the server in Codex

The external MCP process uses standard input/output; Codex launches it. The following combines upstream's `uvx freecad-mcp` entrypoint with [Codex's documented MCP registration syntax](https://developers.openai.com/codex/mcp):

```sh
codex mcp add freecad -- uvx freecad-mcp
codex mcp list
```

Alternatively, add this table to your existing `~/.codex/config.toml` (do not replace unrelated settings):

```toml
[mcp_servers.freecad]
command = "uvx"
args = ["freecad-mcp"]
```

Use **one** method. Codex desktop, CLI and IDE share this configuration. If the desktop client cannot find `uvx`, set `command` to its full executable path. Reopen the client after configuring it. [Official Codex MCP documentation](https://developers.openai.com/codex/mcp).

The addon's default port **9875** is an XML-RPC connection used by the bridge, not an HTTP/SSE MCP URL. Do not substitute it for the stdio configuration above. [Upstream client troubleshooting](https://github.com/neka-nat/freecad-mcp/blob/main/docs/installation.md#windows-client-launch-troubleshooting).

## 4. Check the complete connection

Ask Codex:

```text
Check the FreeCAD MCP connection with an available read-only operation.
List the open documents and report whether FreeCAD responds.
Do not change existing documents.
```

A configured entry in `codex mcp list` is only the first check; a successful tool response establishes that the bridge reaches FreeCAD. Then start Gridfinity Designer. If desired, request a separate disposable test document before a real organizer.

## Troubleshooting and further reading

| Symptom | Next step |
|---|---|
| Workbench missing | Check folder nesting, restart FreeCAD and inspect Report view. |
| MCP process will not launch | Try `uvx freecad-mcp --help`; check the client's executable path. |
| Connection refused | Start the addon's RPC server; keep its FreeCAD instance open. |
| Slow operation or missing headless executable | Follow upstream's execution guide; GUI and headless execution are separate capabilities. |
| Remote FreeCAD can model but cannot save your file | Choose a path writable on the server and arrange retrieval; client and server may have different filesystems. |

- [Installation and platform-specific troubleshooting](https://github.com/neka-nat/freecad-mcp/blob/main/docs/installation.md).
- [Auto-start and remote configuration](https://github.com/neka-nat/freecad-mcp/blob/main/docs/configuration.md).
- [Execution modes, timeouts and headless setup](https://github.com/neka-nat/freecad-mcp/blob/main/docs/execution.md).
- [Available tools](https://github.com/neka-nat/freecad-mcp/blob/main/docs/tools.md).

Installing this skill does not perform these connection steps. A fresh install of this upstream package was not retested while writing the guide; our example's existing FreeCAD MCP connection was exercised during CAD generation.
