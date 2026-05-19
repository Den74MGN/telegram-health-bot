# 🆓 FREE Setup Guide - Telegram Health Bot

## 💯 100% Free Operation - No Paid APIs Required!

This guide will help you set up your Telegram Health Bot using **ONLY FREE APIs and services**. No credit card required, no hidden costs!

---

## 📋 Prerequisites

- Python 3.9 or higher
- Telegram account
- GitHub account (you already have this!)
- Google account (for Gemini API)

---

## 🚀 Quick Start (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/santafreshden4ik-arch/telegram_health_bot.git
cd telegram_health_bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get FREE API Keys

#### 🤖 Telegram Bot Token (FREE)
1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 🧠 Google Gemini API (FREE - 60 requests/minute)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key
4. **FREE tier**: 60 requests per minute, unlimited daily quota!

#### 🔄 OpenRouter API (FREE models available)
1. Go to https://openrouter.ai/keys
2. Sign up with Google/GitHub
3. Click "Create Key"
4. Copy your API key
5. **FREE models**: Llama 3.2, Gemma 2, Mistral, Qwen

#### 🤗 Hugging Face API (FREE)
1. Go to https://huggingface.co/settings/tokens
2. Create account if needed
3. Click "New token"
4. Copy your token
5. **FREE tier**: Unlimited inference API calls!

#### 🎨 Pollinations.ai (100% FREE - No API Key Needed!)
- **No registration required**
- **No API key needed**
- **Unlimited image generation**
- Already integrated in the bot!

---

## ⚙️ Configuration

### Create `.env` file

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### Edit `.env` with your FREE API keys:

```env
# Telegram Bot (REQUIRED)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# FREE AI APIs (at least one required)
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here  # Optional
HUGGINGFACE_API_KEY=your_huggingface_token_here  # Optional

# Pollinations.ai - NO API KEY NEEDED! (100% FREE)

# Bot Configuration
CONTENT_SCHEDULE=09:00,14:00,20:00
ENABLE_ANALYTICS=true
LOG_LEVEL=INFO
```

---

## 🎯 FREE AI Models Usage

### Text Generation (FREE)

The bot automatically uses FREE models with fallback:

1. **Google Gemini 2.0 Flash** (FREE tier - 60 req/min)
2. **OpenRouter Free Models**:
   - `meta-llama/llama-3.2-3b-instruct:free`
   - `google/gemma-2-9b-it:free`
   - `mistralai/mistral-7b-instruct:free`
   - `qwen/qwen-2-7b-instruct:free`
3. **Hugging Face** (FREE unlimited):
   - `mistralai/Mistral-7B-Instruct-v0.1`
   - `meta-llama/Llama-2-7b-chat-hf`

### Image Generation (FREE)

1. **Pollinations.ai** (100% FREE, no key needed!)
2. **Hugging Face Stable Diffusion** (FREE with API key)

---

## ▶️ Run the Bot

### Basic Run

```bash
python main.py
```

### With Logging

```bash
python main.py --log-level DEBUG
```

### Background Run (Linux/Mac)

```bash
nohup python main.py &
```

---

## ✅ Verify Setup

### Test FREE API Connections

```bash
python free_ai_clients.py
```

You should see:
```
✓ OpenRouter connection successful
✓ Hugging Face connection successful  
✓ Gemini connection successful
```

### Test FREE Image Generation

```bash
python free_image_generator.py
```

You should see:
```
✓ Pollinations.ai is available (100% FREE!)
✓ Generated image: 234567 bytes
✓ Saved to test_image.jpg
```

---

## 🔧 Troubleshooting

### "Rate limit exceeded" for Gemini
**Solution**: Bot automatically switches to OpenRouter or Hugging Face FREE models

### OpenRouter shows "No credits"
**Solution**: Use only FREE models listed above (they don't need credits)

### Hugging Face model loading
**Solution**: First request may take 20-30 seconds as model loads. Subsequent requests are fast.

### Pollinations.ai timeout
**Solution**: Image generation may take 10-30 seconds. Bot has automatic retry.

---

## 📊 FREE Tier Limits

| Service | FREE Limit | Notes |
|---------|-----------|-------|
| **Gemini 2.0 Flash** | 60 req/min | Best for text generation |
| **OpenRouter Free** | Unlimited* | Free models only |
| **Hugging Face** | Unlimited | May have cold start delay |
| **Pollinations.ai** | Unlimited | 100% free, no limits! |
| **Telegram Bot API** | Unlimited | Completely free |

*Free models on OpenRouter have no rate limits

---

## 🎓 Best Practices for FREE Operation

### 1. Optimize API Usage
- Use caching for repeated queries
- Implement exponential backoff on errors
- Enable automatic fallback between providers

### 2. Monitor Usage
- Check logs regularly: `tail -f bot.log`
- Track which FREE API is used most
- Adjust preferred provider in code

### 3. Cost = $0.00 Forever!
- All services used are 100% FREE
- No hidden costs
- No credit card required
- No trial periods that expire

---

## 🤝 Support

If you encounter issues:
1. Check `.env` file has correct API keys
2. Verify Python version: `python --version` (need 3.9+)
3. Check logs: `cat bot.log`
4. Test individual components with test scripts

---

## 🌟 Features Using FREE APIs

✅ AI-generated health tips (Gemini/OpenRouter/Hugging Face)
✅ Beautiful images (Pollinations.ai)
✅ Scheduled content (built-in Python scheduler)
✅ Analytics tracking (local SQLite database)
✅ Error handling with fallback (automatic)
✅ Centralized logging (built-in Python logging)

---

## 🔄 Automatic Fallback System

The bot includes intelligent fallback:

1. Try **Gemini** (fastest, 60 req/min)
2. If fails → Try **OpenRouter FREE models**
3. If fails → Try **Hugging Face**
4. If all fail → Create draft for manual review

**You'll NEVER lose content due to API failures!**

---

## 🎉 Congratulations!

Your Telegram Health Bot is now running **100% FREE** with:
- ✅ Multiple AI providers
- ✅ Automatic failover
- ✅ Image generation
- ✅ No ongoing costs
- ✅ Production-ready error handling

**Total Cost: $0.00 per month, forever!**

---

## 📚 Additional Resources

- [Gemini API Docs](https://ai.google.dev/docs)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference)
- [Pollinations.ai](https://pollinations.ai/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Built with ❤️ using only FREE and open-source tools!**
