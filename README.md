# dolario-bot
Dolario es un bot de Telegram que brinda diversas funcionalidades para que puedas obtener el precio actual del dólar en Venezuela.

![Example](src\assets\1.png)

## Librerías necesarias:

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI): Una biblioteca de Python para la API de bots de Telegram.
- [pyDolarVenezuela](https://github.com/fcoagz/pyDolarVenezuela): Una biblioteca para obtener el precio del dólar en Venezuela.
- [python-dotenv](https://github.com/theskumar/python-dotenv): Una biblioteca que carga variables de entorno desde un archivo `.env`.
- [pytz](https://github.com/stub42/pytz): Un paquete Python que proporciona funcionalidades relacionadas con zonas horarias.

## Uso

1. Obtenga su token API de bot de Telegram
2. Establecer las variables de entorno: `NAME`, `BOT_TOKEN`, `ADMIN` (opcional), `USERNAME` (opcional).
3. Ejecute los siguientes comandos
```sh
pip install -r requirements.txt
python main.py
```

## License
MIT License.