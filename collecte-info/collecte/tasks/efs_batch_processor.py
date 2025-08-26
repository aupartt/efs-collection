import asyncio
import logging
import re

from aiohttp import ClientError, ClientSession, ClientTimeout, TCPConnector
from async_lru import alru_cache

logger = logging.getLogger(__name__)


class EFSBatchProcessor:
    """Process multiple EFS ID requests with a shared session"""

    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None

    async def __aenter__(self):
        timeout = ClientTimeout(total=45, connect=15, sock_read=15)
        connector = TCPConnector(
            limit=100,
            limit_per_host=20,
            keepalive_timeout=30,
            enable_cleanup_closed=True,
        )
        self.session = ClientSession(timeout=timeout, connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @alru_cache()
    async def get_efs_id(self, url: str, max_retries: int = 3) -> str | None:
        """Get EFS ID using shared session"""
        if not url:
            return None

        for attempt in range(max_retries):
            async with self.semaphore:
                try:
                    async with self.session.head(url, allow_redirects=True) as resp:
                        reg = r"trouver-une-collecte/([0-9]+)/"
                        match = re.search(reg, resp.url.raw_path)
                        return match.group(1) if match else None

                except (TimeoutError, ClientError) as e:
                    if attempt < max_retries - 1:
                        wait_time = 2**attempt
                        logger.warning(
                            f"Retry {attempt + 1}/{max_retries} for EFS_ID",
                            extra={"url": url, "error": str(e)},
                        )
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        logger.error(
                            "Failed to retrieve EFS_ID after retries",
                            extra={"url": url, "error": str(e)},
                        )
                        return None

                except Exception as e:
                    logger.error(
                        "Unexpected error retrieving EFS_ID",
                        extra={"url": url, "error": str(e)},
                    )
                    return None

        return None
