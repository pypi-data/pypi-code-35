import os

import docker
import dockerpty


class Docker:
    def __init__(self):
        self.client = docker.from_env()

    def shell(self, image, tag='latest'):
        # container = self.client.containers.run(
        #     image + ':' + tag,
        #     user=os.getuid(),
        #     detach=True,
        #     tty=True,
        #     network_mode='host',
        #     environment=dict(os.environ),
        #     auto_remove=True,
        #     volumes={
        #         '/home': {'bind': '/home', 'mode': 'rw'}
        #     },
        #     stdin_open=True,
        #     working_dir=os.getcwd(),
        # )
        # dockerpty.start(self.client.api, container.id)
        cmd = 'docker run --rm -ti --net=host'
        cmd += ' -v /home:/home -v /etc/passwd:/etc/passwd'
        cmd += ' --user {} -e HOME={} --workdir={}'.format(
            os.getuid(), os.environ['HOME'], os.getcwd())
        cmd += ' {}:{} bash'.format(image, tag)
        os.system(cmd)
