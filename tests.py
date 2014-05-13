from unittest import TestCase

from tinyfsm import *


__author__ = 'tonyfunc'


class TestState0(TinyState):
    def __init__(self, key, is_initial_state=False):
        super(TestState0, self).__init__(key, is_initial_state)

    def enter(self, owner):
        print('Entering TestState1')

    def execute(self, owner):
        print('Executing TestState1')

    def exit(self, owner):
        print('Exiting TestState1')


class TestState1(TinyState):
    def __init__(self, key, is_initial_state=False):
        super(TestState1, self).__init__(key, is_initial_state)

    def enter(self, owner):
        print('Entering TestState2')

    def execute(self, owner):
        print('Executing TestState2')

    def exit(self, owner):
        print('Exiting TestState2')


class TestTinyFSM(TestCase):
    def setUp(self):
        print('Setting up a new FSM...')
        self.fsm = TinyFSM(self)
        self.state0 = TestState0('state0', True)
        self.state1 = TestState1('state1')
        self.fsm.add_state(self.state0)
        self.fsm.add_state(self.state1)

    def test_add_state(self):
        self.assertRaises(InvalidStateError, self.fsm.add_state, 'invalid state')
        self.assertRaises(InvalidStateError, self.fsm.add_state, TestState1(None))
        self.assertRaises(DuplicateStateError, self.fsm.add_state, TestState0('state0'))
        self.assertRaises(StateMachineError, self.fsm.add_state, TestState0('state2', True))

    def test_change_state(self):
        self.assertIsNotNone(self.fsm.current_state)
        self.assertIsNone(self.fsm.previous_state)
        self.assertRaises(StateNotFoundError, self.fsm.change_state, 'error')
        self.fsm.process()
        self.fsm.change_state('state1')
        self.assertEqual(self.fsm.current_state, self.state1)

    def test_revert_to_previous_state(self):
        self.assertIsNotNone(self.fsm.current_state)
        self.assertIsNone(self.fsm.previous_state)
        state = self.fsm.current_state
        self.fsm.change_state('state1')
        self.assertEqual(self.fsm.previous_state, state)
        self.assertNotEqual(self.fsm.current_state, state)
        self.fsm.revert_to_previous_state()
        self.assertEqual(self.fsm.current_state, state)
        self.assertNotEqual(self.fsm.previous_state, state)