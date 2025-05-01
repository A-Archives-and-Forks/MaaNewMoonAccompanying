import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.setup import check_and_install_dependencies


def main():
    from maa.agent.agent_server import AgentServer
    from maa.toolkit import Toolkit

    import actions.Logger
    import actions.ConsumptiveRealism
    import actions.Platform

    try:
        Toolkit.init_option("./")
        socket_id = sys.argv[-1]
        AgentServer.start_up(socket_id)
        AgentServer.join()
        AgentServer.shut_down()

    except Exception as e:
        print(e)
        print("Agent启动失败！")


if __name__ == "__main__":
    check_and_install_dependencies()
    main()
