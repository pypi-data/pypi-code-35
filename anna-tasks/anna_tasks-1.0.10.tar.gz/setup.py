import setuptools

description = "### anna tasks package"

setuptools.setup(
	name='anna_tasks',
	version='1.0.10',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-tasks',
	description='anna task package',
	long_description=description,
	long_description_content_type='text/markdown',
	packages=[
		'anna_tasks', 'anna_tasks.base', 'anna_tasks.base.checkout', 'anna_tasks.base.checkout.cart',
		'anna_tasks.lillynails',
		'anna_tasks.lillynails.customer', 'anna_tasks.lillynails.customer.login',
		'anna_tasks.lillynails.checkout',
		'anna_tasks.lillynails.checkout.cart', 'anna_tasks.lillynails.checkout.order', 'anna_tasks.template23',
		'anna_tasks.template23.checkout',
		'anna_tasks.template23.checkout.cart', 'anna_tasks.template23.checkout.order',
		'anna_tasks.buildor', 'anna_tasks.buildor.checkout', 'anna_tasks.buildor.checkout.cart',
		'anna_tasks.houseofmansson', 'anna_tasks.houseofmansson.checkout', 'anna_tasks.houseofmansson.checkout.cart'
	]
)
