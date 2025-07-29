git clone https://github.com/PASIYAv12/Btc.git
cd Btc

# Create a .env file like .env.example and add your Binance API Key/Secret and Telegram Token
cp .env.example .env
# edit .env to add:
# BINANCE_API_KEY="..."
# BINANCE_API_SECRET="..."
# TELEGRAM_TOKEN="..."
# OWNER_ID="6711430693"

pip install -r requirements.txt
python main.py
