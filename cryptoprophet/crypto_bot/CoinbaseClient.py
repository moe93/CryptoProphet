#@formatter:off
"""
Create a Coinbase Pro client here

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 13th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jul. 31st, 2022 Year of Our Lord
"""

import  pandas                      as      pd                              # Dataframes to facilitate analysis
from    re                          import  compile                         # Use regex for validation
from    os                          import  getcwd                          # Get current working directory
from    os.path                     import  join                            # Create path that is agnostic to OS
from    time                        import  time                            # Get time
from    requests.auth               import  AuthBase                        # Base class that all auth implementations derive from
import  requests                                                            # HTTP GET and POST for API interaction
import  hmac                                                                # Keyed-Hashing for Message Authentication
import  hashlib                                                             # Secure hash and message digest algorithms
import  orjson                                                              # Fast, efficient JSON parser


class CoinbaseClient( AuthBase ):
    
    # Add type hints
    _cb_key         : str = None
    _cb_secret      : str = None
    api_url         : str = 'https://api.coinbase.com/v2/'
    
    def __init__( self, key, secret ):
        self.str = "Call Crypto Bot main application code here"
        self.validate_api( key, secret )                                    # Validate API entries

    def __call__( self, request ):
        timestamp   = str( int(time()) )                                    # Get current time as string
        
        message     = timestamp + request.method + request.path_url + (request.body or '')
        b_message   = message.encode( 'UTF-8' )                             # Encode message as bytes
        b_secret    = (self._cb_secret).encode( 'UTF-8' )                   # Encode secret as bytes
        signature   = hmac.new( b_secret, b_message, hashlib.sha256 ).hexdigest()
    
        request.headers.update( { 'CB-ACCESS-SIGN'      : signature     ,
                                  'CB-ACCESS-TIMESTAMP' : timestamp     ,
                                  'CB-ACCESS-KEY'       : self._cb_key  } )
        return request
    
    def validate_api( self, _key: str, _secret: str ) -> int:
        """
        Validate Coinbase API information.
        
        Note on RegEx:
            - The leading ^ and the trailing $ are known as position anchors, which match the start
            and end positions of the line, respectively. As the result, the entire input string
            shall be matched fully, instead of a portion of the input string (substring).
            
            - {m}   : The preceding item is matched exactly m times
            - {m,n} : The preceding item is matched at least m times, but not more than n times.
            -   \   : Backslash is an escape character (i.e. \[ matches "[")
            -   +   : Plus sign indicates one or more occurrences of the preceding element.
                      For example, ab+c matches "abc", "abbc", "abbbc", and so on, but not "ac".
                      
        :param _key:
        :param _secret:
        :return:
        """
        
        # Key
        pattern = compile( r'^[A-z0-9]{16}$' )                              # Validates API key
        if not pattern.match( _key ):                                       # If NOT valid
            raise ValueError( "Coinbase API key is invalid" )               #   Raise error
        else:                                                               # Else, if it is correct
            self._cb_key = _key                                             #   Store API key
            
        # Secret
        pattern = compile( r'^[A-z0-9]{32}$' )                               # Validates API secret
        if not pattern.match( _secret ):                                    # If NOT valid
            raise ValueError( "Coinbase API secret is invalid" )            #   Raise error
        else:                                                               # Else, if it is correct
            self._cb_secret = _secret                                       #   Store API secret
        
        return 0
    
    

#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv     import  dotenv_values                               # Read key-value pairs from a .env file without modifying the environment
    from dotenv     import  find_dotenv                                 # Search for the .env within the main directory and subdirectories
    env_dir         = find_dotenv()                                     # Store absolute path to .env file
    cb_key          = dotenv_values( env_dir )['cb_key']                # Read key
    cb_secret       = dotenv_values( env_dir )['cb_secret']             # Read secret
    
    cb_client = CoinbaseClient( cb_key, cb_secret )                     # Start client
    r = requests.get( cb_client.api_url + 'user', auth = cb_client )    # Get current user
    print( r.json() )
    print( orjson.loads( r.content ) )

#   ----------------- ___ END ___: Setup script and run -----------------
