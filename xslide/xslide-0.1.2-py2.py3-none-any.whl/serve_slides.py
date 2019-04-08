import os
import sys

from xslide import eval_out_path


def main(args=sys.argv):
    if len(args) > 1:
        file_to_monitor = args[1]
        if not os.path.isfile(file_to_monitor) or not file_to_monitor.endswith(".py"):
            print("USAGE:\n{} presentation_source_path".format(args[0]))
            sys.exit(3)
        file_to_monitor = os.path.abspath(file_to_monitor)

        port = int(args[2]) if len(args) > 2 else 5500
        from livereload import Server, shell

        _, html_root, __ = eval_out_path(file_to_monitor)
        server = Server()
        this_dir = os.path.dirname(os.path.abspath(__file__))
        rebuild_cmd = shell('python3 %s' % file_to_monitor, cwd=os.path.dirname(this_dir))
        rebuild_cmd()
        server.watch(file_to_monitor, rebuild_cmd, delay=1)
        server.serve(root=html_root, port=port)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
