import sys
import click
import requests
import json
import re
import base64


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

URL_BASE = "http://localhost:8080/g3/"

API_VERSION_MIN = "4.01.00"


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-b', '--base', type=str, default=URL_BASE, show_default=True, help="Service Base URL")
@click.option('-u', '--user', type=str, default='amis', show_default=True, help="User login")
@click.option('-p', '--password', default='amis', show_default=True, type=str,  help="User password")
@click.option('--username', type=str, help="Full User name")
@click.option('--pretty', type=bool, default=False, is_flag=True, show_default=True, help="print pretty formatted output")
@click.pass_context
def cli(ctx, base, user, password, username, pretty):
    """
    ICZ ISAC Client - tools for calling services through the REST API.

    This tools are intended for testing purposes only.
    """

    ctx.ensure_object(dict)
    ctx.obj.update({
        'base': base.rstrip('/'),
        'user': user,
        'password': password,
        'username': username,
        'pretty': pretty,
    })


def validate_date(ctx, param, value):
    if value and not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        raise click.BadParameter('date parameter should be in format YYYY-MM-DD')
    return value


def call_api(url, *, params=None, json=None, headers=None, auth=(), accept_codes=()):
    try:
        resp = requests.post(url, data=params, json=json, headers=headers, auth=auth)
        if resp.status_code in accept_codes:
            return None
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}", file=sys.stderr)
        sys.exit(1)


@cli.command()
@click.pass_context
def info(ctx):
    """
    ISAC Communication Node operational information.
    """
    params = {
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/app.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.pass_context
def config(ctx):
    """
    Communication Node Configuration information.
    """
    params = {
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/nodeconfig.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.pass_context
def status(ctx):
    """
    Communication Node Status information.
    """
    params = {
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/nodestatus.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.pass_context
def provider(ctx):
    """
    HealthCare Provider detail information as a source for editing.
    """
    params = {
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/confedit/provider.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.pass_context
def prodsys(ctx):
    """
    Production system detail information.
    """
    params = {
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/prodsys/get.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('--id', type=str, required=True, help="Patient ID - rodne cislo")
@click.option('--firstname', type=str, required=False, help="Patient First Name")
@click.option('--lastname', type=str, required=False, help="Patient Last Name")
@click.pass_context
def patsum(ctx, id, firstname, lastname):
    """
    Patient Emergency Information Summary Client.
    """
    params = {
        'rc': id,
        'firstname': firstname,
        'lastname': lastname,
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/ec.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('--provoid', type=str, required=True, help="HealthCare Provider OID")
@click.option('--eventid', type=str, required=True, help="Clinical Event ID")
@click.pass_context
def docview(ctx, provoid, eventid):
    """
    Patient Clinical Event Documentation View Client.
    """
    params = {
        'icz': provoid,
        'eventId': eventid,
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/DocumentView.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('--rc', type=str, required=True, help="Patient ID - rodne cislo")
@click.option('--lastname', type=str, help="Patient Surname")
@click.option('--from', 'fromdate', type=str, default='2000-01-01', show_default=True, callback=validate_date, help="Start date for searching documents")
@click.option('--to', 'todate', type=str, callback=validate_date, help="End date for searching documents")
@click.pass_context
def survey(ctx, rc, lastname, fromdate, todate):
    """
    Patient Documentation Survey Client.
    """
    params = {
        'rc': rc,
        'lastname': lastname,
        'from': fromdate,
        'to': todate,
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/survey.json', json=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('--patoid', type=str, required=False, help="Patient OID")
@click.option('--orgoid', type=str, required=True, help="HealthCare Provider OID")
@click.option('--docoid', type=str, required=True, help="Document OID")
@click.option('--bodytype', type=str, required=False, default="text/plain", show_default=True, help="Required MimeType of the Document")
@click.option('-o', '--output', type=click.File(mode='wb'), required=False, help="Write the Document Body to file")
@click.pass_context
def handover(ctx, patoid, orgoid, docoid, bodytype, output):
    """
    Patient Documentation Handover Client.
    """
    params = {
        'patoid': patoid,
        'orgoid': orgoid,
        'docoid': docoid,
        'bodytype': bodytype,
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/handover.json', json=params, auth=(ctx.obj['user'], ctx.obj['password']))

    if output:
        data = json.loads(data)
        if 'body' in data:
            body = base64.b64decode(data['body'])
            output.write(body)
    else:
        print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('--contype', type=str, required=False, default="application/xml", show_default=True, help="Document Content Type")
@click.option('-i', '--input', 'inputFile', type=click.File(mode='rb'), required=False, help="Read the Document Body from file")
@click.pass_context
def senddoc(ctx, contype, inputFile):
    """
    Send Document to other HealthCare Provider.
    """
    params = inputFile.read()
    headers = {
        'Content-Type': contype,
    }
    data = call_api(ctx.obj['base'] + '/msgstore/senddoc.json', params=params, headers=headers, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('-o', '--output', type=click.File(mode='wb'), required=False, default=sys.stdout, show_default=True, help="Write the Document Body to file")
@click.pass_context
def recvdoc(ctx, output):
    """
    Receive Document from other HealthCare Provider.
    """
    data = call_api(ctx.obj['base'] + '/msgstore/download', auth=(ctx.obj['user'], ctx.obj['password']), accept_codes=(404, ))
    if data:
        output.write(data)


@cli.command()
@click.pass_context
def bedfund(ctx):
    """
    Bed Fund Survey Client.
    """
    params = {
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/beds.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


@cli.command()
@click.option('--period', type=str, required=False, help="Date interval for records [dd.mm.yyyy - dd.mm.yyyy]")
@click.option('--status', type=str, required=False, help="Record status to be selected, allowed values: A B C F P or combination")
@click.pass_context
def rescnotif(ctx, period, status):
    """
    Rescue Notifications Survey Client.
    """
    params = {
        'period':   period,
        'status':   status,
        'username': ctx.obj['username'],
    }
    data = call_api(ctx.obj['base'] + '/rescnotif.json', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    print(json.dumps(json.loads(data), indent=4) if data and ctx.obj['pretty'] else data)


if __name__ == '__main__':
    cli(obj={})     # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
