class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False
        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)
        return player_value >= self._value


class All:
    def test(self, player):
        return True


class Not:
    def __init__(self, matcher):
        self.matcher = matcher

    def test(self, player):
        return not self.matcher.test(player)


class HasFewerThan:
    def __init__(self, value, attr):
        self.value = value
        self.attr = attr

    def test(self, player):
        return getattr(player, self.attr) < self.value


class Or:
    def __init__(self, *matchers):
        self.matchers = matchers

    def test(self, player):
        return any(matcher.test(player) for matcher in self.matchers)


class QueryBuilder:
    def __init__(self, matcher=None):
        if matcher is None:
            matcher = All()
        self._matcher = matcher

    def plays_in(self, team):
        matcher2 = And(self._matcher, PlaysIn(team))
        return QueryBuilder(matcher2)

    def has_at_least(self, value, attr):
        matcher2 = And(self._matcher, HasAtLeast(value, attr))
        return QueryBuilder(matcher2)

    def has_fewer_than(self, value, attr):
        matcher2 = And(self._matcher, HasFewerThan(value, attr))
        return QueryBuilder(matcher2)

    def one_of(self, *matchers):
        matcher2 = Or(*matchers)
        return QueryBuilder(matcher2)

    def build(self):
        return self._matcher

