import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Prisoner-v0',
    entry_point='prisoner_env.envs:PrisonerEnv'
)



