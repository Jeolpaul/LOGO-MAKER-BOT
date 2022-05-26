from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from main.logo import generate_logo
from beta.database import insert, getid
from beta.utils import not_subscribed
from config import ADMIN


START = """
**🔮 Hello {},\nYou Can Use Me To Create Awesome Logos...**

➤ Click The Button Below To Know How To Use Me
"""

HELP = """
**🖼 How To Use Me ?**

**To Make Logo -** `/logo Your Name`
**To Make Square Logo - ** `/logosq Your Name`

**♻️ Example:** 
`/logo Beta`
`/logosq BetaBots`
"""

@Client.on_message(filters.private & filters.create(not_subscribed))
async def is_not_subscribed(client, message):
    await message.reply_text(
       text="**⚠️Sorry bro,You didn't Joined Our Updates Channel Join now and start again🙏**",
       reply_markup=InlineKeyboardMarkup([
           [ InlineKeyboardButton(text="📢𝙹𝚘𝚒𝚗 𝙼𝚢 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕📢", url=client.invitelink)]
           ])
       )

# Commands
@app.on_message(filters.command("start"))
async def start(bot, message):   
    insert(int(message.chat.id))
    await message.reply_photo(
        photo="https://telegra.ph//file/69b6154eaecdaf3845d9f.jpg",
        caption=START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Help", callback_data="help_menu"),
            InlineKeyboardButton(text="Developer", url="t.me/beta_bot_updates")
            ]]
            )
        )


@app.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply_photo("https://telegra.ph//file/69b6154eaecdaf3845d9f.jpg",caption=HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="start_menu")]]))

@app.on_message(filters.command("logo") & filters.incoming & filters.text & ~filters.forwarded & (
  filters.group | filters.private))
async def logo(bot, message):
  try:
    text = message.text.replace("logo","").replace("/","").replace("@beta_bot_updates","").strip().upper()
    
    if text == "":
      return await message.reply_text(HELP)

    x = await message.reply_text("`🔍 Generating Logo For You...`")  
    logo = await generate_logo(text)

    if "telegra.ph" not in logo:
      return await x.edit("`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT")
      
    if "error" in logo:
      return await x.edit(f"`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT \n\n`{logo}`")
      
    await x.edit("`🔄 Done Generated... Now Sending You`")

    logo_id = logo.replace("https://telegra.ph//file/","").replace(".jpg","").strip()
    await message.reply_photo(logo,caption="**🖼 Logo Generated By @JP_Jeol_org**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Upload As File 📁", callback_data=f"flogo {logo_id}")]]))
    await x.delete()
  except FloodWait:
    pass
  except Exception as e:
    try:
      await x.delete()
    except:
      pass
    return await message.reply_text("`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT")

# Square Logo
@app.on_message(filters.command("logosq") & filters.incoming & filters.text & ~filters.forwarded & (
  filters.group | filters.private))
async def logo(bot, message):
  try:
    text = message.text.replace("logosq","").replace("/","").replace("@beta_bot_updates","").strip().upper()
      
    if text == "":
      return await message.reply_text(HELP)
  
    x = await message.reply_text("`🔍 Generating Logo For You...`")  
    logo = await generate_logo(text,True)
  
    if "telegra.ph" not in logo:
      return await x.edit("`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT)
        
    if "error" in logo:
      return await x.edit(f"`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT \n\n`{logo}`")
      
    await x.edit("`🔄 Done Generated... Now Sending You`")
    
    logo_id = logo.replace("https://telegra.ph//file/","").replace(".jpg","").strip()
    
    await message.reply_photo(logo,caption="**🖼 Logo Generated By @JP_Jeol_org**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Upload As File 📁", callback_data=f"flogo {logo_id}")]]))
    await x.delete()
  except FloodWait:
    pass
  except Exception as e:
    try:
      await x.delete()
    except:
      pass
    return await message.reply_text("`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT)

#broadcast

@app.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
 if (message.reply_to_message):
   ms = await message.reply_text("Geting All ids from database ...........")
   ids = getid()
   tot = len(ids)
   await ms.edit(f"Starting Broadcast .... \n Sending Message To {tot} Users")
   for id in ids:
     try:
     	await message.reply_to_message.copy(id)
     except:
     	pass

@app.on_message(filters.private & filters.user(ADMIN) & filters.command(["users"]))
async def get_users(client: Client, message: Message):    
    msg = await client.send_message(chat_id=message.chat.id, text="അവിടെ നില്ല് ഇപ്പോ തരാം 🤨")
    ids = getid()
    tot = len(ids)
    await msg.edit(f"Total uses = {tot}")


# Callbacks
@app.on_callback_query(filters.regex("start_menu"))
async def start_menu(_,query):
  await query.answer()
  await query.message.edit(START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", callback_data="help_menu"),InlineKeyboardButton(text="Repo", url="https://github.com/Jeolpaul/LOGO-MAKER-BOT")]]))

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(_,query):
  await query.answer()
  await query.message.edit(HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="start_menu")]]))

@app.on_callback_query(filters.regex("flogo"))
async def logo_doc(_,query):
  await query.answer()
  try:
    x = await query.message.reply_text("`🔄 Sending You The Logo As File`")
    await query.message.edit_reply_markup(reply_markup=None)
    link = "https://telegra.ph//file/" + query.data.replace("flogo","").strip() + ".jpg"
    await query.message.reply_document(link,caption="**🖼 Logo Generated By @JP_Jeol_org)
  except FloodWait:
    pass
  except Exception as e:
    try:
      return await x.edit(f"`❌ Something Went Wrong...`\n\nReport This Error In @BETA_BOTSUPPORT \n\n`{str(e)}`")
    except:
      return
    
  return await x.delete()
  

if __name__ == "__main__":
  print("==================================")
  print("[INFO]: LOGO MAKER BOT STARTED BOT SUCCESSFULLY")
  print("=======JOIN @beta_bot_updates=========")

  idle()
  print("[INFO]: LOGO MAKER BOT STOPPED")
