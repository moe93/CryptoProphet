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

import  asyncio                                                             # Asynchronous routines
import time
import  websockets                                                          # Connect to websocket server
import  orjson                                                              # Fast, efficient JSON parser

class Websocket( object ):
    
    API_URL         : str = 'wss://ws-feed.exchange.coinbase.com'
    
    def __init__( self ) -> None:
        self.init_run = True                                                # Initial run flag
        self.URL = self.API_URL                                             # Use default API URL
        
        
    async def connect( self, payload ) -> None:
        """
        Perform a GET request.
        
        :return:
        """
        async with websockets.connect( self.URL ) as ws:
            if( self.init_run ):
                await ws.send( payload )
                self.init_run = False
                await asyncio.sleep( 0.1 )
            else:
                pass
            
            while True:
                msg = await ws.recv()
                msg_decoded = orjson.loads( msg )
                print( msg_decoded )
                time.sleep( 1 )
    
    
#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':

    ws = Websocket()                                     # Start socket
    # req     =  { "type": "subscribe",
    #              "product_ids": [
    #                      "ETH-USD"],
    #              "channels": ["level2_batch"] }
    req     =  { "type": "subscribe",
                 "product_ids": [
                         "ETH-USD"],
                 "channels": ["ticker"] }
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future( ws.connect(orjson.dumps(req)) )
        loop.run_forever()
    except KeyboardInterrupt:
        print( "Interrupt detected" )
    finally:
        print( "Closing loop" )
        loop.close()
    

#   ----------------- ___ END ___: Setup script and run -----------------
