import setuptools

setuptools.setup(
  name="jupyter-vscode-server",
  # py_modules rather than packages, since we only have 1 file
  py_modules=['opencode'],
  entry_points={
      'jupyter_serverproxy_servers': [
          'opencode = opencode:setup_opencode',
      ]
  },
  install_requires=['jupyter-server-proxy'],
)