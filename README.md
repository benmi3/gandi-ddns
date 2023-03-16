# Gandi-ddns

This is a simple python program that updated A and AAAA recornds using GANDI API.
I made this for use on my linux machine, but should run on anything can can run python3.

## Requirements
- [] [python3.10 or more (the current version when created)](https://www.python.org/downloads/) 
- [] [Domain on gandi.net](https://www.gandi.net/)
- [] [Gandi Public Api KEY](https://api.gandi.net/docs/authentication/)

## Installation

Download the repository

```bash
git clone https://gitlab.com/benmi/gandi-ddns.git
```
create a .venv
```bash
cd gandi-ddns
python3 -m venv .venv
```
add requirements to venv
```bash
.venv/bin/python3 -m pip install -r requirements.txt
```

## Usage
create a "config.ini" file and use this template
```bash
[section1]
# gandi.net API key
apikey = s3cr3t4p1k3y
# Domain
domain = example.com
# record name
rrset_name = @
# record type
rrset_type = A
# rrset_ttl value 300 ~ 2592000
rrset_ttl = 320
```
or you can run the program once and it will create one for you
```bash
.venv/bin/python3 gandi-ddns.py
```

## Problems

if you have any problems with the script feel free to open an issue.
I will later add a FAQ for often seen problems.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## References

- [ ] [Gandi API References](https://api.gandi.net/docs/livedns/)
- [ ] [ConfigParser](https://docs.python.org/3/library/configparser.html)
- [ ] [Requests](https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes)
- [ ] [Inspired by this github repo](https://github.com/matt1/gandi-ddns)

## License

<dl>
<dt rel="LICENSE">MIT License

Copyright (c) 2023 Benjamin Jorgensen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</dt>
</dl>
