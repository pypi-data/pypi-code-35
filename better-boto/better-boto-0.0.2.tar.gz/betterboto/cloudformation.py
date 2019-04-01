import types


def create_or_update(self, **kwargs):
    stack_name = kwargs.get('StackName')

    is_first_run = True
    try:
        self.describe_stacks(
            StackName=stack_name
        )
        is_first_run = False
    except self.exceptions.ClientError as e:
        if "Stack with id {} does not exist".format(stack_name) not in str(e):
            raise e

    if is_first_run:
        self.create_stack(**kwargs)
        waiter = self.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
    else:
        try:
            self.update_stack(**kwargs)
            waiter = self.get_waiter('stack_update_complete')
            waiter.wait(StackName=stack_name)
        except Exception as e:
            if "No updates are to be performed" not in str(e):
                raise e


def make_better(client):
    client.create_or_update = types.MethodType(create_or_update, client)
    return client
