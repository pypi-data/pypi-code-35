from LambdaPage import LambdaPage


def print_path(event):
    path = event['pathParameters']
    print(event)


if __name__ == '__main__':
    page = LambdaPage()
    page.add_endpoint('get', '/path', print_path)
    page.start_local()
