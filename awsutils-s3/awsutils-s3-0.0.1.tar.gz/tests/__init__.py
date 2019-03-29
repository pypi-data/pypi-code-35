from ._config import S3_BUCKET, TEST_PATH, LOCAL_BASE, LOCAL_PATH


def printer(header, body):
    """Pretty print lists for visual check that correct output was returned."""
    print('\n{0}:\n'.format(header.upper()) + '\n'.join('\t{0}'.format(b) for b in body))


__all__ = ['S3_BUCKET', 'TEST_PATH', 'LOCAL_BASE', 'LOCAL_PATH', 'printer']
