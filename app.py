from pyrogram import *

from pyrogram.types import *

import music_search as api

from save_data import *

BOTTOKEN = "" # @botfather
 
APIID    = 33 # my.telegram.org

APIHASH  = "" # my.telegram.org

app = Client(
    "music_bot", 
    bot_token = BOTTOKEN,
    api_id = APIID,
    api_hash = APIHASH,
)

@app.on_message(filters.command('start'))
async def command_start(client:Client, message:Message):

    await app.set_bot_commands(
        [BotCommand("start", 'شروع')]
    )
    await message.reply_text(".سلام. لطفا نام آهنگ یا خواننده مورد نظر خود را ارسال کنید.")

@app.on_message(filters.text & filters.private)
async def song_search(client:Client, message:Message):
    search = message.text
    user = message.chat.id
    
    # search history
    save_data(user, search) 
    
    if len(search) >= 50: 
        await message.reply_text(
            "پیام خیلی بزرگ است. لطفا یک پیام با طول کمتر ارسال کنید."
            )
        return
    
    else:
        results = api.search_music(search, 1)
        if len(results) == 0:
            await message.reply_text(
                'چیزی پیدا نشد.',
            )
            return
        
        buttons = []
        
        i = 0
        
        for result in results:
            btn = InlineKeyboardButton(
                result['title'], 
                str(i)+ "_" + str(1) + "_" + search
            )
            buttons.append([btn])
            
            i += 1
            
        next_btn = InlineKeyboardButton(
            "صفحه بعد",
            "N_1_"+search # N_1_mehdi --> N: next page, 1: page, search: mehdi
        )
        
        buttons.append([next_btn])
        
        answer = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            "لطفا از لیست زیر یکی را انتخاب کنید.",
            reply_markup= answer
        )

@app.on_callback_query()
async def callback(client:Client, callback_query:CallbackQuery):
    callback_data = callback_query.data
    
    callback_data = callback_data.split('_')
    
    key = callback_data[0]
    page = int(callback_data[1])
    search = callback_data[2]
    
    if key == "N":
        page += 1
        results = api.search_music(search, page)
        
        if len(results) == 0:
            await callback_query.answer("مورد دیگری پیدا نشد.",
                                  show_alert = False)
            return
        
        buttons = []
        
        i = 0
        
        for result in results:
            btn = InlineKeyboardButton(
                result['title'], 
                str(i)+ "_" + str(page) + "_" + search # 10_2_mehdi
            )
            buttons.append([btn])
            
            i += 1
            
        next_btn = InlineKeyboardButton(
            "صفحه بعد",
            f"N_{page}_"+search
        )
        prev_btn = InlineKeyboardButton(
            "صفحه قبل",
            f"P_{page}_"+search # P_2_mehdi
        )
        
        buttons.append([prev_btn, next_btn])
        answer = InlineKeyboardMarkup(buttons)
        
        await callback_query.message.edit(
            "لطفا از لیست زیر یکی را انتخاب کنید.\n"+'صفحه: '+str(page),
            reply_markup= answer
        )
        
    elif key == "P":
        page -= 1
        results = api.search_music(search, page)
        if len(results) == 0:
            await callback_query.answer("مورد دیگری پیدا نشد.",
                                show_alert = False)
            return
        
        buttons = []
        
        i = 0
        
        for result in results:
            btn = InlineKeyboardButton(
                result['title'], 
                str(i)+ "_" + str(page) + "_" + search
            )
            buttons.append([btn])
            
            i += 1
            
        next_btn = InlineKeyboardButton(
            "صفحه بعد",
            f"N_{page}_"+search
        )
        
        prev_btn = InlineKeyboardButton(
            "صفحه قبل",
            f"P_{page}_"+search
        )
        
        if page > 1:
            buttons.append([prev_btn, next_btn])
        else:
            buttons.append([next_btn])
            
        answer = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit(
            "لطفا از لیست زیر یکی را انتخاب کنید.\n"+'صفحه: '+str(page),
            reply_markup= answer
        )
    elif key == "D1":
        results = api.search_music(search, page)
        target  = int(callback_data[3])
        
        link    = results[target]["d320"]
        await callback_query.message.reply_audio(
            link
        )
    elif key == "D2":
        results = api.search_music(search, page)
        target  = int(callback_data[3])
        
        link    = results[target]["d128"]
        await callback_query.message.reply_audio(
            link
        )  
    else:
        results = api.search_music(search, page)
        key = int(key)
        
        message = search
        answer = results[key]
        
        buttons = []
        cover = None
        
        if answer['photo'] is not None:
            cover = answer['photo']
            
        if answer["link"] is not None:
            link = answer['link']
            btn_link = InlineKeyboardButton("link", url=link)
            buttons.append([btn_link])
            
        if answer["d320"] is not None:
            btn_320 = InlineKeyboardButton("Download 320", 
                                           f"D1_{page}_"+search+"_"+str(key)) # D1_1_mehdi_1
            buttons.append([btn_320])
            
        if answer["d128"] is not None:
            btn_128 = InlineKeyboardButton("Download 128", 
                                           f"D2_{page}_"+search+"_"+str(key)) # D2_1_mehdi_1
            buttons.append([btn_128])
            
        if answer['title'] is not None:
            message += '\n' + answer['title']
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        if cover is not None:
            await callback_query.message.reply_photo(cover, caption=message, reply_markup=keyboard)
        else:
            await callback_query.message.reply_text(message, reply_markup=keyboard)
    
    
    await callback_query.answer("انجام شد.",
        show_alert = False)
    return
        
app.run()
