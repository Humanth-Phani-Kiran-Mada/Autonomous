"""
Advanced Web Crawler for autonomous knowledge acquisition
"""
import asyncio
import aiohttp
from typing import List, Dict, Set, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import json
from pathlib import Path
import config
from src.logger import logger
import hashlib

class WebCrawler:
    """Intelligent web crawler that autonomously discovers and learns from web content"""
    
    def __init__(self):
        self.visited_urls: Set[str] = set()
        self.discovered_knowledge: List[Dict] = []
        self.crawl_history: Dict = {}
        self.cache_dir = config.CACHE_DIR / "crawled_content"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.load_state()
        logger.info("🕷️ Web Crawler initialized")
    
    def load_state(self):
        """Load crawler state from disk"""
        state_file = config.DATA_DIR / "crawler_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.visited_urls = set(state.get("visited_urls", []))
                    self.crawl_history = state.get("crawl_history", {})
                    logger.info(f"Loaded crawler state: {len(self.visited_urls)} visited URLs")
            except Exception as e:
                logger.error(f"Failed to load crawler state: {e}")
    
    def save_state(self):
        """Save crawler state to disk"""
        state_file = config.DATA_DIR / "crawler_state.json"
        try:
            state = {
                "visited_urls": list(self.visited_urls),
                "crawl_history": self.crawl_history
            }
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
            logger.debug("Crawler state saved")
        except Exception as e:
            logger.error(f"Failed to save crawler state: {e}")
    
    def _get_cache_path(self, url: str) -> Path:
        """Get cache file path for URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.json"
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch a single page with error handling"""
        if url in self.visited_urls:
            logger.debug(f"📋 URL already visited: {url}")
            return None
        
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=config.CRAWLER_TIMEOUT),
                headers={"User-Agent": config.CRAWLER_USER_AGENT}
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    self.visited_urls.add(url)
                    self.crawl_history[url] = {
                        "timestamp": datetime.now().isoformat(),
                        "status": 200
                    }
                    logger.info(f"✅ Fetched: {url}")
                    return content
                else:
                    logger.warning(f"⚠️ Failed to fetch {url}: Status {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.warning(f"⏱️ Timeout fetching {url}")
            return None
        except Exception as e:
            logger.error(f"❌ Error fetching {url}: {e}")
            return None
    
    def extract_knowledge(self, html: str, url: str) -> List[Dict]:
        """Extract structured knowledge from HTML content"""
        knowledge = []
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            page_title = title.string if title else "Unknown"
            
            # Extract main content
            main_content = soup.find(['main', 'article', 'div'])
            if main_content:
                paragraphs = main_content.find_all('p')
                for para in paragraphs[:10]:  # Limit to first 10 paragraphs
                    text = para.get_text(strip=True)
                    if len(text) > 50:  # Only keep substantial paragraphs
                        knowledge.append({
                            "source": url,
                            "type": "text_content",
                            "content": text,
                            "title": page_title,
                            "timestamp": datetime.now().isoformat()
                        })
            
            # Extract headers
            headers = soup.find_all(['h1', 'h2', 'h3'])
            for header in headers[:5]:
                text = header.get_text(strip=True)
                if text:
                    knowledge.append({
                        "source": url,
                        "type": "header",
                        "content": text,
                        "title": page_title,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Extract links (for future crawling)
            links = soup.find_all('a', href=True)
            discovered_links = []
            for link in links[:5]:
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url, href)
                    if self._is_valid_url(absolute_url):
                        discovered_links.append(absolute_url)
            
            if discovered_links:
                knowledge.append({
                    "source": url,
                    "type": "links",
                    "content": discovered_links,
                    "title": page_title,
                    "timestamp": datetime.now().isoformat()
                })
            
            logger.info(f"🧠 Extracted {len(knowledge)} knowledge items from {url}")
            return knowledge
        except Exception as e:
            logger.error(f"Error extracting knowledge from {url}: {e}")
            return []
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL for crawling"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except:
            return False
    
    async def crawl_sources(self, sources: Optional[List[str]] = None, max_pages: int = 50) -> List[Dict]:
        """Autonomously crawl learning sources and extract knowledge"""
        sources = sources or config.LEARNING_SOURCES
        self.discovered_knowledge = []
        
        logger.info(f"🚀 Starting autonomous crawl of {len(sources)} sources (max {max_pages} pages)")
        
        connector = aiohttp.TCPConnector(limit_per_host=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            pages_crawled = 0
            
            for source in sources:
                if pages_crawled >= max_pages:
                    break
                
                # Create tasks for each source
                for _ in range(min(3, max_pages - pages_crawled)):
                    task = self.fetch_page(session, source)
                    tasks.append((source, task))
                    pages_crawled += 1
            
            # Execute tasks concurrently
            for source, task in tasks:
                try:
                    html = await task
                    if html:
                        knowledge_items = self.extract_knowledge(html, source)
                        self.discovered_knowledge.extend(knowledge_items)
                        
                        # Cache content
                        cache_path = self._get_cache_path(source)
                        with open(cache_path, 'w') as f:
                            json.dump({"url": source, "knowledge": knowledge_items}, f)
                except Exception as e:
                    logger.error(f"Error processing {source}: {e}")
        
        self.save_state()
        logger.info(f"✅ Crawl complete: {len(self.discovered_knowledge)} knowledge items acquired")
        return self.discovered_knowledge
    
    def get_discovery_summary(self) -> Dict:
        """Get summary of discovered knowledge"""
        return {
            "total_visited_urls": len(self.visited_urls),
            "total_knowledge_items": len(self.discovered_knowledge),
            "knowledge_types": list(set(k.get("type") for k in self.discovered_knowledge)),
            "crawl_history_size": len(self.crawl_history)
        }
