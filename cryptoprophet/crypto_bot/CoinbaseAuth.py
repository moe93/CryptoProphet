#@formatter:off
"""
Create a Coinbase Pro client here

VERSION: 0.0.1
    - ADDED     : Pre-planning stage

KNOWN ISSUES:
    - Non encountered


AUTHOR                      :   Mohammad Odeh
DATE                        :   Aug.  7th, 2022 Year of Our Lord
LAST CONTRIBUTION DATE      :   Aug.  7th, 2022 Year of Our Lord
"""

from    typing                      import  Dict, Optional, Union           # Additional type hints
from    re                          import  compile                         # Use regex for validation
from    time                        import  time                            # Get time
from    requests.auth               import  AuthBase                        # Base class that all auth implementations derive from
import  pandas                      as      pd                              # Data manipulation
import  requests                                                            # HTTP GET and POST for API interaction
import  hmac                                                                # Keyed-Hashing for Message Authentication
import  hashlib                                                             # Secure hash and message digest algorithms
import  orjson                                                              # Fast, efficient JSON parser
import  json
import  base64

class CoinbaseAuthClient( AuthBase ):

    # Add type hints
    _CB_KEY         : str   = None
    _CB_SECRET      : str   = None
    _CB_PASSPHRASE  : str   = None
    # _URL            : str   = None
    VALID_METHODS   : [str] = [ 'GET', 'POST', 'DELETE' ]
    VALID_KWARGS    : [str] = [ 'pro', 'api_passphrase' ]
    API_URL         : Dict[str, str] = { 'v2' : 'https://api.coinbase.com/v2/',
                                         'pro': 'https://api.pro.coinbase.com/' }
    
    def __init__( self, api_key: str, api_secret: str, **kwargs: Optional[Union[bool, str]] ):
        """
        Coinbase authenticated client.
        
        :param api_key: Coinbase API key.
        :param api_secret: Coinbase API key.
        :keyword pro: Use Coinbase Pro instead of Coinbase (default: False).
        :keyword api_passphrase: Coinbase Pro API passphrase.
        """
        self.url = self.API_URL[ 'v2' ]                                     # Set new API (v2) as default
        self.pro = False                                                    # Use Coinbase.com as default
        
        if (api_key or api_secret) is None:                                 # Check that API key/secret are given
            raise ValueError( 'No API Key/Secret is provided' )             #   If not, raise error
        else:                                                               # Else, move on
            self.unpack_kwargs( **kwargs )                                  #   Unpack **kwargs
            self.validate_api( api_key, api_secret, self._CB_PASSPHRASE )   #   Validate API entries
    
    def __call__( self, request ):
        
        if( self.pro ):
            timestamp = str(time())
            body = (request.body or b"").decode()
            message = f"{timestamp}{request.method}{request.path_url}{body}"
            hmac_key = base64.b64decode(self._CB_SECRET)
            signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
            signature_b64 = base64.b64encode(signature.digest()).decode()
            
            header = { 'CB-ACCESS-SIGN'      : signature_b64 ,
                       'CB-ACCESS-TIMESTAMP' : timestamp     ,
                       'CB-ACCESS-KEY'       : self._CB_KEY  ,
                       "CB-ACCESS-PASSPHRASE": self._CB_PASSPHRASE,
                       'Content-Type'        : 'application/json'}
            
        else:
            timestamp   = str( int(time()) )                                    # Get current time as string
            message     = timestamp + request.method + request.path_url + (request.body or '')
            b_message   = message.encode( 'UTF-8' )                             # Encode message as bytes
            b_secret    = (self._CB_SECRET).encode( 'UTF-8' )                   # Encode secret as bytes
            signature   = hmac.new( b_secret, b_message, hashlib.sha256 ).hexdigest()
            
            header = { 'CB-ACCESS-SIGN'      : signature     ,
                       'CB-ACCESS-TIMESTAMP' : timestamp     ,
                       'CB-ACCESS-KEY'       : self._CB_KEY  ,
                       'Content-Type'        : 'application/json'}
            
        request.headers.update( header )
        
        return request
    
    def unpack_kwargs( self, **kwargs ) -> None:
        """
        Unpack keyword arguments if they exist
        :param kwargs:
        :return:
        """
        for key, value in kwargs.items():                                   # Check if we have any keyword arguments passed
            if key.lower() not in self.VALID_KWARGS:                        #   If keyword not within the valid kwargs list
                pass                                                        #       pass
            else:                                                           #   Otherwise, keyword is within valid list
                # Case 1: kwarg=='pro'
                if key.lower() == self.VALID_KWARGS[ 0 ]:                   #       kwarg == 'pro'
                    if isinstance( value, bool ) and value is True:         #           Check if bool AND True
                        self.url = self.API_URL['pro']                      #               Use CBPro API
                        self.pro = True                                     #               Set flag
                        print( f'Using CBPro API. URL: {self.url}' )        #               [INFO] ...
                # Case 2: kwarg=='api_passphrase'
                if key.lower() == self.VALID_KWARGS[ 1 ]:                   #       kwarg == 'api_passphrase'
                    if isinstance( value, str ):                            #           Check if str
                        self._CB_PASSPHRASE = value                         #               Store API Passphrase
                        
    def validate_api( self, key: str, secret: str, passphrase: str ):
        """
        Validate Coinbase API information.

        Note on RegEx:
            The leading ^ and the trailing $ are known as position anchors, which match the start
            and end positions of the line, respectively. As the result, the entire input string
            shall be matched fully, instead of a portion of the input string (substring).

            - {m}   : The preceding item is matched exactly m times.
            - {m,n} : The preceding item is matched at least m times, but not more than n times.
            - \\\   : Backslash is an escape character (i.e. \\\[ matches "[").
            - \\+   : Plus sign indicates one or more occurrences of the preceding element.
            For example, ab+c matches "abc", "abbc", "abbbc", and so on, but not "ac".

        :param key:         Coinbase API key
        :param secret:      Coinbase API secret
        :param passphrase:  Coinbase API passphrase
        """
        # If CBPro is being used
        if self.pro is True:
            pattern = { 'key'       : compile( r'^[a-f0-9]{32}$'   ),
                        'secret'    : compile( r'^[A-z0-9+\/]+==$' ),
                        'passphrase': compile( r'^[A-z0-9#$%=@!{},`~&*()<>?.:;_|^/+\[\]]{8,32}$' ) }

            # Validate API passphrase
            try:                                                            # Check if passphrase was provided
                if not pattern['passphrase'].match( passphrase ):           #   If NOT valid
                    raise ValueError( "Coinbase API secret is invalid" )    #       Raise error
                else:                                                       #   Else, if it is correct
                    self._CB_PASSPHRASE = passphrase                        #       Store API passphrase
            except TypeError as e:                                          # Catch error
                raise ValueError( "Coinbase API passphrase not provided" )  #   Raise ValueError
            
        # If CB (v2) is being used
        else:
            pattern = { 'key'       : compile( r'^[A-z0-9]{16}$' ),
                        'secret'    : compile( r'^[A-z0-9]{32}$' ) }
        
        # Validate API key
        if not pattern['key'].match( key ):                                 # If NOT valid
            raise ValueError( "Coinbase API key is invalid" )               #   Raise error
        else:                                                               # Else, if it is correct
            self._CB_KEY = key                                              #   Store API key
        
        # Validate API secret
        if not pattern['secret'].match( secret ):                           # If NOT valid
            raise ValueError( "Coinbase API secret is invalid" )            #   Raise error
        else:                                                               # Else, if it is correct
            self._CB_SECRET = secret                                        #   Store API secret
            
    def api_call( self, method: str, uri: str, payload: str = "" ) -> pd.DataFrame:
        """
        
        :param method:
        :param uri:
        :param payload:
        :return:
        """
        method = method.upper()                                             # Convert input to uppercase
        
        if method not in self.VALID_METHODS:                                # Check if method is valid
            raise TypeError( f'"{method}" is not a valid method' )          #   If not, raise error
        if isinstance( uri, str ) is not True:                              # Check if uri is string
            raise TypeError( f'"{uri}" is not a string' )                   #   If not, raise error
        
        try:                                                                # Catch connection error
            if   method == self.VALID_METHODS[ 0 ]:                         #   method == "GET"
                resp = requests.get( self.url + uri,                        #   ...
                                     auth = self )                          #   ...
                print( orjson.loads( resp.content ) )
            elif method == self.VALID_METHODS[ 1 ]:                         #   method =="POST"
                resp = requests.post( self.url + uri,                       #   ...
                                      json = payload,                       #   ...
                                      auth = self )                         #   ...
            elif method == self.VALID_METHODS[ 2 ]:                         #   method == "DELETE"
                resp = requests.delete( self.url + uri,                     #   ...
                                        auth = self )                       #   ...
            else:
                resp = None
                
            resp.raise_for_status()

            if resp.status_code == 200:
                if isinstance(resp.json(), list):
                    df = pd.DataFrame.from_dict(resp.json())
                    return df
                else:
                    df = pd.DataFrame(resp.json(), index=[0])
                    return df
            else:
                if "msg" in resp.json():
                    resp_message = resp.json()["msg"]
                elif "message" in resp.json():
                    resp_message = resp.json()["message"]
                else:
                    resp_message = ""
    
                if resp.status_code == 401 and (
                        resp_message == "request timestamp expired"
                ):
                    msg = f"{method} ({resp.status_code}) {self.url}{uri} - {resp_message} (hint: check your system time is using NTP)"
                else:
                    msg = f"CoinbasePro authAPI Error: {method.upper()} ({resp.status_code}) {self.url}{uri} - {resp_message}"
        
        except requests.ConnectionError as err:
            reason, msg = ("ConnectionError", err)
            print( reason, msg )

        except requests.exceptions.HTTPError as err:
            reason, msg = ("HTTPError", err)
            print( reason, msg )
            
        except requests.Timeout as err:
            reason, msg = ("TimeoutError", err)
            print( reason, msg )
            
        except json.decoder.JSONDecodeError as err:
            reason, msg = ("JSONDecodeError", err)
            print( reason, msg )
            
        except Exception as err:
            reason, msg = ("GeneralException", err)
            print( reason, msg )
            
#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from dotenv     import  dotenv_values                               # Read key-value pairs from a .env file without modifying the environment
    from dotenv     import  find_dotenv                                 # Search for the .env within the main directory and subdirectories
    env_dir         = find_dotenv('v2.env')                             # Store absolute path to .env file
    cb_key          = dotenv_values( env_dir )['cb_key']                # Read key
    cb_secret       = dotenv_values( env_dir )['cb_secret']             # Read secret
    cb_passphrase   = dotenv_values( env_dir )['cb_passphrase']         # Read passphrase

    # API_URL   : str = 'https://api.pro.coinbase.com/'
    API_URL   : str = 'https://api.coinbase.com/v2/'
    cb_client = CoinbaseAuthClient( cb_key, cb_secret,
                                    pro=False,
                                    api_passphrase=cb_passphrase )      # Start client
    r = requests.get( API_URL + 'user', auth = cb_client )              # Get current user
    print( orjson.loads( r.content ) )
    
    market = 'BTC-USD'
    acc = cb_client.api_call( 'GET', 'accounts' )
    tic = cb_client.api_call( 'GET', f'products/{market}/ticker' )
    # print( orjson.loads( req.content ) )

#   ----------------- ___ END ___: Setup script and run -----------------
