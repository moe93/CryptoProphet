#@formatter:off
"""
Create a Telegram communication bot

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 15th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jun. 15th, 2022 Year of Our Lord
"""
from dotenv import load_dotenv
load_dotenv()

import os
token_ = os.environ.get('tg_token')
user_id_ = os.environ.get('tg_user_id')

# Class to inherit from
from    TelegramBot_main                    import  *

import  json
from    apscheduler.schedulers.background   import  BackgroundScheduler
from    telegram                            import  InlineKeyboardMarkup
from    telegram                            import  InlineKeyboardButton

CANCEL = ["200"]
class TelegramBotInApp( TelegramBot ):
    """
    Handle communication from within the app.
    """
    
    def __init__(self, tg_token, tg_id) -> None:
        super().__init__(tg_token, tg_id)
        self.scannerSchedule = BackgroundScheduler(timezone="UTC")
        self.dispatcher.add_handler( CommandHandler("showkeyboard"   , self.showkeyboard) )
        # self.commands_list.append( BotCommand( "get_request"          , "show help text + list of commands") )
        # self.commands_bot.set_my_commands(self.commands_list)

    def create_callback_data( self, callback_tag, exchange: str = "", parameter: str = "" ):
        return json.dumps( {"c": callback_tag, "e": exchange, "p": parameter} )
    
    def showkeyboard( self, update: Update, context: CallbackContext ) -> InlineKeyboardMarkup:
        """control panel buttons"""
        # Get user that sent /start and log his name
        user = update.message.from_user
        self.logger.info("User %s started the conversation.", user.first_name)
        keyboard = [ [InlineKeyboardButton("row_1"              , callback_data=1)],
                     # -------------------------------------
                     [InlineKeyboardButton("row_2_1"            , callback_data=2),
                      InlineKeyboardButton("row_2_2"            , callback_data=3),],
                     # -------------------------------------
                     [InlineKeyboardButton("row_3"              , callback_data=4),],
                     # -------------------------------------
                     [InlineKeyboardButton("row_4_1"            , callback_data=5),
                      InlineKeyboardButton("row_4_2"            , callback_data=6),],
                     # -------------------------------------
                     [InlineKeyboardButton("Cancel", callback_data = self.create_callback_data(CANCEL[0]),)],
                     ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
        return InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

#%% ----------------- ___START___: Setup script and run -----------------

bot = TelegramBot( token_, user_id_ )                               # Start bot
bot.start_bot( False )
bot.setcommands( None, None )
bot.commands_list.append( BotCommand( "showkeyboard"          , "shows keyboard. Does nothing for now") )
bot.commands_bot.set_my_commands(bot.commands_list)

#   ----------------- ___ END ___: Setup script and run -----------------