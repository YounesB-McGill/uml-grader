
from typing import List

class Grading:
    def __init__(self, name: str, classes: float, attributes: float, associations: float):
        self.name = name
        self.classes = classes
        self.attributes = attributes
        self.associations = associations
        self.total_without_multiplicities = (classes + attributes + associations)/3
        self.total_with_multiplicities = (classes + attributes +  2*associations)/4

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""{self.name}, {[self.classes, self.attributes, self.associations,
                                  self.total_without_multiplicities, self.total_with_multiplicities]}"""


class StudentModel:
    def __init__(self, identifier, gradings: List[Grading]):
        self.identifier = identifier
        self.gradings = gradings

    def make_feature_vector(self, grading_names: List[str]):
        v = []
        for g in self.gradings:
            if g.name in grading_names:
                v.append(g.classes)
                v.append(g.attributes)
                v.append(g.associations)
        return v

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.identifier}\n{self.gradings}\n"
