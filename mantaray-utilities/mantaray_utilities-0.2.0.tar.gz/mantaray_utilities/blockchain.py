def subscribe_event(event_func_name, keeper, agreement_id):
    event_map[event_func_name](keeper, agreement_id)

def _log_event(event_name):
    def _process_event(event):
        print(f'Received event {event_name}.')

    return _process_event

def subscribe_AGREEMENT_CREATED_EVENT(keeper, agreement_id):
    event = keeper.escrow_access_secretstore_template.subscribe_agreement_created(
        agreement_id,
        60,
        _log_event(keeper.escrow_access_secretstore_template.AGREEMENT_CREATED_EVENT),
        (),
        wait=True
    )
    assert event, 'no event for EscrowAccessSecretStoreTemplate.AgreementCreated'

def subscribe_Fulfilled_LockRewardCondition(keeper, agreement_id):
    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id,
        60,
        _log_event(keeper.lock_reward_condition.FULFILLED_EVENT),
        (),
        wait=True
    )
    assert event, 'no event for LockRewardCondition.Fulfilled'

def subscribe_Fulfilled_AccessSecretStoreCondition(keeper, agreement_id):
    event = keeper.access_secret_store_condition.subscribe_condition_fulfilled(
        agreement_id,
        60,
        _log_event(keeper.escrow_reward_condition.FULFILLED_EVENT),
        (),
        wait=True
    )
    assert event, 'no event for AccessSecretStoreCondition.Fulfilled'

def subscribe_Fulfilled_EscrowReward(keeper, agreement_id):
    event = keeper.escrow_reward_condition.subscribe_condition_fulfilled(
        agreement_id,
        60,
        _log_event(keeper.escrow_reward_condition.FULFILLED_EVENT),
        (),
        wait=True
    )
    assert event, 'no event for EscrowReward.Fulfilled'

event_map = {
    "created agreement": subscribe_AGREEMENT_CREATED_EVENT,
    "lock reward": subscribe_Fulfilled_LockRewardCondition,
    "access secret store": subscribe_Fulfilled_AccessSecretStoreCondition,
    "escrow reward": subscribe_Fulfilled_EscrowReward,
}