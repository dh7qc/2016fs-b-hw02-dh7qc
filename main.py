"""Team Rocket Bag-smith

A tool for opening Bag(TM) using recently discovered manufacturer backdoor.
"""

# For the floor function
from math import floor


def read_int():
    """A helper function for reading an integer from stdin

    :return: The integer that was read
    :rtype: int
    """
    return int(input('>> '))


def read_bool():
    """A helper function for reading a bool from stdin.

    Requires that the user type "1" or "0".

    :return: The bool that was read
    :rtype: int
    """
    val = input('>> ')
    while val not in ('1', '0'):
        print("Answer Yes (1) or No (0)")
        val = input('>> ')
    return bool(int(val))


def press_button(display):
    """Returns True if the display value indicates that the button should
    be pressed.

    :param int display: The current value on the Button Layer display

    :return: True if the button should be pressed
    :rtype: bool
    """

    # Returns true if number is divisible by 17, else false.
    if display % 17 == 0:
        return True
    else:
        return False


def button_layer(bag_state):
    """Interact with the user to override the Button Layer

    :param bag_state: The current state of the bag

    :return: None
    """

    # Status defaults to true to enter loop.
    status = True

    # Loops until status false (input not divisible by 17)
    while status:
        print("What number is displayed?")
        input = read_int()
        status = press_button(input)

        # Increment suspicion level if button pressed.
        if status is True:
            bag_state['suspicion level'] += 1
            print("Press the button!")
        else:
            print("Leave the button alone now.")

    print("Button layer is complete.")


def which_to_press(history, displayed):
    """Returns the integer value of the button to press according to the
    button press history and currently displayed value.

    :param list history: A list of pairs (tuples) that stores the
        history of values displayed and buttons pressed. Each tuple
        looks like: (value_displayed, button_pressed)

    :param int displayed: The value that is currently displayed.

    :return: The label of the button to press.
    :rtype: int
    """
    # History format:
    # history[x][y]
    # x = round number
    # y = 0 = value displayed in round x
    # y = 1 = button pressed in round x

    # If display shows 1, press 4
    if displayed == 1:
        return 4
    # If 2, press button pressed first round.
    elif displayed == 2:
        return history[0][1]
    # If 3, press button pressed in previous round.
    elif displayed == 3:
        prev_round = len(history) - 1
        return history[prev_round][0]
    # Otherwise (4)
    else:
        # Get number of completed rounds.
        completed_rounds = len(history)
        # Calculate round as in the problem description.
        round = floor(completed_rounds / 2)
        # Return the max of the displayed/pressed values.
        if history[round][1] > history[round][0]:
            return history[round][1]
        else:
            return history[round][0]


def history_layer(bag_state):
    """Interact with the user to override the History Layer

    :param bag_state: The current state of the bag.

    :return: None
    """

    # Empty list to store history tuples
    history = []

    # Loop for the 5 rounds.
    for num in range(5):
        # Prompt and get integer input.
        print("What number is displayed right now?")
        display = read_int()

        # Get the number to press and tell user.
        press = which_to_press(history, display)
        print("Press the button labeled", press)

        # Store the data into the history list as tuple.
        history.append((display, press))

        # Add 1 to suspicion level if press is odd.
        if press % 2 == 1:
            bag_state['suspicion level'] += 1

    print("History layer complete.")


def dial_to(bag_state, code):
    """Determines which letter to dial to, based on the bag's serial
    number and code word.

    :param bag_state: The current state of the bag.
    :param str code: The code word that is displayed in the Code Layer

    :return: The letter to turn the dial to
    :rtype: str
    """
    # Get the serial number and its size.
    serial = bag_state['serial number']
    size = len(serial)

    # Get the indexes for slicing the serial.
    first_index = int(serial[size-4])
    last_index = int(serial[size-2]) + 1

    # Slice to get the substring.
    sub_str = code[first_index: last_index]

    # Sort the substring by character into a list.
    sub_str = sorted(sub_str)

    # Return the first character in the list.
    return sub_str[0]


def code_layer(bag_state):
    """Interact with the user to override the Code Layer

    :param bag_state: The current state of the bag.

    :return: None
    """

    # Prompt and get input
    print("What is the displayed code?")
    code = input('>> ')

    # Determine letter to dial to.
    dial = dial_to(bag_state, code)

    print("Turn the dial to", dial)
    print("Code layer complete.")


def should_flip(bag_state, has_red, has_blue, has_green):
    """Determine whether a single switch should be flipped (toggled).

    :param bag_state: The current state of the bag.
    :param bool has_red: True if the red light is on for this switch,
        otherwise False.
    :param bool has_blue: True if the blue light is on for this switch,
        otherwise False.
    :param bool has_green: True if the green light is on for this switch,
        otherwise False.

    :return: True if the user should flip (toggle) this switch, otherwise False
    :rtype: bool
    """

    # Label D, all lights off. Always return false
    if has_red is False and has_blue is False and has_green is False:
        return False
    # Label C, red and blue on, green off
    # Return true if check engine light on
    elif has_red is True and has_blue is True and has_green is False:
        return bag_state['indicators']['check engine']
    # Label E, green and red on, blue off
    # Return true if everything's okay alarm sounding.
    elif has_red is True and has_blue is False and has_green is True:
        return bag_state['indicators']['everything ok']
    # Label J, green on, red and blue off
    # Return true if serial number contains a 'J'
    elif has_red is False and has_blue is False and has_green is True:
        return 'J' in bag_state['serial number']
    # Label Q, all lights on
    # Return true if serial number contains a 'Q'
    elif has_red is True and has_blue is True and has_green is True:
        return 'Q' in bag_state['serial number']
    # Label Y, only blue light on
    # Return true if serial number contains a 'Y'
    else:
        return 'Y' in bag_state['serial number']


def switches_layer(bag_state):
    """Interact with the user to override the Switches Layer

    :param bag_state: The current state of the bag.

    :return: None
    """
    # Get the switch count from the bag
    num_switch = bag_state['switch count']

    # Loops once for every switch.
    for switch in range(num_switch):
        # Prompt and get light statuses.
        print("Does switch {} have a red light?".format(switch))
        red = read_bool()
        print("Does switch {} have a blue light?".format(switch))
        blue = read_bool()
        print("Does switch {} have a green light?".format(switch))
        green = read_bool()

        # Determine whether or not to flip the switch.
        selection = should_flip(bag_state, red, blue, green)

        # Increase suspicion level by 2 if switch needs flipped.
        if selection is True:
            bag_state['suspicion level'] += 2
            print("Flip that switch\n")
        else:
            print("DO NOT flip that switch")

    print("Switches layer is complete.")


def get_bag_state():
    """Interact with the user to create an initial bag state.

    The bag state has several keys:

    * "suspicion level": The bag's current suspicion level (starts at 0).
    * "serial number": The bag's serial number (requires user input).
    * "switch count": The number of switches in the Switches Layer
        (requires user input)
    * "indicators": A dictionary with the following keys:
        * "check engine": True if the bag's Check Engine light is on
            (requires user input)
        * "everything ok": True if the bag's Everything's OK Alarm
            is sounding (requires user input)

    :return: The initial bag state
    :rtype: dict
    """
    state = {
        'suspicion level': 0,
        'indicators': {},
    }

    print("What is the bag's serial number?")
    state['serial number'] = input('>> ')

    print('Is the Check Engine light on?')
    state['indicators']['check engine'] = read_bool()

    print('Is the Everything\'s OK Alarm sounding?')
    state['indicators']['everything ok'] = read_bool()

    print('How many switches are on the bag?')
    state['switch count'] = read_int()

    return state


def main():
    """Program entry point.

    Greets the user and begins interactive layer override
    guide. Prior to exit, the program warns the user to wait a certain
    amount of time before opening the bag.

    :return: None

    """
    print("Welcome to the Bag-smith!")

    state = get_bag_state()

    print("State acquired. Let's start.")

    print("\n**History Layer**")
    history_layer(state)

    print("\n**Code Layer**")
    code_layer(state)

    print("\n**Switches Layer**")
    switches_layer(state)

    print("\n**Button Layer**")
    button_layer(state)

    print("Layers bypassed.")
    print("Wait", state['suspicion level'],
          "seconds or more to allow suspicion level to dissipate.")


if __name__ == '__main__':
    #  Start it
    main()
