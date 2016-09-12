# Import pytest, so that we can use xfail.
# You should remove this if you find you no longer need pytest.
# flake8 will remind you.
import pytest

# Import all of our testable functions from main.
from main import press_button, which_to_press, dial_to, should_flip


def test_press_button():
    """Test that we'll know when to press the Button Layer button

    Tests press_button function.
    """
    # Needs to be True when input is divisible by 17. 

    # The following should be True. 
    valid = [-34, -17, 0, 17, 34, 51, 68, 85]
    # The following should be False (numbers incremented by 1).
    invalid = [num + 1 for num in valid]

    # Test each value that should be True.
    for num in valid:
        assert(press_button(num) is True)

    # Test each value that should be False.
    for num in invalid:
        assert(press_button(num) is False)


def test_which_to_press():
    """Test that we'll know how to respond to the History Layer

    Tests which_to_press function.
    """
    # Format: which_to_press(history, displayed)
    # History Format: (pressed, displayed) tuple.
    
    # If display shows 1, always return 4. 
    '''
    x = [(1, 4), (25, 100)]
    assert(which_to_press(None, 1) == 4)

    # If display shows 2, return value pressed in previous round.
    assert(which_to_press(x, 2) == 100)

    # If display shows 3, return value displayed in previous round. 
    assert(which_to_press(x, 3) == 25)

    # If display shows 4...
    '''
    pytest.xfail("...")

def test_dial_to():
    """Test that we'll know how to respond to the Code Layer

    Tests dial_to function.
    """

    # dial_to(state, code)
    # Set up a state with a test serial number. 
    state = {
        'suspicion level': 0,
        'indicators': {},
    }
    state['serial number'] = 'JQXX7e3652'

    # Test code 
    code = 'circuit'
    
    # dial_to should return a 'c'
    assert(dial_to(state, code) == 'c')

    # Test another example, should return 'a'. 
    state['serial number'] = 'XX7e3652'
    code = 'elephant'
    assert(dial_to(state, code) == 'a')
    

def test_should_flip():
    """Test that we'll know how to respond to the Switches Layer

    Tests should_flip function.
    """

    # Function: should_flip(bag_state, has_red, has_blue, has_green)
    
    # Test state and serial number: 
    test_state = {
        'suspicion level': 0,
        'indicators': {},
    }
    test_state['serial number'] = 'JQXX7e3652'
    test_state['indicators']['check engine'] = False
    test_state['indicators']['everything ok'] = True 

    # Label D, All off, return False.
    assert(should_flip(test_state, False, False, False) is False)

    # Label C, Red and blue on, green off, False.
    assert(should_flip(test_state, True, True, False) is False)

    # Label E, green and red on, blue off, True.
    assert(should_flip(test_state, True, False, True) is True)

    # Label J, green on, red and blue off, True (J in serial)
    assert(should_flip(test_state, False, False, True) is True)

    # Label Q, all lights on, True (Q in serial)
    assert(should_flip(test_state, True, True, True) is True)

    # Label Y, only blue light on. False (No Y in serial).
    assert(should_flip(test_state, False, True, False) is False)

