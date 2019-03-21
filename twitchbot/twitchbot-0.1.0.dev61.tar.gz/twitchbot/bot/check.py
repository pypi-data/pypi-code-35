import datetime

from twitchbot.bot.context import Context
from twitchbot.bot.user import User


class Check:
    def __init__(self):
        self.description = f''

    async def check(self, cmd: 'Command', ctx: Context):
        return True


class HasRank(Check):
    def __init__(self, rank):
        super().__init__()
        self._rank = rank
        self.description = f'rank {self._rank} is required'

    async def check(self, cmd: 'Command', ctx: Context):
        return ctx.author.rank.has(self._rank)


class NotRank(HasRank):
    def __init__(self, rank):
        super().__init__(rank)
        self.description = f'rank {self._rank} is not allowed'

    async def check(self, cmd: 'Command', ctx: Context):
        return not await super().check(ctx)


class MinRank(Check):
    def __init__(self, rank):
        super().__init__()
        self._rank = rank
        self.description = f'minimum rank {self._rank} is required'

    async def check(self, cmd: 'Command', ctx: Context):
        return ctx.author.rank.has_power(ctx.author.rank.convert_rank(self._rank).power)


class IsOwner(Check):
    def __init__(self):
        super().__init__()
        self.description = f'you should be owner'

    async def check(self, cmd: 'Command', ctx: Context):
        return ctx.author.login == ctx.bot.channel


class NotOwner(IsOwner):
    def __init__(self):
        super().__init__()
        self.description = f'you should not be owner'

    async def check(self, cmd: 'Command', ctx: Context):
        return not await super().check(ctx)


class HasState(Check):
    def __init__(self, *states):
        super().__init__()
        self._states = states
        self.description = f'following state(s) should be true: {", ".join(self._states)}'

    async def check(self, cmd: 'Command', ctx: Context):
        for state in self._states:
            if not ctx.bot.get_state(state, default=False):
                return False
        return True


class NotState(HasState):
    def __init__(self, *states):
        super().__init__(*states)
        self.description = f'following state(s) should be false: {", ".join(self._states)}'

    async def check(self, cmd: 'Command', ctx: Context):
        if len(self._states) == 0:
            return True
        return not await super().check(cmd, ctx)


class CoolDown(Check):
    def __init__(self, cool_down):
        super().__init__()
        if isinstance(cool_down, datetime.timedelta):
            self._cool_down: datetime.timedelta = cool_down
        else:
            self._cool_down: datetime.timedelta = datetime.timedelta(seconds=cool_down)

    async def check(self, cmd: 'Command', ctx: Context):
        if cmd.last_execution and (datetime.datetime.now() < (cmd.last_execution + self._cool_down)):
            self.description = f'command is on cool down ({round(((cmd.last_execution + self._cool_down) - datetime.datetime.now()).total_seconds(), 2)} seconds)'
            return False
        return True


class UserCoolDown(Check):
    def __init__(self, cool_down):
        super().__init__()
        if isinstance(cool_down, datetime.timedelta):
            self._cool_down: datetime.timedelta = cool_down
        else:
            self._cool_down: datetime.timedelta = datetime.timedelta(seconds=cool_down)

        self._users = dict()

    async def check(self, cmd: 'Command', ctx: Context):
        if isinstance(ctx.author, User) and ctx.author.is_api():
            user = ctx.author.login
        else:
            user = str(ctx.author)

        if user not in cmd._user_executions:
            return True

        if datetime.datetime.now() < (cmd._user_executions[user] + self._cool_down):
            self.description = f'command is on cool down ({round(((cmd._user_executions[user] + self._cool_down) - datetime.datetime.now()).total_seconds(), 2)} seconds) for you'
            return False
        return True
