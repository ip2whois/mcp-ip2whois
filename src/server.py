from typing import Any, Dict
import httpx
from mcp.server.fastmcp import FastMCP
import os
import sys

# Initialize FastMCP server
mcp = FastMCP("ip2whois")

# Constants
IPW_API_BASE = "https://api.ip2whois.com/v2"
USER_AGENT = "ip2whois-app/1.0"

def get_api_key() -> str | None:
    """Retrieve the API key from MCP server config."""
    return os.getenv("IP2WHOIS_API_KEY")

async def make_request(url: str, params: dict[str, str]) -> dict[str, Any] | None:
    """Make a request to the IP2WHOIS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_whois(domain: str) -> Dict[str, Any] | str:
    """
    Lookup WHOIS data for a domain name. Use this tool when the user asks about 
    domain registration details, registrar names, expiry dates, domain ownership, 
    or nameservers for a specific website (e.g., 'google.com').

    Args:
        domain: The domain name to look up (e.g., 'example.com').

    Returns:
        A JSON string result includes domain age, update and expiry date, assiociated nameservers, registrar and registrant information, and admin, tech and billing information.
    """
    params = {"domain": domain}
    api_key = get_api_key()
    params["key"] = api_key  # IP2WHOIS API key parameter
    whois_result = await make_request(IPW_API_BASE, params)

    if not whois_result:
        return f"Unable to fetch WHOIS information for domain {domain}."

    return whois_result

if __name__ == "__main__":
    mcp.run(transport='stdio')