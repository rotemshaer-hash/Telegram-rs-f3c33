from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import asyncio
import feedparser

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION = os.environ['SESSION_STRING']
TARGET = int(os.environ['TARGET_GROUP'])

SOURCES = [
    'ArtificialIntelligenceNews',
    'OpenAINews',
    'AIToolsHub',
    'ai_newss',
    'deeplearning_ai',
    'gpt4news',
    'TheAIEdge',
    'ml_news_channel',
]

RSS_FEEDS = [
    'https://techcrunch.com/tag/artificial-intelligence/feed/',
    'https://venturebeat.com/category/ai/feed/',
    'https://www.artificialintelligence-news.com/feed/',
    'https://feeds.feedburner.com/TheHackersNews',
    'https://www.wired.com/feed/tag/ai/latest/rss',
    'https://openai.com/blog/rss/',
    'https://bair.berkeley.edu/blog/feed.xml',
    'https://machinelearningmastery.com/feed/',
]

KEYWORDS = [
    # אנגלית
    'artificial intelligence', 'machine learning', 'deep learning',
    'neural network', 'large language model', 'llm', 'gpt', 'chatgpt',
    'openai', 'anthropic', 'claude', 'gemini', 'mistral', 'llama',
    'generative ai', 'gen ai', 'ai model', 'foundation model',
    'transformer', 'diffusion model', 'stable diffusion', 'midjourney',
    'copilot', 'autopilot', 'autonomous', 'robotics', 'humanoid',
    'agi', 'superintelligence', 'alignment', 'safety', 'regulation',
    'nvidia', 'gpu', 'inference', 'fine-tuning', 'rlhf',
    'multimodal', 'text to image', 'text to video', 'sora',
    'ai agent', 'agentic', 'reasoning model', 'o1', 'o3',
    'google deepmind', 'meta ai', 'microsoft ai', 'apple intelligence',
    'ai chip', 'data center', 'compute', 'benchmark',
    # עברית
    'בינה מלאכותית', 'למידת מכונה', 'בינה מלאכותית גנרטיבית',
    'מודל שפה', 'רובוט', 'אוטונומי', 'רגולציה על AI',
]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
sent_urls = set()

def has_keyword(text):
    if not text:
        return False
    t = text.lower()
    return any(k.lower() in t for k in KEYWORDS)

@client.on(events.NewMessage(chats=SOURCES))
async def handler(event):
    if has_keyword(event.message.text):
        await client.send_message(TARGET, f"🤖 {event.message.text}")

async def check_rss():
    while True:
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    summary = entry.get('summary', '')
                    if has_keyword(f"{title} {summary}") and link not in sent_urls:
                        sent_urls.add(link)
                        await client.send_message(TARGET, f"📰 {title}\n{link}")
            except Exception as e:
                print(f"RSS error: {e}")
        await asyncio.sleep(300)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("Not authorized!")
        return
    print("AI News Bot running...")
    await asyncio.gather(
        client.run_until_disconnected(),
        check_rss()
    )

asyncio.run(main())
