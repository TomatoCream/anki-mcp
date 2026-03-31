import httpx
import json
from typing import Any, Dict, Optional
from .models import AnkiResponse

class AnkiClient:
    def __init__(self, url: str = "http://localhost:8765", version: int = 6):
        self.url = url
        self.version = version

    async def invoke(self, action: str, **params) -> Any:
        payload = {
            "action": action,
            "version": self.version,
            "params": params
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.url, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                anki_resp = AnkiResponse(**data)
                if anki_resp.error:
                    raise Exception(anki_resp.error)
                return anki_resp.result
            except httpx.RequestError as exc:
                raise Exception(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            except json.JSONDecodeError:
                raise Exception("Failed to decode JSON response from Anki-Connect")
            except Exception as e:
                raise e
