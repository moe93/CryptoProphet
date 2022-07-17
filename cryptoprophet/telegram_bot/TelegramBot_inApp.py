#@formatter:off
"""
Create a Telegram communication bot

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 15th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jul. 16th, 2022 Year of Our Lord
"""

from    typing                              import  Any, List, Union            # Needed for type hinting
import  orjson                                                                  # Fast, efficient JSON parser

from    apscheduler.schedulers.background   import  BackgroundScheduler         # Background scheduling
from    telegram                            import  InlineKeyboardButton        # Telegram inline keyboard
from    telegram                            import  ReplyKeyboardRemove         # Remove keyboard after user input
from    telegram.bot                        import  Bot, BotCommand             # Make commands visible in-app

# Inherit from TelegramBot_helper.py
from    TelegramBot_helper                  import  *                           # Use "import *" to get all imports from module

CANCEL = ["200"]
class TelegramBotInApp( TelegramBotHelper ):
    """
    Handle communication from within the app.
    """
    # Type hints
    commands_list   : list
    commands_bot    : Bot
    
    def __init__( self, tg_token, tg_user_id ) -> None:
        super().__init__( tg_token, tg_user_id )                                # Initialize inherited class
        
        self.logger = self.setup_logger( 'TelegramBot_inApp' )                  # Setup logger
        self.scannerSchedule = BackgroundScheduler(timezone="UTC")              # Run scanner on specified schedule

    # ----------------- ___START___: create_callback_data -----------------
    @staticmethod
    def create_callback_data( callback_tag, exchange: str = "", parameter: str = "" ):
        try:
            callback_data = orjson.dumps( {"c": callback_tag, "e": exchange, "p": parameter} )
            print( callback_data.decode('utf-8') )
        except TypeError:
            raise
        
        return callback_data.decode('utf-8')                                    # Return decoded callback data

    # Here is where we start defining bot commands
    # ------------------------- ___START___: help -------------------------
    def help( self, update: Update, context: CallbackContext ) -> None :
        """
        Sends a message when the command /help is issued.

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        
        txt  = '<b>List of available commands.</b> \n\n'
        txt += '<b>/help</b> - <i>shows this text message</i>\n'
        txt += '<b>/set_commands</b> - <i>sets commands in the Telegram GUI</i>\n'
        txt += '<b>/show_keyboard</b> - <i>show the keyboard</i>\n'
        txt += '<b>/start</b> - <i>for now only greets user</i>\n'
        txt += '<b>/placeholder</b> - <i>placeholder function</i>\n'
        
        self.send_telegram_message( update, f'{txt}', context=context)
    
    # --------------------- ___START___: set_commands ---------------------
    def set_commands( self, update: Update, context: CallbackContext ) -> None :
        """
        Sets commands to be visible within the app for easier access

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        self.commands_list = [ BotCommand( "help"           , "show help text + list of commands"),
                               BotCommand( "set_commands"   , "sets commands in the Telegram GUI"),
                               BotCommand( "show_keyboard"  , "show the keyboard"),
                               BotCommand( "start"          , "for now only greets user"),
                               BotCommand( "placeholder"    , "placeholder function")
                               ]
        print( '[INFO] Setting commands in the Telegram GUI...', end='' )
        self.commands_bot = Bot( self.token )
        self.commands_bot.set_my_commands( self.commands_list )
        print( "DONE!" )
        # context.bot.send_message( chat_id=self.user_id, text='Hello and welcome' )
        self.send_telegram_message(
                update,
                "<i>Bot Commands Created</i>",
                ReplyKeyboardRemove(),
                context=context,
                )

    # ------------------------ ___START___: start -------------------------
    def start( self, update: Update, context: CallbackContext ) -> None :
        """
        Sends a message when the command /start is issued.

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        txt = f"Hello, I am {self.updater.bot['first_name']}"
        update.message.reply_text( f'{txt}' )

    # ---------------------- ___START___: placeholder ---------------------
    @staticmethod
    def placeholder( update: Update, context: CallbackContext ) -> None :
        """
        Placeholder function

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        txt = 'I am a placeholder function'
        update.message.reply_text( f'{txt}' )

    # ------------------------- ___START___: text -------------------------
    # def text( self, update_obj: Update, context: MessageHandler ) -> Any :
    @staticmethod
    def text( update: Update, context: Any ) -> Any :
        """
        Function to handle normal text

        :param update:
        :param context: MessageHandler:
        :return: None
        """

        text_received = update.message.text
        txt = \
        f'''
        "{text_received}" is not a known command. \n
        Please see /help for a list of all available commands
        '''
        update.message.reply_text( f'{txt}' )
    
    # --------------------- ___START___: show_keyboard ---------------------
    def show_keyboard( self, update: Update, context: CallbackContext ) -> InlineKeyboardMarkup:
        """
        Control panel buttons
        
        :param update:
        :param context:
        :return: InlineKeyboardMarkup
        """
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

        # Send message with text and appended InlineKeyboard
        reply_markup    = InlineKeyboardMarkup( keyboard, one_time_keyboard=True )  # Inline keyboard with options in list above
        reply_text      = '<i>Start handler, Choose a route</i>'                    # Reply text to send

        # update.message.reply_text( text         = f'{reply_text}',              # Send message with reply_text
        #                            reply_markup = reply_markup )                # ... and append inline keyboard
        self.send_telegram_message( update                  ,
                                    reply   = reply_text    ,
                                    markup  = reply_markup  ,
                                    context = context )

        return reply_markup

#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv     import  load_dotenv
    load_dotenv()
    
    from os         import  environ
    token_      =   environ.get('tg_token')
    user_id_    =   environ.get('tg_user_id')
    
    bot = TelegramBotInApp( token_, user_id_ )                               # Start bot

#   ----------------- ___ END ___: Setup script and run -----------------