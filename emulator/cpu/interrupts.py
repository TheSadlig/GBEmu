class Interrupts:
    def __init__(self):
        # If the flag is set, the interrupt will be disable after next operation
        # TODO handle interrupt mechanics when we have the main loop in place
        self.disable_interrupts_after_next = 0
        self.enable_interrupts_after_next = 0

        self.interrupts_enabled = 1