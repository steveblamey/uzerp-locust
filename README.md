# uzERP Locust Testing

A <a href="http://locust.io">locust</a> file for load testing uzERP

## Installation

```
$ git checkout https://github.com/steveblamey/uzerp-locust.git
$ cd uzerp-locust

$ virtualenv env
$ source env/bin/activate

$ pip-install -r requirements.txt
```

Edit ```config.py``` to suit.

Run locust:

```
$ locust --no-web -c 5 -r 2 -n 20
```

_See the Locust website for more information on the locust command line._

## Links

uzERP is a Business Management System (ERP).

* Website: <a href="https://www.uzerp.com/">uzerp.com</a>
* Wiki: <a href="https://wiki.uzerp.com/">wiki.uzerp.com</a>
* locust.io: <a href="http://locust.io">locust</a>

## Authors

<a href="https://steveblamey.co.uk">Steve Blamey</a> (@<a href="http://twitter.com/steveblamey">steveblamey</a> on Twitter)

## License

Open source licensed under the MIT license (see _LICENSE_ file for details).
