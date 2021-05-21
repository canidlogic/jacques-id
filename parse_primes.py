#
# parse_primes.py
# ===============
#
# Parse the list of the first 1000 prime numbers from the PrimePages at:
#
#   https://primes.utm.edu/
#
# The parse() function takes the file path to a UTF-8 text file that is
# the data file of the first 1000 prime numbers.  It returns a list of
# integers read in from the file if successful, or throws an exception
# if there was a problem.
#
# Content lines in the data file contain nothing other than a sequence
# of one or more decimal integers separated by whitespace, and with
# optional leading and trailing whitespace.  All other kinds of lines
# are ignored.
#
# There do not necessarily need to be exactly 1000 prime numbers in the
# file.  However, the numbers that are listed must all be greater than
# one, and each successive number must be greater than the previous.
#

import os.path

#
# Exception classes
# -----------------
#
# Each exception overloads the __str__ operator so that it can be
# printed as a user-friendly error message.  It has punctuation at the
# end, but it does NOT have a line break at the end.
#
# All exceptions defined by this module are subclasses of PrimeError.
#

class PrimeError(Exception):
  def __str__(self):
    return 'Unknown error!'

class LogicError(PrimeError):
  def __str__(self):
    return 'Internal logic error!'

class NotFoundError(PrimeError):
  def __str__(self):
    return 'Data file not found!'

class OpenError(PrimeError):
  def __str__(self):
    return 'Can\'t open data file!'

class OrderError(PrimeError):
  def __str__(self):
    return 'Primes are not in ascending, non-duplicate order!'

#
# Public functions
# ----------------
#

# Parse the data file of prime numbers.
#
# The data file format is described at the top of this script.
# Exceptions are thrown in case of any problems.
#
# An empty list may be returned if no content lines were encountered.
#
# Parameters:
#
#   fpath : str - the file path to the data file of prime numbers
#
# Return:
#
#   a list of integers, representing all the numbers that were
#   encountered in the file, in ascending order
#
def parse(fpath):
  
  # Check parameter type
  if not isinstance(fpath, str):
    raise LogicError()
  
  # Check that path is to an existing regular file
  if not os.path.isfile(fpath):
    raise NotFoundError()
  
  # Open the data file for reading in UTF-8
  result = []
  try:
    with open(fpath, 'rt', encoding='utf-8') as f:
    
      # Read and process each line of the file
      first_line = True
      for s in f:
        
        # If this is first line, clear first line flag and perform BOM
        # handling
        if first_line:
          # Clear first line flag
          first_line = False
          
          # Only proceed with BOM processing if at least one character
          if len(s) > 0:
            
            # Strip BOM if present at start of line
            if ord(s[0]) == 0xfeff:
              
              # Strip the BOM
              if len(s) > 1:
                s = s[1:]
              else:
                s = ''
          
        # Find all whitespace-separated tokens in the line
        tkb = s.split()
        
        # If no tokens, skip this line
        if len(tkb) < 1:
          continue
        
        # If any token is not an ASCII decimal integer, skip this line
        skip_it = False
        for t in tkb:
          # Check that each character in token is ASCII
          for c in t:
            if ord(c) > 0x7f:
              skip_it = True
              break
          
          # Check that token is decimal integer
          if not t.isdecimal():
            skip_it = True
          
          # Leave loop if we need to skip line
          if skip_it:
            break
        
        # Skip lines that do not have all ASCII decimal tokens
        if skip_it:
          continue
        
        # Add all tokens to the result, checking that each is greater
        # than the last one added
        for t in tkb:
          
          # Parse current integer
          ival = int(t)
          
          # If result is not empty, check ordering
          if len(result) > 0:
            if result[-1] >= ival:
              raise OrderError()
        
          # Add the new integer to the result
          result.append(ival)
        
  except PrimeError as pe:
    raise pe
  
  except Exception as e:
    raise PrimeError from e

  # If we got here, return result
  return result
