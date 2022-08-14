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
from    CoinbaseAuth                import  CoinbaseAuthClient


class CoinbaseClient( AuthBase ):
    
    # Add type hints
    _cb_key         : str = None
    _cb_secret      : str = None
    API_URL         : str = 'https://api.coinbase.com/v2/'
    
    def __init__( self, key: str, secret: str, url: str = None ) -> None:
        if url is not None:                                                 # Override API URL if provided
            self.URL = url                                                  #   ...
        else:                                                               # If not
            self.URL = self.API_URL                                         #   Use default API URL
            
        self.auth_client = CoinbaseAuthClient( key, secret )            # Start authenticated client
        # self.auth_session = self._start_session()                       # Start authenticated session
        
    def _start_session( self ) -> requests.Session:
        """
        Create a requests module session to improve performance by persisting
        cookies across all requests made within the session instance
        
        :return: Authenticated session
        """
        session = requests.session()
        session.auth = self.auth_client
        session.headers.update({'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'User-Agent': 'coinbase/python/2.0'})
        return session
        
    def _get( self, url_path: str ) -> requests.Response:
        """
        Perform a GET request.
        
        :return:
        """
        get = requests.get( self.URL + url_path, auth = self.auth_client )
        print( get.url )
        return get
    
    def get_price( self, currency_pair: str ) -> requests.Response:
        """
        https://api.coinbase.com/v2/prices/{currency_pair}/spot
        
        :param currency_pair: Pair such as "BTC-USD"
        :return:
        """
        return self._get( f'prices/{currency_pair}/spot' )              # Get currency pair price

    def get_fees( self ) -> requests.Response:
        """
        https://api.exchange.coinbase.com/fees

        :return:
        """
        get = requests.get( 'https://api.exchange.coinbase.com/fees', auth = self.auth_client )
        return get              # Get currency pair price
    
    
#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv     import  dotenv_values                               # Read key-value pairs from a .env file without modifying the environment
    from dotenv     import  find_dotenv                                 # Search for the .env within the main directory and subdirectories
    env_dir         = find_dotenv()                                     # Store absolute path to .env file
    cb_key          = dotenv_values( env_dir )['cb_key']                # Read key
    cb_secret       = dotenv_values( env_dir )['cb_secret']             # Read secret
    
    cb_client = CoinbaseClient( cb_key, cb_secret )                     # Start client
    # req = requests.get( cb_client.auth_client.API_URL + 'user', auth = cb_client.auth_client )    # Get current user
    # # print( r.json() )
    # print( orjson.loads( req.content ) )
    # r_currencies = requests.get( cb_client.auth_client.API_URL + 'currencies', auth = cb_client.auth_client )    # Get current user
    # print( r.json() )
    # print( orjson.loads( r_currencies.content ) )
    req = cb_client.get_price( 'BTC-USD' )
    req_fees = cb_client.get_fees()
#   ----------------- ___ END ___: Setup script and run -----------------
