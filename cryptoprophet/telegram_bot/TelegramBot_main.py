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

from    typing                      import  Any, List, Union                  # Needed for type hinting
# import  orjson                                                          # Fast, efficient JSON parser

import html
import json
import traceback

from    telegram                    import  ReplyKeyboardRemove, Update
from    telegram                    import  ParseMode
from    telegram.ext                import  CallbackContext
from    telegram.ext                import  Updater
from    telegram.ext                import  Dispatcher
from    telegram.ext                import  CommandHandler              # Handle any command sent by the user
from    telegram.bot                import  Bot, BotCommand             # Make commands visible in-app

# Telegram type hinting imports
from    telegram.ext.utils.types    import  BD                          # BD : Type of the bot data
from    telegram.ext.utils.types    import  CCT                         # CCT: An instance of :class:`telegram.ext.CallbackContext`
from    telegram.ext.utils.types    import  CD                          # CD : Type of the chat data for a single user
from    telegram.ext.utils.types    import  UD                          # UD : Type of the user data for a single user

# from    TelegramBot_inApp           import  TelegramBotInApp
from    TelegramBot_helper          import  TelegramBotHelper
from    auxiliary.InterruptHandler  import  GracefulInterruptHandler as Grace

class TelegramBot( object ):
    
    # Add type hints
    token           : str;   user_id     : str;     bot_running = bool
    updater         : Union[ Updater[CCT, UD, CD, BD],
                             Updater[Union[CallbackContext, Any], Any, Any, Any] ]
    dispatcher      : Union[ Dispatcher[CCT, UD, CD, BD],
                             Dispatcher[Union[CallbackContext, Any], Any, Any, Any] ]
    commands_list   : List[BotCommand]
    commands_bot    : Bot
    
    def __init__( self, tg_token, tg_id ):
        self.helper = TelegramBotHelper( tg_token, tg_id )
        self.logger = self.helper.setup_logger( 'TelegramBot_main' )        # Setup logger
        self.token  = self.helper.token                                     # Extract validated token
        self.user_id= self.helper.user_id                                   # Extract validated user ID
        # self.inApp  = TelegramBotInApp()

        self.bot_running = False
        self.connect_bot()                                                  # Connect to the bot
        
    def connect_bot( self ) -> None :
        """
        The Updater class continuously fetches new updates from telegram
        and passes them on to the Dispatcher class.
        
        If you create an Updater object, it will create a Dispatcher for
        you and link them together with a Queue.
        :return: None
        """
        
        try:
            self.updater    = Updater( token            = self.token,       # Connect to bot
                                       use_context      = True,             # ...
                                       user_sig_handler = Grace().handler )
            self.dispatcher = self.updater.dispatcher                       # Start dispatcher
            
        except:                                                             # If it fails
            raise Exception( 'Failed to connect to bot' )                   #   Raise error
        
        finally:
            self._add_bot_commands()                                        # Register commands to dispatcher
    
    def start_bot( self, blocking = True ) -> None:
        """
        Starts the bot.
        
        :param blocking: boolean flag. If True, bot is run on idle
                         mode (i.e. blocks python console). [Default: True]
        :return: None
        """
        if( self.bot_running is not True ):                                 # Check if bot is running or not
            self.updater.start_polling()                                    #   If not, start pooling connection
            self.bot_running = True                                         #   Set bot_running flag to True
            
        if( blocking ):                                                     # If blocking flag is True
            self.updater.idle()                                             #   Run the bot until Ctrl-C
        else: pass
        
    def _add_bot_commands( self ) -> None :
        """
        Desired bot commands are added here.
        
        :return: None
        """
        
        # Add the different commands
        self.dispatcher.add_handler( CommandHandler("help"          , self.help)        )
        self.dispatcher.add_handler( CommandHandler("setcommands"   , self.setcommands) )
        self.dispatcher.add_handler( CommandHandler("start"         , self.start)       )
        self.dispatcher.add_handler( CommandHandler("placeholder"   , self.placeholder) )
        # ... and the error handler
        self.dispatcher.add_error_handler( self.error_handler )
        # Unknown commands are echoed back at user
        # self.dispatcher.add_handler( MessageHandler(Filters.text    , self.text)        )

    # This here is for logging errors
    def error_handler( self, update: object, context: CallbackContext ) -> None:
        """
        Log the error and send a telegram message to notify the developer.
        """
        # Log the error before we do anything else, so we can see it even if something breaks.
        self.logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)
    
        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
                f'An exception was raised while handling an update\n'
                f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
                '</pre>\n\n'
                f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
                f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
                f'<pre>{html.escape(tb_string)}</pre>'
        )
    
        # Finally, send the message
        context.bot.send_message(chat_id=self.user_id, text=message, parse_mode=ParseMode.HTML)
        
    # Here is where we start defining bot commands
    def help( self, update: Update, context: CallbackContext ) -> None :
        """
        Sends a message when the command /help is issued.
        
        :param update:
        :param context: CallbackContext:
        :return: None
        """
        
        txt = \
        '''
        Available Commands :-
        /help           - shows this text message
        /setcommands    - sets commands in the Telegram GUI
        /start          - for now only greets user
        /placeholder    - placeholder function
        '''
        update.message.reply_text( f'{txt}' )
    
    def setcommands( self, update: Update, context: CallbackContext ) -> None :
        """
        Sets commands to be visible within the app for easier access

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        self.commands_list = [ BotCommand( "help"           , "show help text + list of commands"),
                               BotCommand( "setcommands"    , "sets commands in the Telegram GUI"),
                               BotCommand( "start"          , "for now only greets user"),
                               BotCommand( "placeholder"    , "placeholder function")
                               ]
        print( '[INFO] Setting commands in the Telegram GUI...', end='' )
        self.commands_bot = Bot( self.token )
        self.commands_bot.set_my_commands( self.commands_list )
        print( "DONE!" )
        # context.bot.send_message( chat_id=self.user_id, text='Hello and welcome' )
        self.helper.send_telegram_message(
                update,
                "<i>Bot Commands Created</i>",
                ReplyKeyboardRemove(),
                context=context,
                )
        
    def start( self, update: Update, context: CallbackContext ) -> None :
        """
        Sends a message when the command /start is issued.

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        txt = f"Hello, I am {self.updater.bot['first_name']}"
        update.message.reply_text( f'{txt}' )
    
    def placeholder( self, update: Update, context: CallbackContext ) -> None :
        """
        Placeholder function

        :param update:
        :param context: CallbackContext:
        :return: None
        """
        txt = 'I am a placeholder function'
        update.message.reply_text( f'{txt}' )
        
    # def text( self, update_obj: Update, context: MessageHandler ) -> Any :
    def text( self, update_obj: Update, context: Any ) -> Any :
        """
        Function to handle normal text
        
        :param update_obj:
        :param context: MessageHandler:
        :return: None
        """
        
        text_received = update_obj.message.text
        txt = \
        f'''
        "{text_received}" is not a known command. \nPlease see /help for a list of all available commands
        '''
        update_obj.message.reply_text( f'{txt}' )


#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv     import  load_dotenv
    load_dotenv()
    
    from os         import  environ
    token_      =   environ.get('tg_token')
    user_id_    =   environ.get('tg_user_id')

    bot = TelegramBot( token_, user_id_ )                               # Start bot
    bot.start_bot( blocking=False )                                     # Start bot with idling OFF (FALSE)
    bot.setcommands( None, None )                                       # Register commands with Telegram
    bot.updater.bot.send_message( text      = "Online and ready.",      # [INFO] ...
                                  chat_id   = user_id_ )                # ...
    bot.start_bot( blocking=True )                                      # Switch idling to ON (TRUE)

#   ----------------- ___ END ___: Setup script and run -----------------