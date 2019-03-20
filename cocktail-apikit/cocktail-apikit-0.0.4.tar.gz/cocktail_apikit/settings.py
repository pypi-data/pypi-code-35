import os


class DefaultSettings(object):
    """
    Default project global scope
    """

    API_ENV = os.environ.get('API_ENV', 'development')

    # API return data related configuration
    API_DEFAULT_LIMIT = 20
    API_MAXIMUM_LIMIT = 100

    ############################################################
    # Mongo Database configuration template
    ############################################################
    MONGODB_URI = os.environ.get('MONGODB_URI')
    MONGO_DATABASE = {
        'DEFAULT': {
            'development': {
                'DB_NAME': 'default_db',
                'COLLECTION_NAME': 'default_collection'
            },

            'test': {
                'DB_NAME': 'test_default_db',
                'COLLECTION_NAME': 'default_collection'
            },

            'production': {
                'DB_NAME': 'production_default_db',
                'COLLECTION_NAME': 'default_collection'
            },
        }
    }

    @classmethod
    def mongo_db_config(cls, collection_name: str = 'DEFAULT'):
        """
        Return mongo db configuration from environment variable with the given collection_name
        """
        env_config = cls.MONGO_DATABASE.get(collection_name).get(cls.API_ENV)
        env_config.update({'MONGODB_URI': cls.MONGODB_URI})
        return env_config

    ############################################################
    # AWS service configuration
    ############################################################
    AWS_REGION = os.environ.get('AWS_REGION', 'us-west-2')
    AWS = {
        "development": {
            "BUCKET_NAME": "dev-bucket-name"
        },
        "test": {
            "BUCKET_NAME": "test-bucket-name"
        },
        "production": {
            "BUCKET_NAME": "production-bucket-name"
        },

    }

    @classmethod
    def aws_config(cls):
        """
        Return aws's configuration from environment variable 'API_ENV'
        """
        env_config = cls.AWS.get(cls.API_ENV)
        env_config.update({
            'AWS_REGION': cls.AWS_REGION
        })
        return env_config


if __name__ == '__main__':
    os.environ.setdefault('API_ENV', 'development')
    print(DefaultSettings.mongo_db_config())
    print(DefaultSettings.aws_config())
