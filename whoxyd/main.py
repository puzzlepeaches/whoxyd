import json

import click
import requests
import validators


class GetWhoisData:
    def __init__(self, domain, response, possible_contacts, bad_registrars):
        self.domain = domain
        self.response = response
        self.possible_contacts = possible_contacts
        self.bad_registrars = bad_registrars

    def get_email(self):
        """Get email from whois record"""

        for i in self.response.json()["whois_records"]:
            try:
                for contact in self.possible_contacts:
                    try:
                        if self.domain in i[contact]["email_address"].split("@")[1]:
                            if not any(
                                bad in i[contact]["email_address"].lower()
                                for bad in self.bad_registrars
                            ):
                                return i[contact]["email_address"]
                            # return i[contact]["email_address"]
                    except KeyError:
                        pass
            except KeyError:
                pass

    def get_company(self):
        """Get company name from whois record"""

        for i in self.response.json()["whois_records"]:
            try:
                for contact in self.possible_contacts:
                    if not any(
                        bad in i[contact]["company_name"].lower()
                        for bad in self.bad_registrars
                    ):
                        return i[contact]["company_name"]
            except KeyError:
                continue


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.argument("domain", required=True)
@click.option(
    "-k",
    "--key",
    required=True,
    type=click.STRING,
    envvar="WHOXY_API_KEY",
    help="Whoxy API key. Can be set with envvar WHOXY_API_KEY",
)
def main(domain, key):
    """
    Query Whoxy for the WHOIS information for a domain.
    """

    # Defining poassible contact types
    possible_contacts = [
        "registrant_contact",
        "administrative_contact",
        "technical_contact",
    ]
    dat = {
        "domain": domain,
        "found": False,
        "email": None,
        "company": None,
    }

    # Defining bad registrar names
    bad_registrars = ["protection", "privacy", "guard", "proxy", "domain", "whois"]

    # Checking if the domain input is valid
    if not validators.domain(domain):
        raise click.BadParameter("Invalid domain!")

    try:
        response = requests.get(f"http://api.whoxy.com/?key={key}&history={domain}")
    except requests.exceptions.RequestException as e:
        dat["error"] = str(e)
        print(json.dumps(dat, indent=4))
        exit(1)

    # Instantiate the GetWhoisData class
    try:
        getwhoisdata = GetWhoisData(domain, response, possible_contacts, bad_registrars)
    except Exception as err:
        dat["error"] = str(err)
        print(json.dumps(dat, indent=4))
        exit(1)

    # Get historical email addresses and company names
    try:
        email = getwhoisdata.get_email()
        company = getwhoisdata.get_company()
    except Exception as err:
        dat["error"] = str(err)
        print(json.dumps(dat, indent=4))
        exit(1)

    if email is not None:
        dat["found"] = True
        dat["email"] = email
    if company is not None:
        dat["found"] = True
        dat["company"] = company

    print(json.dumps(dat, indent=4))


if __name__ == "__main__":
    main()
