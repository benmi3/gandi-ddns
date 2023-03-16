# Gandi-ddns

This is a simple python program that updated A and AAAA recornds using GANDI API.

## Requirements
python3.10 or more

## Installation

Download the repository

```bash
git clone https://gitlab.com/benmi/gandi-ddns.git
```
create a .venv
```bash
cd gandi-ddns
python3 -m venv .venv
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


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## References

- [ ] [Gandi API References](https://api.gandi.net/docs/livedns/)
- [ ] [ConfigParser](https://docs.python.org/3/library/configparser.html)
- [ ] [Requests](https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes)
- [ ] [Inspired by this github repo from matt1](https://github.com/matt1/gandi-ddns)

## License

rel="LICENSE"

<dl>
  <dt rel="LICENSE">LICENSE</dt>
</dl>
