from skale.contracts import BaseContract


class ValidatorsData(BaseContract):
    def get_reward_period(self):
        constants = self.skale.get_contract_by_name('constants')
        return constants.contract.functions.rewardPeriod().call()

    def get_delta_period(self):
        constants = self.skale.get_contract_by_name('constants')
        return constants.contract.functions.deltaPeriod().call()
