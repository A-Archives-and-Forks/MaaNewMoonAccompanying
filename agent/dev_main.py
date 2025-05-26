import sys

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

import custom.Logger
import custom.ConsumptiveRealism
import custom.Platform
import custom.PeriodicInspection
import custom.Strap
import custom.Counter
import custom.Procurement
import custom.Timer
import custom.Pipeliner
import custom.RewardSelect

def main():
    Toolkit.init_option("./")

    socket_id = sys.argv[-1]

    AgentServer.start_up("1bcf6108-75f3-47e4-bc96-f8b5a2379011")
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()
