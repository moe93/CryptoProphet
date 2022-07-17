#@formatter:off
"""
Telegram bot.
This class is the front-end of the bot. All other classes and interactions
tie-in and pour into this main class.


**NOTE: This class inherits TelegramBot_inApp.py**

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 15th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jul. 16th, 2022 Year of Our Lord
"""

# Needed for error logger
import  traceback                                                       # Manipulate traceback errors
import  html                                                            # Manipulate HTML data

# Class to inherit from
from    TelegramBot_inApp           import  *                           # Contains in-app setup and handling functions

# Graceful interrupt handler class
from    auxiliary.InterruptHandler  import  GracefulInterruptHandler as Grace

# Telegram bot classes and helpers
from    telegram                    import  ParseMode                   # Message parse modes (needed for HTML parsing)
from    telegram.ext                import  MessageHandler              # Handler class to handle messages
from    telegram.ext                import  Filters                     # Predefined filters to use with MessageHandler
from    telegram.ext                import  Dispatcher                  # Dispatch updates to bot
from    telegram.ext                import  CommandHandler              # Handle any command sent by the user

# Telegram type hinting imports
from    telegram.ext.utils.types    import  BD                          # BD : Type of the bot data
from    telegram.ext.utils.types    import  CCT                         # CCT: An instance of :class:`telegram.ext.CallbackContext`
from    telegram.ext.utils.types    import  CD                          # CD : Type of the chat data for a single user
from    telegram.ext.utils.types    import  UD                          # UD : Type of the user data for a single user

class TelegramBot( TelegramBotInApp ):
    
    # Add type hints
    bot_running = bool
    updater         : Union[ Updater[CCT, UD, CD, BD],
                             Updater[Union[CallbackContext, Any], Any, Any, Any] ]
    dispatcher      : Union[ Dispatcher[CCT, UD, CD, BD],
                             Dispatcher[Union[CallbackContext, Any], Any, Any, Any] ]
    commands_list   : List[BotCommand]
    commands_bot    : Bot
    
    def __init__( self, tg_token, tg_user_id ):
        super().__init__( tg_token, tg_user_id )                            # Initialize inherited class
        
        self.bot_running = False                                            # Bot is NOT running on start
        self.logger = self.setup_logger( 'TelegramBot_main' )               # Setup logger
        self.connect_bot()                                                  # Connect to the bot
        
    def connect_bot( self ) -> None :
        """
        The Updater class continuously fetches new updates from telegram
        and passes them on to the Dispatcher class.
        
        If you create an Updater object, it will create a Dispatcher for
        you and link them together with a Queue.
        :return: None
        """
        
        try:                                                                # Catch error
            self.updater    = Updater( token            = self.token,       #   Connect to bot
                                       use_context      = True,             #   ...
                                       user_sig_handler = Grace().handler ) #   ...
            self.dispatcher = self.updater.dispatcher                       #   Start dispatcher
            self._add_bot_commands()                                        #   Register commands to dispatcher
            
        except:                                                             # If error occurs
            raise Exception( 'Failed to connect to bot' )                   #   Catch and raise error
    
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
        Bot commands are added here.
        
        The full list of available command functions can be found
        in the TelegramBot_inApp.py file.
        
        :return: None
        """
        
        # Add the different commands
        self.dispatcher.add_handler( CommandHandler("help"              , self.help)         )
        self.dispatcher.add_handler( CommandHandler("set_commands"      , self.set_commands) )
        self.dispatcher.add_handler( CommandHandler("show_keyboard"     , self.show_keyboard))
        self.dispatcher.add_handler( CommandHandler("start"             , self.start)        )
        self.dispatcher.add_handler( CommandHandler("placeholder"       , self.placeholder)  )
        
        # ... and the error handler
        self.dispatcher.add_error_handler( self.error_handler )
        # Unknown commands are echoed back at user
        self.dispatcher.add_handler( MessageHandler(Filters.text    , self.text)        )

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
        update_str  = update.to_dict() if isinstance(update, Update) else str(update)
        update_html = html.escape(orjson.dumps(update_str, option=orjson.OPT_INDENT_2).decode('utf-8'))
        message = (
                f'An exception was raised while handling an update\n'
                f'<pre>update = {update_html}'
                '</pre>\n\n'
                f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
                f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
                f'<pre>{html.escape(tb_string)}</pre>'
        )
    
        # Finally, send the message
        context.bot.send_message(chat_id=self.user_id, text=message, parse_mode=ParseMode.HTML)


#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    # from dotenv     import  load_dotenv                                 # Read key-value pairs from a .env file
    # load_dotenv()                                                       # Load environment variables from .env
    #
    # from os         import  environ
    # token_      =   environ.get('tg_token')
    # user_id_    =   environ.get('tg_user_id')

    from dotenv     import  dotenv_values                               # Read key-value pairs from a .env file without modifying the environment
    from dotenv     import  find_dotenv                                 # Search for the .env within the main directory and subdirectories
    env_dir     = find_dotenv()                                         # Store absolute path to .env file
    token_      = dotenv_values( env_dir )['tg_token']                  # Read token
    bot_id_     = dotenv_values( env_dir )['tg_bot_id']                 # Read bot ID
    user_id_    = dotenv_values( env_dir )['tg_user_id']                # Read user ID
    
    bot = TelegramBot( token_, user_id_ )                               # Start bot
    bot.start_bot( blocking=False )                                     # Start bot with idling OFF (FALSE)
    bot.set_commands( None, None )                                      # Register commands with Telegram
    bot.updater.bot.send_message( text      = "Online and ready.",      # [INFO] ...
                                  chat_id   = user_id_ )                # ...
    bot.start_bot( blocking=True )                                      # Switch idling to ON (TRUE)

#   ----------------- ___ END ___: Setup script and run -----------------