"""
Copyright (c)  2019 Shankar

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
#This is the __init__.py for libprime



from libprime.prime_number_check import nisprime
import time

#Wrapper for prime_number_check.nisprime
def isprime(n,iprime=True,timer=False):
	"""
	n is the number to be checked.
	iprime is the return value if n is prime.
	timer is used for calculating time elapsed for  running      	this function.
	"""
	#This function return iprime's value if n is prime
	#Otherwise it returns the smallest prime
     # factor of n.
    
     #type:n int
     #type:iprime anything
     #type:timer bool
    
    
    
	start_time=time.time()
	return_value=nisprime(n,ifprime=iprime)
	end_time=time.time()
	if timer:
		#if timer is set to True then,
		time_elapsed=start_time-end_time
		return (return_value,time_elapsed)
		#returns a tuple
		#containing the return_value(factor or 
		#iprime)
		#time elapsed,the time taken to run this.
	else:
		#default returns only return_value or 
		#iprime if n is found to be prime
		return return_value	
	
__version__='0.0.1b2'
__author__='shankar'	
