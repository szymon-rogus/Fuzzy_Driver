import numpy as np
import skfuzzy as fuzzy
import skfuzzy.control as ctrl


def create_system(rules):
    warning_system = ctrl.ControlSystem(rules)
    warning = ctrl.ControlSystemSimulation(warning_system)
    return warning


class FuzzyWarner(object):
    def __init__(self):
        self.temperature = ctrl.Antecedent(np.arange(-40, 41, 1), 'temperature')
        self.humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'air_humidity')
        self.rainless_days = ctrl.Antecedent(np.arange(0, 41, 1), 'rainless_days_period')
        self.warning_level = ctrl.Consequent(np.arange(0, 11, 1), 'warning_level')

    def create_fuzzy_functions(self):
        self.warning_level['low'] = fuzzy.trimf(self.warning_level.universe, [0, 0, 4])
        self.warning_level['medium'] = fuzzy.trimf(self.warning_level.universe, [2, 4, 7])
        self.warning_level['high'] = fuzzy.trimf(self.warning_level.universe, [5, 8, 10])
        self.warning_level['very_high'] = fuzzy.trimf(self.warning_level.universe, [7, 10, 10])

        self.temperature['hot'] = fuzzy.trapmf(self.temperature.universe, [25, 30, 40, 40])
        self.temperature['warm'] = fuzzy.trapmf(self.temperature.universe, [15, 20, 30, 35])
        self.temperature['chill'] = fuzzy.trapmf(self.temperature.universe, [5, 10, 15, 25])
        self.temperature['cool'] = fuzzy.trapmf(self.temperature.universe, [-10, 0, 5, 10])
        self.temperature['cold'] = fuzzy.trapmf(self.temperature.universe, [-40, -40, -20, 0])

        self.humidity['very_dry'] = fuzzy.trapmf(self.humidity.universe, [0, 0, 15, 30])
        self.humidity['dry'] = fuzzy.trapmf(self.humidity.universe, [10, 25, 35, 45])
        self.humidity['moderate'] = fuzzy.trapmf(self.humidity.universe, [30, 40, 50, 60])
        self.humidity['humid'] = fuzzy.trapmf(self.humidity.universe, [45, 60, 75, 85])
        self.humidity['very_humid'] = fuzzy.trapmf(self.humidity.universe, [70, 95, 100, 100])

        self.rainless_days['long'] = fuzzy.trapmf(self.rainless_days.universe, [14, 21, 40, 40])
        self.rainless_days['average'] = fuzzy.trapmf(self.rainless_days.universe, [5, 7, 14, 21])
        self.rainless_days['short'] = fuzzy.trapmf(self.rainless_days.universe, [0, 0, 3, 7])

    def view_all_fuzzy_functions(self):
        self.temperature.view()
        self.humidity.view()
        self.rainless_days.view()
        self.warning_level.view()

    def create_rules(self):
        rules = [ctrl.Rule(
            self.temperature['cold'] | self.temperature['cool'] | self.temperature['chill'] | self.humidity['very_humid'],
            self.warning_level['low']),
                 ctrl.Rule(self.humidity['humid'] & self.temperature['hot'], self.warning_level['medium']),
                 ctrl.Rule(self.humidity['humid'] & self.temperature['warm'] & self.rainless_days['long'], self.warning_level['medium']),
                 ctrl.Rule(
                     self.humidity['humid'] & self.temperature['warm'] & (
                             self.rainless_days['average'] | self.rainless_days['short']),
                     self.warning_level['low']),
                 ctrl.Rule(self.temperature['warm'] & self.rainless_days['short'], self.warning_level['low']),
                 ctrl.Rule(self.temperature['warm'] & self.rainless_days['average'] & self.humidity['moderate'], self.warning_level['low']),
                 ctrl.Rule(self.temperature['warm'] & self.rainless_days['long'] | self.humidity['moderate'], self.warning_level['medium']),
                 ctrl.Rule(self.temperature['warm'] & self.humidity['dry'] & (
                             self.rainless_days['long'] | self.rainless_days['average']),
                           self.warning_level['medium']),
                 ctrl.Rule(self.temperature['warm'] & self.humidity['very_dry'] & self.rainless_days['average'],
                           self.warning_level['medium']),
                 ctrl.Rule(self.temperature['warm'] & self.humidity['very_dry'] & self.rainless_days['long'], self.warning_level['high']),
                 ctrl.Rule(self.temperature['hot'] & self.humidity['moderate'], self.warning_level['medium']),
                 ctrl.Rule(self.temperature['hot'] & self.humidity['dry'] & self.rainless_days['long'], self.warning_level['very_high']),
                 ctrl.Rule(self.temperature['hot'] & self.humidity['dry'] & self.rainless_days['average'], self.warning_level['high']),
                 ctrl.Rule(self.temperature['hot'] & self.humidity['dry'] & self.rainless_days['short'], self.warning_level['medium']),
                 ctrl.Rule(
                     self.temperature['hot'] & self.humidity['very_dry'] & (
                                 self.rainless_days['long'] | self.rainless_days['average']),
                     self.warning_level['very_high']),
                 ctrl.Rule(self.temperature['hot'] & self.humidity['very_dry'] & self.rainless_days['short'], self.warning_level['high'])]

        return rules

