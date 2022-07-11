#@formatter:off
"""
Telegram helper class and functions

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 15th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jun. 15th, 2022 Year of Our Lord
"""

from    typing                      import  Any, List, Union                # Needed for type hinting
from    re                          import  compile                         # Use regex for validation
# import  orjson                                                          # Fast, efficient JSON parser

import html
import json
import  logging
from    datetime                    import  datetime
from    os                          import  path, curdir, makedirs

from    telegram                    import  Update
from    telegram                    import  InlineKeyboardMarkup
from    telegram                    import  CallbackQuery
from    telegram.ext                import  CallbackContext
from    telegram.ext                import  Updater

# Telegram type hinting imports
from    telegram.ext.utils.types    import  BD                              # BD : Type of the bot data
from    telegram.ext.utils.types    import  CCT                             # CCT: An instance of :class:`telegram.ext.CallbackContext`
from    telegram.ext.utils.types    import  CD                              # CD : Type of the chat data for a single user
from    telegram.ext.utils.types    import  UD                              # UD : Type of the user data for a single user

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
    
    def setup_logger( self, logger_name ) -> logging.Logger :
    
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
        
    def validate_config( self, tg_token: str, tg_id: str ) -> int :
        """
        Validate telegram token and user_id

        :param tg_token: Telegram bot token
        :param tg_id: Telegram user/client ID
        :return: None
        """
    
        pattern = compile( r'^\d{1,10}:[A-z0-9-_]{35,35}$' )
        if not pattern.match( tg_token ):
            raise Exception( 'Telegram token is invalid' )
        else:
            self.token = tg_token
    
        pattern = compile(r'^-?\d{7,13}$')
        if not pattern.match( tg_id ):
            raise Exception( 'Telegram user_id is invalid' )
        else:
            self.user_id = tg_id
            
        return 0
            
    def send_telegram_message( self, update : Update, reply,
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
            context = CallbackQuery( id             = '2',
                                     from_user      = self.user_id,
                                     chat_instance  ="",
                                     bot            = Updater(self.token, use_context=True).bot )

        if new_message or update == None:
            context.bot.send_message( chat_id=self.user_id,
                                      text=reply,
                                      reply_markup=markup,
                                      parse_mode="HTML" )
        else:
            context.bot.edit_message_text( chat_id=update.effective_message.chat_id,
                                           message_id=update.effective_message.message_id,
                                           text=reply,
                                           reply_markup=markup,
                                           parse_mode="HTML" )
            
#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    from os import environ
    token_ = environ.get('tg_token')
    user_id_ = environ.get('tg_user_id')
    bot = TelegramBotHelper( token_, user_id_ )                         # Start bot

#   ----------------- ___ END ___: Setup script and run -----------------