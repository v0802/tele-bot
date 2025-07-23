
import os
from telegram import Update, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ChatJoinRequestHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_GROUP_ID = int(os.getenv("MAIN_GROUP_ID"))
BACKUP_GROUP_ID = int(os.getenv("BACKUP_GROUP_ID"))

PRIVATE_GROUP_LINK = "https://t.me/malluvoicegroup"

async def welcome_restrict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_user = update.message.new_chat_members[0]

    await context.bot.restrict_chat_member(
        chat_id=MAIN_GROUP_ID,
        user_id=new_user.id,
        permissions=ChatPermissions(can_send_messages=False)
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Request Access to Private Group", url=PRIVATE_GROUP_LINK)]
    ])

    await context.bot.send_message(
        chat_id=MAIN_GROUP_ID,
        text=f"👋 Welcome {new_user.mention_html()}!\n\n🚫 You're restricted from chatting.\nPlease request to join our private backup group below. Once approved, you'll be unrestricted.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user

    await context.bot.approve_chat_join_request(chat_id=BACKUP_GROUP_ID, user_id=user.id)

    await context.bot.restrict_chat_member(
        chat_id=MAIN_GROUP_ID,
        user_id=user.id,
        permissions=ChatPermissions(can_send_messages=True,
                                    can_send_media_messages=True,
                                    can_send_other_messages=True,
                                    can_add_web_page_previews=True)
    )

    await context.bot.send_message(
        chat_id=MAIN_GROUP_ID,
        text=f"✅ {user.mention_html()} has been approved and can now chat.",
        parse_mode="HTML"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_restrict))
app.add_handler(ChatJoinRequestHandler(handle_join_request))

print("Bot is running...")
app.run_polling()
