# Jacques-ID
Python library for generating unique and permanent ID codes.

The complete client library for Jacques-ID is contained within `jcqid.py`

See the Jacques-ID specification in the `doc` directory for documentation.  Documentation is also included within each of the script files.

The other scripts are utility programs that the client does not normally need to use.  `check_cycles.py` verifies a mathematical property of prime numbers, as described in the specification.  `parse_primes.py` is used for parsing a data file that stores prime numbers.  `prime_table.py` generates tables of prime numbers that are used both in the Jacques-ID specification and the `jcqid.py` and `check_cycles.py` scripts.
