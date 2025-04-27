# Discord Bot in Python

Universal and lightweight template for your bot built with `disnake`. Easily add slash commands, events, and modules (cogs) to fit any use case.

---

## Features

- Full support for Slash commands (`disnake.ext.commands`)
- Modular architecture using cogs for clean code organization
- Event handlers: `on_ready`, `on_member_join`, and more
- Configuration via `.env` or `config.py`
- Example commands: `/avatar`, `/say`, `/userinfo`

---

## Requirements

- Python 3.9 or newer
- `disnake` library
- `python-dotenv` (if using a `.env` file)
- Other dependencies listed in `requirements.txt`

> Install all dependencies:
> ```bash
> pip install -r requirements.txt
> ```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ananas1kexe/bot-on-disnake
   cd discord-python-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your bot**:
   - Create a `.env` file in the project root:
     ```ini
     TOKEN="your_bot_token_here"
     ```

---

## Running the Bot

Start your bot by running:
```bash
python main.py
```

---

## Contributing

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add new command or feature"
   ```
4. Push to your branch and open a Pull Request

---

## Useful Links

- [Project Repository](https://github.com/Ananas1kexe/bot-on-disnake)
- [MIT License](https://github.com/YourUsername/Ananas1kexe/blob/main/LICENSE)

---

## License

This project is licensed under the **MIT License**.  
See [LICENSE](https://github.com/YourUsername/discord-python-bot/blob/main/LICENSE) for details.
