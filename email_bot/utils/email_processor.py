from ..tasks import FederalRegisterTask
from ..exceptions import ParsingException, TaskException
from ..models import OutgoingEmail, IncomingEmail


def _parse_subject(s: str):
    args = s.split(' ')
    cmd_str = args[0]
    if cmd_str[0] != '!':
        raise ParsingException()

    cmd = cmd_str.split('!')[1]
    cmd_args = args[1:]

    return cmd, cmd_args


def _do_task(task: str, args: list) -> OutgoingEmail:
    if task == 'FR':
        return FederalRegisterTask().do(*args)


def process_incoming_email(email: IncomingEmail) -> OutgoingEmail:
    try:
        task, args = _parse_subject(email.subject)
    except ParsingException:
        return OutgoingEmail(subject="Invalid input",
                             body="""Valid Commands:\n\t!FR MM/DD/YY MM/D//YY""")
    # try:
    return _do_task(task, args)
    # except TaskException as e:
    #     return OutgoingEmail(subject="Something went wrong",
    #                          body=str(e))
