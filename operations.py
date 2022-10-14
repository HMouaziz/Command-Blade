from InquirerPy import inquirer
from InquirerPy.base import Choice
from functions import run_ipconfig


def ipconfig():
    add_param = inquirer.confirm(message="Do you want to add parameters?", default=False).execute()
    if add_param is True:
        param = inquirer.select(
            message="Select a parameter to run:",
            choices=[
                "/all",
                "/allcompartments",
                "/displaydns",
                "/flushdns",
                "/registerdns",
                "/release",
                "/release6",
                "/renew",
                "/renew6",
                "/setclassid",
                "/showclassid",
                Choice(value="/?", name="/help"),
                Choice(value=None, name="Return"),
            ],
            default=None,
        ).execute()
        if param == "/all":
            run_ipconfig(parameter="/all")
        elif param == "/allcompartments":
            run_ipconfig(parameter="/allcompartments")
        elif param == "/displaydns":
            run_ipconfig(parameter="/displaydns")
        elif param == "/flushdns":
            run_ipconfig(parameter="/flushdns")
        elif param == "/registerdns":
            run_ipconfig(parameter="/registerdns")
        elif param == "/release":
            value = inquirer.text(message="This parameter accepts a value:").execute()
            run_ipconfig(parameter="/release", value=value)
        elif param == "/release6":
            value = inquirer.text(message="This parameter accepts a value:").execute()
            run_ipconfig(parameter="", value=value)
        elif param == "/renew":
            value = inquirer.text(message="This parameter accepts a value:").execute()
            run_ipconfig(parameter="", value=value)
        elif param == "/renew6":
            value = inquirer.text(message="This parameter accepts a value:").execute()
            run_ipconfig(parameter="", value=value)
        elif param == "/setclassid":
            value = inquirer.text(message="This parameter accepts a value:").execute()
            run_ipconfig(parameter="", value=value)
        elif param == "/showclassid":
            value = inquirer.text(message="This parameter accepts a value:").execute()
            run_ipconfig(parameter="", value=value)
        elif param == "/?":
            run_ipconfig(parameter="/?")
        elif param is None:
            pass


    elif add_param is False:
        run_ipconfig()