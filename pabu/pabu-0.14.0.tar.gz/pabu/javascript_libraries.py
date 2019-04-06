from .config import load, Mode

javascript_libraries = {
    Mode.DEVELOPMENT: [{
            'url': 'https://cdnjs.cloudflare.com/ajax/libs/react/16.8.4/umd/react.development.js',
            'hash': 'sha256-5qXzTpCme2glpjIMD82N9CvHzot7DsNj+J81wNBYCs8=',
        },{
            'url': 'https://cdnjs.cloudflare.com/ajax/libs/react-dom/16.8.4/umd/react-dom.development.js',
            'hash': 'sha256-zaBIa6kuwEspzOIU5TeB5bATnxmvJFmht9smi5jLH/Q=',
        },{
            'url': 'https://unpkg.com/@material-ui/core@3.9.3/umd/material-ui.development.js',
            'hash': 'sha384-OHgODUxh5l1oYv44Q37dwi/H0/yW9noynTkDzIp0IK2dL1ykwZUSB++YbYbQp4f5',
        },{
            'url': 'https://unpkg.com/react-beautiful-dnd@10.1.0/dist/react-beautiful-dnd.js',
            'hash': 'sha384-E8lHto1m0Yl8oc4JaZihKNlqmEmnm14731VcvV+KXDKJDdbsmXAWQ3zq+RMnKTHD',
        }],
    Mode.PRODUCTION: [{
            'url': 'https://cdnjs.cloudflare.com/ajax/libs/react/16.8.4/umd/react.production.min.js',
            'hash': 'sha256-ctUamuIgSCQg1wsh8Iw0QbDXScmyXhjJ6lxYUscC3FA=',
        },{
            'url': 'https://cdnjs.cloudflare.com/ajax/libs/react-dom/16.8.4/umd/react-dom.production.min.js',
            'hash': 'sha256-8uWWG/7CB3OS89Cw67+B++t6w0EMGfQE9C6OGps+Wd8=',
        },{
            'url': 'https://unpkg.com/@material-ui/core@3.9.3/umd/material-ui.production.min.js',
            'hash': 'sha384-P5QeKgQTUmZqGgEBOi1Yk3Ypri0M/CGnCpPfO6rx1+ecOvwiwlQcxOvhxTzsWbPU',
        },{
            'url': 'https://unpkg.com/react-beautiful-dnd@10.1.0/dist/react-beautiful-dnd.min.js',
             'hash': 'sha384-zo+Gb/fetDb0/fqUY1FIPzktRQi8wZjNWFbhVQREJwAqfX+9g5OkGO8NjTnj6xal',
        }],
}
