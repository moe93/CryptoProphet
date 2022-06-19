#@formatter:off
"""
Create a Coinbase Pro client here

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Jun. 13th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Jun. 14th, 2022 Year of Our Lord
"""

import  coinbasepro                 as      cbp                         # Official API for Coinbase Pro
import  pandas                      as      pd                          # Dataframes to facilitate analysis
from    re                          import  compile                     # Use regex for validation
from    os                          import  getcwd                      # Get current working directory
from    os.path                     import  join                        # Create path that is agnostic to OS
import  orjson                                                          # Fast, efficient JSON parser

class CoinbaseProClient( object ):
    def __init__( self, _key, _secret, _passphrase ):
        self.str = "Call Crypto Bot main application code here"
        self._key           = None                                      # Initiate internal API key
        self._secret        = None                                      # Initiate internal API secret
        self._passphrase    = None                                      # Initiate internal API passphrase
        self.validate_api_login( _key, _secret, _passphrase )           # Validate API entries

        self.client = None                                     # Initiate exchange client
        self.start_client()                                             # Start client

        self.dataframe = None
        
    def validate_api_login( self, _key, _secret, _passphrase ):
        """
        Note on RegEx:
            - The leading ^ and the trailing $ are known as position anchors, which match the start
            and end positions of the line, respectively. As the result, the entire input string
            shall be matched fully, instead of a portion of the input string (substring).
            
            - {m}   : The preceding item is matched exactly m times
            - {m,n} : The preceding item is matched at least m times, but not more than n times.
            -   \   : Backslash is an escape character (i.e. \[ matches "[")
            -   +   : Plus sign indicates one or more occurrences of the preceding element.
                      For example, ab+c matches "abc", "abbc", "abbbc", and so on, but not "ac".
        :return:
        """
        # Key
        p = compile( r'^[a-f0-9]{32}$' )                                # Validates API key
        if not p.match( _key ):                                         # If NOT valid
            raise ValueError( "Coinbase Pro API key is invalid" )       #   Raise error
        else:                                                           # Else, if it is correct
            self._key = _key                                            #   Store API key
            
        # Secret
        p = compile( r'^[A-z0-9+\/]+==$' )                              # Validates API secret
        if not p.match( _secret ):                                      # If NOT valid
            raise ValueError( "Coinbase Pro API secret is invalid" )    #   Raise error
        else:                                                           # Else, if it is correct
            self._secret = _secret                                      #   Store API secret
        
        # Passphrase
        p = compile( r'^[A-z0-9#$%=@!{},`~&*()<>?.:;_|^/+\[\]]{8,32}$' )# Validates API secret
        if not p.match( _passphrase ):                                  # If NOT valid
            raise ValueError( "Coinbase Pro API passphrase is invalid" )#   Raise error
        else:                                                           # Else, if it is correct
            self._passphrase = _passphrase                              #   Store API _passphrase
        
        return 0
    
    def start_client( self ) -> cbp.AuthenticatedClient :
        """ Client is used to query data """
        self.client = cbp.AuthenticatedClient( self._key,  self._secret, self._passphrase )
        return self.client
    
    def get_dataframe( self,
                       ticker: str,
                       start: Optional[str] = None,
                       stop: Optional[str] = None,
                       granularity: Optional[str] = None,
                       ) -> pd.DataFrame:
        """ Query historical data and return as a pandas dataframe """
        self.dataframe = self.client.get_product_historic_rates( ticker,
                                                                 start,
                                                                 stop,
                                                                 granularity )
        return pd.DataFrame( self.dataframe )
    
    def main( self ):
        """Entry point for the application script"""
        print( self.str )


# api_path = join( getcwd(), 'venv' )                                     # Directory where the cbp_key.json lives
api_path = '../../venv'                                                 # Directory where the cbp_key.json lives
api_file = join( api_path, 'cbp_key.json' )                             # Complete path to cbp_key.json file
with open( api_file, 'r' ) as f:                                        # Open cbp_key.json file for reading
    api_data = orjson.loads( f.read() )                                 #   Read cbp_key.json file

key         = api_data[ 'key'        ]                                  # Populate data from cbp_key.json file
secret      = api_data[ 'secret'     ]                                  # ...
passphrase  = api_data[ 'passphrase' ]                                  # ...

cbp_client = CoinbaseProClient( key, secret, passphrase )
cbp_client.client.get_product_24hr_stats( 'ETH-USD' )

df = cbp_client.get_dataframe( 'BTC-USD' )
print( df )