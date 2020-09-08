import sys
import click
import requests
import json
import uuid
import base64

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

URL_BASE = "http://localhost:8080/api/nixzd/v11"


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-b', '--base', type=str, default=URL_BASE, show_default=True, help="Service Base URL")
@click.option('-u', '--user', type=str, default='amis', show_default=True, help="User login")
@click.option('-p', '--password', default='amis', show_default=True, type=str,  help="User password")
@click.option('--pretty', type=bool, default=False, is_flag=True, show_default=True, help="print pretty formatted output")
@click.pass_context
def cli(ctx, base, user, password, pretty):
    """
    ICZ ISAC NIXZD Client - tools for calling services through the NIXZD REST API.

    This tools are intended for testing purposes only.
    """

    ctx.ensure_object(dict)
    ctx.obj.update({
        'base': base.rstrip('/'),
        'user': user,
        'password': password,
        'pretty': pretty,
    })


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
def sayHello(ctx):
    """
    Service tests the NIXZD API availability.
    """
    params = {
    }
    data = call_api(ctx.obj['base'] + '/sayHello', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    if ctx.obj['pretty']:
        print(data)
    else:
        print(data)


@cli.command()
@click.option('--rc', type=str, required=True, help="Patient ID - rodne cislo")
@click.option('--purpose', type=click.Choice(['EMERGENCY', 'TREATMENT', 'PATIENT'], case_sensitive=False), required=True, help="Purpose of use of the required information")
@click.option('--subject', type=str, default="Trpaslik", help="Name or ID of the requesting persion or entity")
@click.option('--reqorgid', type=str, default="Test HCP", help="Name or ID of the requesting HealthCare Provider")
@click.pass_context
def exists(ctx, rc, purpose, subject, reqorgid):
    """
    Service broadcast request for patient information availability to all peer nodes.
    """
    params = {
        'idType': 'RC',
        'idValue': rc,
        'purposeOfUse': purpose.upper(),
        'subjectNameId': str(base64.b64encode(subject.encode('utf-8'))),
        'requestOrgId': reqorgid,
        'requestId': str(uuid.uuid4()),
    }
    data = call_api(ctx.obj['base'] + '/getPsExists.xml', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    if ctx.obj['pretty']:
        print(data)
    else:
        print(data)


@cli.command()
@click.option('--srcid', type=str, required=True, help="Source HealthCare Provider ID")
@click.option('--rc', type=str, required=True, help="Patient ID - rodne cislo")
@click.option('--purpose', type=click.Choice(['EMERGENCY', 'TREATMENT', 'PATIENT'], case_sensitive=False), required=True, help="Purpose of use of the required information")
@click.option('--subject', type=str, default="Trpaslik", help="Name or ID of the requesting persion or entity")
@click.option('--reqorgid', type=str, default="Test HCP", help="Name or ID of the requesting HealthCare Provider")
@click.option('--cdatype', type=click.Choice(['L1', 'L3'], case_sensitive=False), default='L3', help="Type of the HL7 CDA document")
@click.option('--id', type=str, required=True, help="ID of the HL7 CDA document")
@click.option('--oid', type=str, required=True, help="OID of the HL7 CDA document")
@click.option('-o', '--output', type=click.File(mode='wb'), required=False, help="Write the Document Body to file")
@click.pass_context
def cda(ctx, srcid, rc, purpose, subject, reqorgid, cdatype, id, oid, output):
    """
    Get patient HL7 CDA document.
    """
    params = {
        'sourceIdentifier': srcid,
        'idType': 'RC',
        'idValue': rc,
        'purposeOfUse': purpose.upper(),
        'subjectNameId': str(base64.b64encode(subject.encode('utf-8'))),
        'requestOrgId': reqorgid,
        'cdaType': cdatype.upper(),
        'cdaId': id,
        'cdaOid': oid,
        'requestId': str(uuid.uuid4()),
    }
    data = call_api(ctx.obj['base'] + '/getPs.cda', params=params, auth=(ctx.obj['user'], ctx.obj['password']))
    if output:
        output.write(data.encode())
    else:
        if ctx.obj['pretty']:
            print(data)
        else:
            print(data)


if __name__ == '__main__':
    cli(obj={})     # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
