"""NBSR: Non-blocking Stream Reader"""


#from __future__ import print_function
import sys
import threading
import Queue as queue
import re


class NonStreamException(Exception):
    """The stream is to be a stream-type object"""
    pass

class ClosedStreamException (Exception):
    """Raised when the proveded stream is not open"""
    pass
    
class TimoutNotNumber(Exception):
    """The timeout is to be a number or None"""
    pass
    
class AtomicTimoutNotNumber(Exception):
    """The atomic timeout is to be a number"""
    pass
    
class TimeOutOccured(Exception):
    """No (enough) data could be read from the stream"""
    pass
    
class StreamUnexpectedlyClosed(Exception):
    """The stream got closed while we were reading it"""
    pass


returnby_EOF = 0
returnby_NEWLINE = 11
returnby_SIZE = 12
returnby_PATTERN = 20
returnby_TIMEOUT = 100


class NonBlockingStreamReader(object):
    """Class to define a stream reader that can have timeout and does not block
    
    The standard I/O actions are blocking. E.g. readline() does not return until it reads
    a newline character or reaches EOF. Or, a read(4096) won't return until all 4KB is
    read or EOF reached. If the process feeding the stream gets stuck (e.g. waiting for
    an answer/password), i.e. it does not produce enough data and do not terminate
    either, the regular I/O read will hang.
    
    NBSR class provides the timeout feature, so that hanging of I/O actions can be
    overcome. Actually, 2 kinds of timeout can be defined. The so called atomic timeout
    is how much we wait for a single character to be read. If this timeout happens the
    bunch of the read characters is matched to a list of patterns. I.e. we may be
    waiting for a prompt or a '-- more --' line. If any of the patterns is matched, the
    read function returns with the read characters and the index of the matched
    pattern can be retrieved (and can be handled by the caller).
    
    If atomic timeout happened and none of the patterns matched, further read is
    attempted as long as the normal timeout. Typically atomic timeout is a fraction of a
    second and a normal timeout is several seconds.
    
    Read functions only return the characters read. Additional info, i.e. what pattern
    matched (if any) has to be retrieved by the caller separately. See extra methods
    below.
    
    NBSR uses a queue, which is fed by a thread using the standard I/O read. If the
    standard I/O read gets blocked, the queue runs empty. The main process can get
    the data which has been put so far into the queue and return it to the caller.
    
    Any sub-sequent calls of NBSR read (supposing that the stream producer is still stuck)
    result in returning exception or empty string (see the given method for details).
    
    It is the caller's responsibility to feed response to the stream producer or terminate
    it, so that stream reader worker thread unblocks and/or terminates.
    
    NBSR provides the following read methods, which provide the same function as their
    similarly named standard I/O functions, but of course with the timeout feature. They
    return the data read from the stream and they always return at the latest when there
    is timeout:
    
    - read()
    - readline()
    - readlines()
    
    NBSR provides the following extra methods:
    
    - set_timeout() is to set/change the timeout values for subsequent reads
    - found_pattern_info() is to retrieve the info of the pattern if it was matched
    - is_sending() is to test whether the stream is sending data yet, i.e. any data can
        be read from the stream (but actually nothing consumed yet). This can be used in
        the begining of reading the stream as the wait time (timeout) can be a lot longer
        than the timeout between subsequent reads.
    - return_reason() provides the reason why the last read function returned
    - do_pattern_check() is to force a pattern check in case the return reason was some
        higher priority reason, like EOF
    - is_EOF() can be used to check whether EOF has reached. As the read functions simply
        return empty string if we call them after EOF is reached, checking EOF could be
        useful. 
    
    Args:
        stream (stream): an open stream where we read data from.
            This is usually a STDOUT (or STDERR) of a piped process.
        timeout (optional float or None): the read timeout in seconds. By default it is None,
            meaning return is immediate, even if there is no data on the stream
        atomic_timeout (optional float): the timeout for reading a byte from the stream.
            By default it is 1/100 s.
        debugprint (optional bool): only for development
    
    Attributes:
        timeout (float): the timeout in seconds or fraction of seconds that we wait
            until the read function returns, in case the required amount of data or
            the required type of data has not been received yet
        atomic_timeout (float): the timeout for reading 1 byte from the stream
        timeout_diff (float): = the difference how much the timeout is longer than the
            atomic_timeout
        pattern_index (int): the index of the found pattern. If no pattern was found,
            it is None.
        match_object (re.MatchObject): the match object returned by the re search
        blockneeded (bool): indicates whether the queue get function is to be blocking
        linequeue (Queue.Queue): the queue where we put the read data
        bufferedchars (list): a buffer which is filled during is_sending() and emptied
            by the _readone()
        returnby (int): enum value indicating the reason of the last read function
            return, i.e. EOF, SIZE, NEWLINE, PATTERN, TIMEOUT. Such constants can
            be used as NBSR.returnby_EOF, NBSR.returnby_SIZE, etc.
        EOF (bool): flag indicating whether the stream reached EOF and the worker
            thread already finished/returned, i.e. nothing more can be read from the
            stream
    
    Raises:
        NonStreamException: the provided object in 'stream' is not of a stream type
        ClosedStreamException: the provided stream must be open, but closed
        TimoutNotNumber: the provided timeout is not a number or None
        AtomicTimoutNotNumber: the provided atomic timeout is not a number
        TimeOutOccured: the requested amount of data could not be read in time
        StreamUnexpectedlyClosed: the stream got closed while we were reading it
        ValueError: if timout agruments do not make sense
    """
    def __init__(self, stream, timeout=None, atomic_timeout=0.01, debugprint=False):
        #check whether a stream-type object is arrived in 'stream'
        if not isinstance(stream, file):
            raise NonStreamException
        
        #check the stream as it has to be open
        if stream.closed:
            raise ClosedStreamException
        
        #check whether the timeout is a of the correct type
        if not isinstance(timeout, (float, int, type(None))):
            raise TimoutNotNumber
        
        if not isinstance(atomic_timeout, (int, float)):
            raise AtomicTimoutNotNumber
        
        #store the timeouts
        self.set_timeout(timeout, atomic_timeout)
        
        #if there is a given timeout, set the queue get function so that it is blocking
        self.blockneeded = timeout is not None
        
        #store the flag whether debug printing is needed
        self.debugprint = debugprint
        
        #set the EOF flag to false by default
        self.EOF = False
        
        #indicate that no any pattern matched yet
        self.pattern_index = None
        self.match_object = None
        
        #indicate that no any return reason is available yet
        self.returnby = -1
        
        #create the buffer for is_sending()
        self.bufferedchars = []
        
        #instantiate a Queue class and store it
        self.linequeue = queue.Queue()
        
        #Create a worker thread instance
        self.workerthread = threading.Thread(
                                                            target=self._populate_queue,
                                                            args=(stream, )
                                                        )
        
        #start the worker thread as a non-daemon
        self.workerthread.daemon = False
        self.workerthread.start()
    
    
    def _populate_queue(self, stream):
        '''Collect data from 'stream' and put them in the 'queue'
        
        Worker function to be run as a child thread. It only reads 1 character at a time
        and put it into the queue. Where there is no more character to read, but there
        is no EOF yet (i.e. the stream source is stuck), this thread hangs.
        Reading only 1 character makes sure all data is read from the stream before
        it hangs. 
        
        Child thread cannot and must not raise exception, so if such is needed the 
        exception class is put into the queue, and the queue consumer is responsible
        to notice this and raise the exception of that class.
        
        Writing the self.EOF is safe as this is the only place it is written, the parent
        only reads it.
        
        Args:
            stream (stream): the stream where we read from. We have already
        '''        
        #loop on reading lines
        while True:
            try:
                #read 1 byte and block until this byte can be read or stream gets closed
                charread = stream.read(1)
            except ValueError:
                if stream.closed:
                    self.linequeue.put(StreamUnexpectedlyClosed)
            
            #put the character (or empty string, if EOF) into the queue
            self.linequeue.put(charread)
                
            #standard I/O read returns empty string on EOF
            if charread == '':
                #set the EOF flag
                self.EOF = True
                
                #finish the worker on EOF
                return
    
    
    def _readone(self, timeout=None):
        """Private function to read one character from the stream
        
        It is the consumer of the queue.
        If there is stream data in the queue, this functon returns it immediately.
        It returns empty string in case of EOF (same behaviour as regular read).
        If the queue is empty and no data can be read within the given timeout,
        the stream is stuck, so it raises TimeOutOccured. The timeout can be explicitly
        provided in the argument or taken from the instance attribute. 
        
        Args:
            timeout (optional float): the timeout the reading max wait if the queue
                is empty. If missing or None, the atomic_timeout set earlier (in init or
                set_timeout) is used.
        
        Returns:
            str: the read character, or empty string on timeout or EOF
        
        Raises:
            TimeOutOccured
            StreamUnexpectedlyClosed
        """
        #first try to get the character from the buffer
        try:
            return self.bufferedchars.pop(0)
        except IndexError:
            pass
            
        try:
            #get an element from the queue. Use the explicit timeout if exists.
            queueelement = self.linequeue.get(
                                                            block=self.blockneeded,
                                                            timeout=timeout or self.atomic_timeout
                                                        )
        
        #Empty exception means that there was a timeout
        except queue.Empty:
            #raise exception
            raise TimeOutOccured
            
        else:
            #if str was taken from the queue, just return it
            if isinstance(queueelement, str):
                if self.debugprint:
#                   print(queueelement, end='', flush=True) #flush was not back-ported to 2.7
                    sys.stdout.write(queueelement)
                    sys.stdout.flush()
                return queueelement
            
            #if there was an error in the worker thread, it did put an Exception class into the queue
            else:
                raise queueelement
        
    
    def _compile_patterns(self, expected_patterns, patterns_compiled, regexflags):
        """Private function to compile re patterns
        
        It checks whether the patters in the list need to be compiled and if so,
        compile them and store them in an instance attribute.
        
        Args are the same as for read functions
        """
        #store the received timeout
        if not isinstance(expected_patterns, (list, tuple)):
            raise ValueError('expected_patterns should be either a list or tuple, but it is ' + str(type(expected_patterns)))
        
        #compile patterns if needed
        if patterns_compiled:
            self.compiled_patterns = expected_patterns
        else:
            self.compiled_patterns = []
            for expected_pattern in expected_patterns:
                self.compiled_patterns.append(
                                                            re.compile(
                                                                            expected_pattern,
                                                                            regexflags
                                                                        )
                                                        )
    
    
    def _readbunch(self, size=None):
        """Private function to read a bunch of data from the stream defined at
        instance creation
        
        Tries to read as many data as possible. I.e. up to EOF, end condition,
        or (on timeout) a matched pattern. It then returns whatever it could read.
        
        If reading ends for more than one reason (i.e. pattern would match but
        there is EOF too), the precedence for returned reason is EOF first, then
        end conditions and then pattern match. I.e. patterns are only checked
        if there was some timeout and there is no other reason for finishing
        reading.
        However, if pattern check is still needed, do_pattern_check() can be used.
        
        If the return reason is that a pattern has matched, the instance attributes
        pattern_index and match_object are set (otherwise they are None).
        
        Args:
            size (int): the amount of data (number of characters) to be read if
                it is a read, or None for a readline
        
        Returns:
            str: the read data if any, or empty string
        
        Raises:
            StreamUnexpectedlyClosed
        """
        #we are going to collect characters in the buffer
        buffer = ''
        
        #indicate that no any pattern matched yet
        self.pattern_index = None
        self.match_object = None
        
        #the next timeout, whether atomic_timeout is to be used or long wait
        this_timeout = None
        
        #create a counter if it is a read
        if size is not None:
            cnt = 0
        
        #loop on reading characters until an end condition or EOF is found, or timeout
        while True:
            try:
                #read 1 character with atomic_timeout for 1st read, or timeout after that
                ch = self._readone(this_timeout)
            
            except TimeOutOccured:
                #this_timeout=None indicate that this was an atomic timeout
                if this_timeout is None:
                    #progress to pattern search
                    pass
                else:
                    #if long timeout occured, return the content of the buffer (can be empty)
                    self.returnby = returnby_TIMEOUT
                    return buffer
            
            except StreamUnexpectedlyClosed:
                #if the stream became closed, let the exception escalate
                raise
            
            #successful read
            else:
                #the previous read might have had atomic timeout, so reset it now after a successful read
                this_timeout = None
                
                #add the character (or nothing in case of EOF) to the buffer
                buffer += ch
                
                #check whether EOF occured
                if ch =='':
                    #return the buffer at EOF
                    self.returnby = returnby_EOF 
                    return buffer
                
                if size is None:
                    if ch == '\n':
                        #if it is at the end of a line, return the line or whatever was read
                        self.returnby = returnby_NEWLINE
                        return buffer
                else:
                    if cnt >= size:
                        #we have read enough, return the buffer
                        self.returnby = returnby_SIZE
                        return buffer
                    else:
                        cnt += 1
                        
                #read on
                continue
                
            #as atomic timeout happened, check patterns whether any of them matches
            if self.do_pattern_check(buffer):
                #set the return reason and return the buffer
                self.returnby = returnby_PATTERN
                return buffer
            
            #set a longer timeout for the next read and continue reading attempt
            this_timeout = self.timeout_diff
            continue
    
    
    ##########################################################
    ## Public methods
    ##########################################################
    
    def read(self, size, expected_patterns=[], patterns_compiled=False, regexflags=0):
        """Read as many as size characters from the stream defined at instance creation
        
        This function never blocks. 
        
        If the required amount of characters can be read within the timeout, it behaves as
        a regular read(). If some data is read but not enough until the timeout, the so-far
        read data is returned. If there are no more data and the stream is stuck or
        EOF, it returns empty string (exactly as regular read would do on EOF).
        
        Args:
            size (int): the amount of data (number of characters) to be read
            expected_patterns (optional tuple/list): a list of patterns that we wait for.
                If any of these patterns match, we return immediately, not waiting
                for EOF or timeout.
            patterns_compiled (optional bool): flag to indicate whether the patterns
                received are already compiled. By default it is False, stating that the
                patterns are pure strings
            regexflags (optional int): see the re module, e.g. re.IGNORECASE. Or
                re.VERBOSE meaning white space is not part of the pattern (unless
                escaped) and comments can appear. Note that if patterns_compiled
                is True, these flags here are ignored.
                
        Returns:
            str: the read data, as many as size or whatever could be read before timeout
        
        Raises:
            StreamUnexpectedlyClosed
        """
        #compile the patterns
        self._compile_patterns(expected_patterns, patterns_compiled, regexflags)
        
        #read a bunch of data
        return self._readbunch(size=size)
    
    
    def readline(self, expected_patterns=[], patterns_compiled=False, regexflags=0):
        """Read one line (or part of it) from the stream defined at instance creation
        
        This function never blocks. 
        
        If the line can be read within the timeout, it behaves as a regular readline().
        If some data is read but no newline arrives until the timeout, the so-far
        read data is returned. If there are no more data and the stream is stuck or
        EOF, it returns empty string (exactly as regular readline would do on EOF).
        
        Args:
            expected_patterns (optional tuple/list): a list of patterns that we wait for.
                If any of these patterns match, we return immediately, not waiting
                for EOF or timeout.
            patterns_compiled (optional bool): flag to indicate whether the patterns
                received are already compiled. By default it is False, stating that the
                patterns are pure strings
            regexflags (optional int): see the re module, e.g. re.IGNORECASE. Or
                re.VERBOSE meaning white space is not part of the pattern (unless
                escaped) and comments can appear. Note that if patterns_compiled
                is True, these flags here are ignored.
        
        Returns:
            str: a full line, part of a line or just empty string, i.e. whatever could be
                read before timeout
        
        Raises:
            StreamUnexpectedlyClosed
        """
        #compile the patterns
        self._compile_patterns(expected_patterns, patterns_compiled, regexflags)
        
        #read a bunch of data
        return self._readbunch(size=None)
    
    
    def readlines(self, expected_patterns=[], patterns_compiled=False, regexflags=0):
        """Read all lines from the stream defined at instance creation
        
        This function never blocks. See the details under readline()
        
        Args:
            expected_patterns (optional tuple/list): a list of patterns that we wait for.
                If any of these patterns match, we return immediately, not waiting
                for EOF or timeout.
            patterns_compiled (optional bool): flag to indicate whether the patterns
                received are already compiled. By default it is False, stating that the
                patterns are pure strings
            regexflags (optional int): see the re module, e.g. re.IGNORECASE. Or
                re.VERBOSE meaning white space is not part of the pattern (unless
                escaped) and comments can appear. Note that if patterns_compiled
                is True, these flags here are ignored.
                
        
        Returns:
            list: the list of the lines read, each string terminated by newline.
                The last line can be a part of a line, i.e. missing the newline at the end.
                On EOF, an empty list is returned.
        
        Raises:
            StreamUnexpectedlyClosed
        """
        #we are going to collect lines in a list
        lines = []
        
        #compile the patterns
        self._compile_patterns(expected_patterns, patterns_compiled, regexflags)
        
        #imitate as if the last read returned newline for the first while loop condition check
        self.returnby = returnby_NEWLINE
        
        #loop on reading lines as long as the previous read returned with newline
        while self.returnby == returnby_NEWLINE:
            #read 1 line string
            line = self.readline(self.compiled_patterns, True)
            
            #add the line to the list. NB, lines+=line would add each char in the line as a separate list element
            lines.append(line)
            
        #return all the lines whatever was read
        return lines
    
    
    def set_timeout(self, timeout, atomic_timeout=None):
        """Set the timeout for the sebsequent read actions
        
        Args:
            timeout (float, int or None): the timeout the reading max wait if the queue is empty
            atomic_timeout (optional float, int or None): the timeout for reading 1 byte from the stream.
                If not given (or set to None) the atomic_timeout provided in init is not changed.
        
        Raises:
            ValueError if timout agruments do not make sense
        """
        #store the received timeout
        if not isinstance(timeout, (float, int, type(None))):
            raise ValueError('timeout should be a float, int or None, but it is ' + str(type(timeout)))
        if timeout <= 0:
            raise ValueError('timeout (' + str(timeout) + ') should be a positive value')
        self.timeout = timeout
        
        #store the received atomic_timeout, but if it is None, do not change the already stored one
        if atomic_timeout is not None:
            if not isinstance(atomic_timeout, (float, int)):
                raise ValueError('atomic_timeout should be either a float or int, but it is ' + str(type(atomic_timeout)))
            if atomic_timeout <= 0:
                raise ValueError('atomic_timeout (' + str(atomic_timeout) + ') should be a positive value')
            self.atomic_timeout = atomic_timeout
        
        #check that values make sense
        if self.atomic_timeout > self.timeout:
            raise ValueError('atomic_timeout (' + str(self.atomic_timeout) + ') should not be bigger than timeout (' + str(self.timeout) + ')')
        
        #calculate the difference and store it as an integer
        if self.timeout is not None:
            self.timeout_diff = self.timeout - self.atomic_timeout
        else:
            self.timeout_diff = 0
    
    
    def found_pattern_info(self):
        """Get the info of the found pattern
        
        Returns:
            tuple: the index of the found pattern and its match object
                int: the integer index of the found pattern. If no pattern was found, it is None
                re.MatchObject: the match object containing captured sections in the pattern
        """
        return self.pattern_index, self.match_object
    
    
    def is_sending(self, firsttimeout):
        """Test the stream by reading 1 character, but not consuming it
        
        If read is successful within the timeout, it indicates that the stream is sending data.
        The read character is buffered and will be returned in the next read (along with
        other read characters).
        
        Args:
            firsttimeout (float): the timeout the reading max wait if the queue is empty
                This timeout value is only temporary for this test and does not affect the
                timeout set in the init or set_timeout().
        
        Returns:
            bool: whether a character can be read from the stream
        
        Raises:
            StreamUnexpectedlyClosed
        """
        #try to read a character from the stream (or buffer)
        try:
            char = self._readone(firsttimeout)
            
        except TimeOutOccured:
            #indicate that the stream is not sending data (yet or stuck or EOF)
            return False
        except StreamUnexpectedlyClosed:
            #if the stream became closed, let the exception escalate
            raise
        
        #store the read character in the buffer (LIFO)
        self.bufferedchars.append(char)
        
        #indicate that the stream is sending data
        return True
    
    
    def return_reason(self):
        """Provide the reason why the last read function returned
        
        Returns:
            int: one of the returnby_xxxxx constants. Negative value means undefined.
        """
        return self.returnby
    
    
    def do_pattern_check(self, input):
        """Do pattern check on the input with the set of last used patterns
        
        If stream reading finishes on EOF or exception, pattern match is not checked,
        but in some cases the caller might want to know whether any pattern matched.
        So, the caller can force this pattern check even after EOF or exception. The
        result of the pattern check is stored in attributes as normal. If this method
        returns True, the caller needs to fetch the matched pattern index and the
        match object with found_pattern_info()
        
        Args:
            input (str): the string that needs to be checked against the patterns
        
        Returns:
            bool: whether any pattern in the list matched the input
        """
        #loop on expected patterns whether any of them matches
        for idx, compiled_pattern in enumerate(self.compiled_patterns):
            matchObj = compiled_pattern.match(input)
            if matchObj is not None:
                #set the pattern order number so that it can be read by the caller
                self.pattern_index = idx
                #save the match object so that the caller can get it
                self.match_object = matchObj
                #indicate match to the caller
                return True
        
        #if the loop exhausted, indicate no match
        self.pattern_index = None
        return False
    
    
    def is_EOF(self):
        """Test whether EOF has reached
        
        Returns:
            bool: flag whether EOF has reached
        
        Note:
            This function purely indicates whether we reached EOF with reading the stream
            with NBSR read functions. So, if we did not read until EOF, or read the stream
            to EOF with other functions than this NBSR instance, or even if the stream
            got closed, this function still returns False, as if the stream could still be read.
            
            Also, this EOF check works without exception even after the stream
            has been closed.
        """
        return self.EOF
