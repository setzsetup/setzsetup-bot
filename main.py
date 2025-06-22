import os
import time
import requests
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Frases de CTA variadas
frases_cta = [
    "🔥 Aproveite agora mesmo!",
    "💥 Oferta imperdível, clique e confira!",
    "✅ Promoção top, só hoje!",
    "🎯 A oferta que você estava esperando!",
    "🚨 Estoque limitado, corre lá!"
]

# Função para buscar ofertas
async def buscar_ofertas():
    url = "https://www.amazon.com.br/gp/bestsellers/videogames/16243818011"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        produtos = soup.select('.zg-grid-general-faceout')[:3]

        ofertas = []
        for produto in produtos:
            titulo = produto.select_one('.p13n-sc-truncate, .zg-text-center-align a span')
            imagem = produto.select_one('img')
            link = produto.select_one('a.a-link-normal')

            if titulo and imagem and link:
                ofertas.append({
                    "titulo": titulo.get_text(strip=True),
                    "imagem": imagem['src'],
                    "link": f"https://www.amazon.com.br{link['href'].split('?')[0]}?tag=setzsetup-20"
                })

        return ofertas

    except Exception as e:
        print(f"Erro ao buscar ofertas: {e}")
        return []

# Função para enviar mensagens
async def enviar_ofertas():
    while True:
        ofertas = await buscar_ofertas()
        for oferta in ofertas:
            try:
                from random import choice
                legenda = f"<b>{oferta['titulo']}</b>

<a href='{oferta['link']}'>{choice(frases_cta)}</a>"
                bot.send_photo(chat_id=CHAT_ID, photo=oferta['imagem'], caption=legenda, parse_mode='HTML')
                await asyncio.sleep(1200)  # 3 por hora = a cada 20 minutos (1200 segundos)
            except Exception as e:
                print(f"Erro ao enviar: {e}")

if __name__ == '__main__':
    asyncio.run(enviar_ofertas())