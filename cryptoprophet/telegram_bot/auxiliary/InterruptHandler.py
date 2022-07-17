#@formatter:off
import  signal
import  readchar
from    typing              import Union

class GracefulInterruptHandlerContextManager( object ):
    interrupted : bool
    released    : bool

    def __init__( self, signals=(signal.SIGINT, signal.SIGTERM, signal.SIGHUP) ):
        self.signals = signals
        self.original_handlers = {}

    def __enter__( self ):
        self.interrupted = False
        self.released = False

        for sig in self.signals:
            self.original_handlers[sig] = signal.getsignal(sig)
            signal.signal( sig, self.handler )
        return self

    def handler( self, signum: Union[int, signal.Signals], frame ):
        msg = f'[?] Signal handler called with signal {signum}.'
        msg = f'{msg} Do you really want to exit? (y/n)'
        print( msg, end="\n", flush=True )
        response = readchar.readchar()
        
        if( response == 'y' ):
            print("")
            self.release()
            self.interrupted = True
            exit( 0 )
        else:
            print( ""               , end="\r"  , flush=True )
            print( " " * len(msg)   , end=""    , flush=True ) # clear the printed line
            print( "    "           , end="\r"  , flush=True )

    def __exit__( self, type, value, tb ):
        self.release()

    def release( self ):
        if ( self.released ):
            return False

        for sig in self.signals:
            signal.signal( sig, self.original_handlers[sig] )

        self.released = True
        return True


class GracefulInterruptHandler( object ):
    def __init__( self, signals=(signal.SIGINT, signal.SIGTERM, signal.SIGHUP) ):
        self.interrupted        = False
        self.released           = False
        
        self.signals            = signals
        self.original_handlers  = {}
        
        for sig in self.signals:
            self.original_handlers[sig] = signal.getsignal(sig)
            signal.signal( sig, self.handler )
    
    def handler( self, signum: Union[int, signal.Signals], frame ):
        msg = f'[?] Signal handler called with signal {signum}.'
        msg = f'{msg} Do you really want to exit? (y/n)'
        print( msg, end="\n", flush=True )
        response = readchar.readchar()
        
        if( response.lower() == 'y' ):
            self.interrupted = True
            print( "[INFO] Exiting gracefully" )
            self.release()
            print( "[INFO] Released" )
            exit(1)
        else:
            print( ""               , end="\r"  , flush=True )
            print( " " * len(msg)   , end=""    , flush=True ) # clear the printed line
            print( "    "           , end="\r"  , flush=True )

    def __exit__(self, type, value, tb):
        self.release()

    def release( self ):
        if( self.released ):
            return False
    
        for sig in self.signals:
            signal.signal( sig, self.original_handlers[sig] )
    
        self.released = True
        return True

#%% ----------------- ___START___: Setup script and run -----------------

if __name__ == '__main__':
    from time import sleep
    
    # # Test 1
    # with GracefulInterruptHandlerContextManager() as h:
    #     for i in range(1000):
    #         print( "..." )
    #         sleep(1)
    #         if h.interrupted:
    #             print( "interrupted!" )
    #             sleep(2)
    #             break
    
    # Test 2
    sig_handler = GracefulInterruptHandler()
    sleep( 10 )
#   ----------------- ___ END ___: Setup script and run -----------------