from gym.envs.registration import register

register(
    id='nevolution-risk-v1',
    entry_point='nevolution_risk.v1:RiskEnv',
)

register(
    id='nevolution-risk-v2',
    entry_point='nevolution_risk.v2.env:RiskEnv',
)

register(
    id='nevolution-risk-v3',
    entry_point='nevolution_risk.v3.env:RiskEnv',
)

register(
    id='nevolution-risk-v4',
    entry_point='nevolution_risk.v4.env:RiskEnv',
)
