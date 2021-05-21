#
# prime_table.py
# ==============
#
# Parse a data file of primes using the parse_primes module and then
# generate either an HTML table listing of primes that are greater than
# 2 and less than 2048, or a Python array literal of the same.
#
# Syntax:
#
#   python3 prime_table.py html [data]
#   python3 prime_table.py py [data]
#
# [data] is the file path to the prime data file that will be parsed
# with the parse_primes module.
#
# The html invocation generates the HTML table while the py invocation
# generates the Python literal.
#

import parse_primes

import io
import sys

#
# Program entrypoint
# ------------------
#

# Check parameters
#
if len(sys.argv) != 3:
  print('Wrong number of arguments!')
  sys.exit(1)

if (sys.argv[1] != 'html') and (sys.argv[1] != 'py'):
  print('Unrecognized mode!')
  sys.exit(1)

# Get parameters
#
param_mode = sys.argv[1]
param_path = sys.argv[2]

# Read the primes
#
plist = None
try:
  plist = parse_primes.parse(param_path)
  
except PrimeError as pe:
  print('Error:', pe)
  sys.exit(1)

# Handle the modes to build the output
#
output = io.StringIO()
if param_mode == 'html':
  output.write('<table>')
  buf = []
  for i in plist:
    # Ignore primes that are 2 or less
    if i <= 2:
      continue
    
    # If prime is exceeding limit of 2048, then leave loop
    if i >= 2048:
      break
    
    # Add prime to buffer
    buf.append(i)
    
    # If buffer has ten primes, output a row and clear buffer
    if len(buf) >= 10:
      output.write('\n  <tr>')
      for bi in buf:
        output.write('<td>')
        output.write(str(bi))
        output.write('</td>')
      output.write('</tr>')
      buf = []
  
  # If partial row remains, output it
  if len(buf) > 0:
    cell_gap = 10 - len(buf)
    output.write('\n  <tr>')
    for bi in buf:
      output.write('<td>')
      output.write(str(bi))
      output.write('</td>')
    output.write('<td')
    if (cell_gap > 1):
      output.write(' colspan="')
      output.write(str(cell_gap))
      output.write('"')
    output.write('></td></tr>')
    buf = []
  
  # Finish the table
  output.write('\n</table>')
  
elif param_mode == 'py':
  output.write('[')
  pcount = 0
  for i in plist:
    # Ignore primes that are 2 or less
    if i <= 2:
      continue
    
    # If prime is exceeding limit of 2048, then leave loop
    if i >= 2048:
      break
    
    # If not first prime to output, comma separator
    if pcount > 0:
      output.write(',')
    
    # If prime number mod 10 is zero, line break and indent; else, space
    if (pcount % 10) == 0:
      output.write('\n  ')
    else:
      output.write(' ')
      
    # Write the prime number
    output.write(str(i))
    
    # Increment prime count
    pcount = pcount + 1

  output.write('\n]')
  
else:
  print('Unrecognized mode!')
  sys.exit(1)

# Print result
#
print(output.getvalue())
