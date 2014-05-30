forex
=====

Command line tool for converting between currencies using data from
[openexchangerates.org](https://openexchangerates.org).

Requires a free
[openexchangerates.org API key](https://openexchangerates.org/signup)
to be set as the environment variable `OER_APP_ID`:

    $ export OER_APP_ID=yourapikeyhere


Use
---

    $ forex.py 1 GBP USD
    1.676 USD

Also does historical end-of-day rate conversions from 1999 onwards:

    $ forex.py 37 GBP USD -d 1999-03-27
    60.090 USD
