# Module level imports
from fuzzy.System import System
from fuzzy.norm.Min import Min
from fuzzy.norm.Max import Max
from fuzzy.defuzzify.COG import COG
from fuzzy.operator.Not import Not
from fuzzy.operator.Compound import Compound
from fuzzy.operator.Input import Input
from fuzzy.Rule import Rule
from fuzzy.OutputVariable import OutputVariable


class PendulumController(System):
    """
    Fuzzy controller.
    """

    def __init__(self, defuzzy=COG, norm=Min,
                 conorm=Max, negation=Not):
        """
        Creates and initialize the controller.

        :Parameters:
          defuzzy
            The defuzzification method to be used. If none is given, the
            Centroid method is used;
          norm
            The norm (``and`` operation) to be used. Defaults to Min and.
          conorm
            The conorm (``or`` operation) to be used. Defaults to Max or.
          negation
            The negation (``not`` operation) to be used. Defaults to Not not.
        """
        super(PendulumController, self).__init__()
        self.defuzzy = defuzzy
        self.__AND__ = norm
        self.__OR__ = conorm
        self.__NOT__ = negation

    def __call__(self, input, output):
        od = self.calculate(input, output)
        for o in od:
            return od[o]

    def add_rule(self, opr_adjs, adjective):
        """
        Adds a decision rule to the knowledge base.

        :Parameters:
          opr_adjs
            The input adjectives
          adjective
            The output adjective
        """
        adj1, adj2 = opr_adjs
        rule_num = len(self.rules) + 1
        self.rules[str(rule_num)] = Rule(
            adjective=adjective,
            # it gets its value from here
            operator=Compound(
                self.__AND__(),
                Input(adj1),
                Input(adj2)
            )
        )

    def add_table(self, lx1, lx2, table):
        """
        Adds a table of decision rules in a two variable controller.

        :Parameters:
          lx1
            The set of membership functions to the variable ``x1``, or the
            lines of the table
          lx2
            The set of membership functions to the variable ``x2``, or the
            columns of the table
          table
            The consequent of the rule where the condition is the line ``and``
            the column. These can be the membership functions or fuzzy sets.
        """
        for i in range(len(lx1)):
            for j in range(len(lx2)):
                my = table[i][j]
                if my is not None:
                    self.add_rule((lx1[i], lx2[j]), my)

    def set_norm(self, norm):
        self.__AND__ = norm
        for rule in self.rules.values():
            rule.operator.norm = self.__AND__()

    def set_defuzzy(self, defuzzy):
        self.defuzzy = defuzzy
        for variable in self.variables.values():
            if isinstance(variable, OutputVariable):
                variable.defuzzify = self.defuzzy()
