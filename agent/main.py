import sys

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

from setup import check_and_install_dependencies

import actions.ConsumptiveRealism


def main():
    Toolkit.init_option("./")

    socket_id = sys.argv[-1]

    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    check_and_install_dependencies()
    main()
