from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
import asyncio

BOT_TOKEN = "7867343021:AAFEnUOf0O1Om5QF_PJm9Rk_FhKA6pr8ZiI"

PATHS = {
    "pc": "gifs/2.mov",
    "phone": "gifs/1.mp4"
}

CAPTIONS = {
    "pc": """How to use gifs on your PC:
    Step 1: Open 𝕏/Telegram
    Step 2: Click on the GIF icon and Search <code>crypto clown</code>
    Step 3: Choose your GIF and send it 🚀""",
    
    "phone": """How to use gifs on your Phone:
    Step 1: Download and open Tenor
    Step 2: Search crypto clown
    Step 3: Add Retardio GIFs to your pack
    Step 4: Send GIFs from your keyboard. Anywhere 🌍"""
}

class VideoBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.file_ids = {"pc": None, "phone": None}
        self._setup_handlers()

    def _setup_handlers(self):
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.callback_query.register(self.handle_buttons)

    @staticmethod
    def get_keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="PC", callback_data="pc_button"),
                InlineKeyboardButton(text="Phone", callback_data="phone_button")
            ]]
        )

    async def cmd_start(self, message: types.Message):
        await message.answer(
            "Where do u want to use Retardio gifs?",
            reply_markup=self.get_keyboard()
        )

    async def send_video(self, callback: types.CallbackQuery, video_type: str):
        try:
            if self.file_ids[video_type] is None:
                video = FSInputFile(PATHS[video_type])
                sent_message = await callback.message.answer_video(
                    video=video,
                    caption=CAPTIONS[video_type],
                    parse_mode="HTML"
                )
                self.file_ids[video_type] = sent_message.video.file_id
            else:
                await callback.message.answer_video(
                    video=self.file_ids[video_type],
                    caption=CAPTIONS[video_type],
                    parse_mode="HTML"
                )
        except Exception as e:
            print(f"Error while sending {video_type} video: {e}")
            await callback.message.answer("Error occurred while sending the video.")

    async def handle_buttons(self, callback: types.CallbackQuery):
        try:
            video_type = callback.data.split('_')[0]
            await self.send_video(callback, video_type)
            await callback.answer()
        except Exception as e:
            print(f"Callback handling error: {e}")
            await callback.answer("Error occurred. Please try again.")

async def main():
    bot = VideoBot(BOT_TOKEN)
    await bot.dp.start_polling(bot.bot)

if __name__ == "__main__":
    asyncio.run(main())