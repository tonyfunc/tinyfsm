__author__ = 'tonyfunc'


class InvalidStateError(Exception):
    pass


class DuplicateStateError(Exception):
    pass


class StateNotFoundError(Exception):
    pass


class StateMachineError(Exception):
    pass


class TinyState(object):
    """
    A class that represents a state of a FiniteStateMachine.
    """

    def __init__(self, key, is_initial_state=False):
        self.__key__ = key
        self.is_initial_state = is_initial_state

    @property
    def key(self):
        return self.__key__

    def enter(self, owner):
        pass

    def execute(self, owner):
        pass

    def exit(self, owner):
        pass


class TinyFSM(object):
    """
    FiniteStateMachine implementation.
    """

    def __init__(self, owner):
        self.__owner__ = owner
        self.__states__ = {}
        self.__previous_state__ = None
        self.__current_state__ = None
        self.__initial_state__ = None

    @property
    def previous_state(self):
        """
        Previous state.
        """
        return self.__previous_state__

    @property
    def current_state(self):
        """
        Current state.
        """
        return self.__current_state__

    def process(self):
        """
        Runs execute method of the current state instance.
        """
        if self.current_state:
            self.current_state.execute(self.__owner__)

    def add_state(self, state):
        """
        Adds a state to the FSM.
        :param state:                   FSMStateMixin instance.
        :raises InvalidStateError:      Raised when the given state is not an instance of TinyState, or when the \
        given state's key is invalid.
        :raises DuplicateStateError:    Raised when the given key is already found in the FSM.
        :raises StateMachineError:      Raised when a state marked as initial state is given when there already is \
        one registered.
        """
        if not state or not isinstance(state, TinyState):
            raise InvalidStateError('%s is not a valid state.' % unicode(state))
        if not state.key:
            raise InvalidStateError('%s is not a valid state key.' % unicode(state.key))
        if state.key in self.__states__:
            raise DuplicateStateError('State key %s already exists.' % unicode(state.key))
        num_init_states = len([x for x in self.__states__.values() if x.is_initial_state])
        if num_init_states > 0 and state.is_initial_state:
            raise StateMachineError('The number of initial states should be equal to 1.')
        self.__states__[state.key] = state
        if state.is_initial_state:
            self.__initial_state__ = state
            self.change_state(state.key)

    def change_state(self, key):
        """
        Attempts to change state to a FSMStateMixin instance paired with the given key.
        :param key:                     Key paired with the State.
        :raises StateNotFoundError:     Raised when failed to find a State with the given key.
        """
        if key not in self.__states__:
            raise StateNotFoundError('No state was found with the key \'%s\'' % key)
        state = self.__states__[key] if key in self.__states__ else None
        if self.current_state:
            self.current_state.exit(self.__owner__)
        self.__previous_state__ = self.current_state
        self.__current_state__ = state
        if self.current_state:
            self.current_state.enter(self.__owner__)

    def revert_to_previous_state(self):
        """
        Attempts to revert to the previous state.
        """
        if self.previous_state:
            self.change_state(self.previous_state.key)