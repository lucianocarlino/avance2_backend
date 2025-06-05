class MEF:
    def __init__(self, state, transition_table, min_mean = None, max_mean = None):
        self.state = state
        self.min_mean = min_mean
        self.max_mean = max_mean
        self.transition_table = transition_table

    def transition(self, event):
        key = (self.state, event)
        if key in self.transition_table:
            if len(self.transition_table[key]) > 2:
                self.state, self.min_mean, self.max_mean = self.transition_table[key]
            else: 
                self.state = self.transition_table[key][0]
                action = self.transition_table[key][1]
                action()