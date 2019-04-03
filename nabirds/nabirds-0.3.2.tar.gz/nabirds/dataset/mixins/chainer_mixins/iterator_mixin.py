import numpy as np
import logging

from .base import BaseChainerMixin

class IteratorMixin(BaseChainerMixin):
	def new_iterator(self, n_jobs, batch_size, repeat=True, shuffle=True, n_prefetch=2):
		self.chainer_check()
		from chainer.iterators import SerialIterator, MultiprocessIterator

		if n_jobs > 0:
			it = MultiprocessIterator(self,
				n_processes=n_jobs,
				n_prefetch=n_prefetch,
				batch_size=batch_size,
				repeat=repeat, shuffle=shuffle)
		else:
			it = SerialIterator(self,
				batch_size=batch_size,
				repeat=repeat, shuffle=shuffle)
		logging.info("Using {it.__class__.__name__} with batch size {it.batch_size}".format(it=it))
		n_batches = int(np.ceil(len(self) / it.batch_size))
		return it, n_batches
