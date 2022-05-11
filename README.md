# whoxyd

Get historical whois info from whoxy using an API key. Tool does the following:

* Gets all historical email addresses and checks if the input domain is in them
* Gets all historical company names and excludes ones containing common privacy services keywords


## Install

```
pipx install git+https://github.com/puzzlepeaches/whoxyd.git
```

## Usage

```
~ wd/whoxyd

Usage: wd [OPTIONS] DOMAIN

  Query Whoxy for the WHOIS information for a domain.

Options:
  -k, --key TEXT  Whoxy API key. Can be set with envvar WHOXY_API_KEY
                  [required]
  -h, --help      Show this message and exit.
```
