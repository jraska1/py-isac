# py-isac
Clients for ISAC REST API and ISAC NIXZD API.

## How to install scripts on your host
The easiest way is to clone the GitHub repository and build virtual environment for launching the script:
```
cd <some directory on your choice>
git clone https://github.com/jraska1/py-isac.git
cd py-isac
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## py_isac - How to get general overview of script features
To launch the script, you have to activate the venv and run it as python script.
For actions and options overview, use -h or --help option as follows:

```
(.venv) [raska@localhost py-isac]$ python py-isac.py --help
Usage: py-isac.py [OPTIONS] COMMAND [ARGS]...

  ICZ ISAC Client - tools for calling services through the REST API.

  This tools are intended for testing purposes only.

Options:
  -b, --base TEXT      Service Base URL  [default: http://localhost:8080/g3/]
  -u, --user TEXT      User login  [default: amis]
  -p, --password TEXT  User password  [default: amis]
  --username TEXT      Full User name
  --pretty             print pretty formatted output  [default: False]
  -h, --help           Show this message and exit.

Commands:
  bedfund   Bed Fund Survey Client.
  docview   Patient Clinical Event Documentation View Client.
  handover  Patient Documentation Handover Client.
  info      ISAC Communication Node operational information.
  patsum    Patient Emergency Information Summary Client.
  recvdoc   Receive Document from other HealthCare Provider.
  senddoc   Send Document to other HealthCare Provider.
  survey    Patient Documentation Survey Client.
```

## nixzd_client - How to get general overview of script features
To launch the script, you have to activate the venv and run it as python script.
For actions and options overview, use -h or --help option as follows:

```
(.venv) [raska@localhost py-isac]$ python nixzd_client.py --help
Usage: nixzd_client.py [OPTIONS] COMMAND [ARGS]...

  ICZ ISAC NIXZD Client - tools for calling services through the NIXZD REST
  API.

  This tools are intended for testing purposes only.

Options:
  -b, --base TEXT      Service Base URL  [default:
                       http://localhost:8080/api/nixzd/v11]
  -u, --user TEXT      User login  [default: amis]
  -p, --password TEXT  User password  [default: amis]
  --pretty             print pretty formatted output  [default: False]
  -h, --help           Show this message and exit.

Commands:
  cda       Get patient HL7 CDA document.
  exists    Service broadcast request for patient information availability...
  sayhello  Service tests the NIXZD API availability.
```

