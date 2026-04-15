"""Allow ``python -m scripts.mcp_server`` to launch the stdio server."""
from .server import main

if __name__ == "__main__":
    main()
