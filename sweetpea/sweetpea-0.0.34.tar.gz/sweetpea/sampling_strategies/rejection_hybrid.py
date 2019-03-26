from sweetpea.sampling_strategies.base import SamplingStrategy, SamplingResult
from sweetpea.blocks import Block

"""
This strategy works by uniformly sampling a permutation of the trials that comprise the crossing,
and then uses a sampler to fill in the rest of the solution with the permutation for a particlar
sequence fixed.

The hope is that pinning the permutation of the trials in the crossing will reduce the search space
enough to make sampling with unigen or spur tractable.
"""
class RejectionHybridSamplingStrategy(SamplingStrategy):

    @staticmethod
    def sample(block: Block, sample_count: int) -> SamplingResult:
        return SamplingResult([], {})
