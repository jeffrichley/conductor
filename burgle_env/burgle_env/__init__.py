import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Burgle-v0',
    entry_point='burgle_env.envs:EasyBurgleEnv'
)

register(
    id='BurgleGuard-v0',
    entry_point='burgle_env.envs:EasyGuardBurgleEnv'
)



