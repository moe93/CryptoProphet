#@formatter:off
"""
Telegram helper class and functions.
Currently, this class creates the loggers, validates the telegram token
and user ID, and facilitates sending messages from the bot to the user.

*** NOTE: This class is to be inherited by TelegramBot_inApp.py

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered

AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 15th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jul. 16th, 2022 Year of Our Lord
"""

from    re                          import  compile                         # Use regex for validation

import  logging
from    datetime                    import  datetime
from    os                          import  path, curdir, makedirs

from    telegram                    import  Update
from    telegram                    import  InlineKeyboardMarkup
from    telegram                    import  CallbackQuery
from    telegram.ext                import  CallbackContext
from    telegram.ext                import  Updater

class TelegramBotHelper( object ):
    """
    Telegram bot helper class:
    
    - Create commands
    - Log errors
    - Send messages
    - etc...
    """
    # Add type hints
    token       : str;   user_id     : str
    logger      : logging.Logger
    def __init__(self, tg_token, tg_user_id ) -> None:
        
        self.logger = self.setup_logger( logger_name='TelegramBot_helper' ) # Setup logger
        if( self.validate_config( tg_token, tg_user_id ) == 0 ):            # Validate login info
            self.logger.info( 'Telegram token and user ID validated successfully' )

    # --------------------- ___START___: setup_logger ---------------------
    @staticmethod
    def setup_logger( logger_name ) -> logging.Logger :
    
        log_path    = path.join( curdir, "logs", "TelegramBot" )            # Log directory
        if path.exists( log_path ) is False:                                # If directory does NOT exist
            makedirs( log_path )                                            #   Create directory

        log_name    = f"helper__{datetime.now().strftime('%Y-%m-%d')}.log"  # Log name
        log_path    = path.join( log_path, log_name )                       # Log directory
        log_format  = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"# Log format
        logging.basicConfig( filename   = log_path,                         # Configure logger
                             filemode   = "w",                              # ...
                             format     = log_format,                       # ...
                             level      = logging.INFO )                    # ...
        
        return logging.getLogger( logger_name )                             # Create and return logger

    # -------------------- ___START___: validate_config -------------------
    def validate_config( self, tg_token: str, tg_id: str ) -> int :
        """
        Validate telegram token and user_id

        :param tg_token: Telegram bot token
        :param tg_id: Telegram user/client ID
        :return: None
        """
    
        pattern = compile( r'^\d{1,10}:[A-z0-9_]{35}$' )                # Telegram token starts with 10digits then a (:)
        if not pattern.match( tg_token ):                                   # If pattern does NOT match
            raise Exception( 'Telegram token is invalid' )                  #   Raise error
        else:                                                               # Else
            self.token = tg_token                                           #   Store Telegram token
    
        pattern = compile(r'^-?\d{7,13}$')                                  # User ID consists of 10 digits
        if not pattern.match( tg_id ):                                      # If pattern does NOT match
            raise Exception( 'Telegram user_id is invalid' )                #   Raise error
        else:                                                               # Else
            self.user_id = tg_id                                            #   Store Telegram user ID
            
        return 0

    # ----------------- ___START___: send_telegram_message ----------------
    def send_telegram_message( self, update : Update, reply : str,
                               markup       : InlineKeyboardMarkup  = None,
                               context      : CallbackContext       = None,
                               new_message  : bool                  = True ):
        """
        Send messages to the Telegram bot
        :param update:
        :param reply:
        :param markup:
        :param context:
        :param new_message:
        :return:
        """
        if context is None:
            updater_bot = Updater(self.token, use_context=True).bot
            context = CallbackQuery( id             = '2', from_user= self.user_id,
                                     chat_instance  = "" , bot      = updater_bot )

        if new_message or update is None:
            context.bot.send_message( chat_id       = self.user_id  , text      = reply,
                                      reply_markup  = markup        , parse_mode= "HTML" )
        else:
            context.bot.edit_message_text( chat_id      = update.effective_message.chat_id,
                                           message_id   = update.effective_message.message_id,
                                           text = reply, reply_markup = markup, parse_mode = "HTML" )
            
#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv     import  load_dotenv
    load_dotenv()
    
    from os         import  environ
    token_      =   environ.get('tg_token')
    user_id_    =   environ.get('tg_user_id')
    
    bot = TelegramBotHelper( token_, user_id_ )                         # Start bot

#   ----------------- ___ END ___: Setup script and run -----------------