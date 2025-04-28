import sys

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

import actions.Logger
import actions.ConsumptiveRealism


def main():
    Toolkit.init_option("./")

    socket_id = sys.argv[-1]

    AgentServer.start_up("1bcf6108-75f3-47e4-bc96-f8b5a237901e")
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()
