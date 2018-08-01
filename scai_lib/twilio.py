import json
from   twilio.rest import Client


class TwilioClient(Client):
    @classmethod
    def from_json(cls, filepath):
        """
        Expect a json file whose content looks like:

        {
          "account_sid" : "...",
          "auth_token" : "...",
          "default_number" : "..."
        }

        """
        with open(filepath) as f:
            jso = json.load(f)
        cli = cls(jso["account_sid"], jso["auth_token"])
        # Let's hope this doesn't overwrite existing attributes...
        cli.default_number = jso['default_number']
        return cli


_CLIENT = None

def configure(json_path):
    global _CLIENT
    _CLIENT = TwilioClient.from_json(json_path)


def text(to, body):
    if _CLIENT is None:
        raise ValueError("Client not initiated. Call twilio.configure first")
    _CLIENT.messages.create(
        to=to, from_=_CLIENT.default_number, body=body
    )
    
