#!/usr/bin/env python3

import re
from collections import OrderedDict
from lxml import etree
from typing import Dict, List


IN = "data/ideal.ecore"


# map ecore to cdm types
TYPES: Dict[str, str] = {
    "ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//EString": "//@types.6",
    "#//int": "//@types.4"
}


# association global id
aid = 0


class Class:
    def __init__(self, name):
        self.name = name
        self.associations = OrderedDict()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.name}"


class Association:
    def __init__(self, aid: int, class1: Class, class2: Class, label1="", label2=""):
        self.aid = aid
        self.classes = [class1, class2]
        self.labels = {class1: label1, class2: label2}
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (f"[aid:{self.aid}] "
                f"{self.classes[0]}('{self.labels[self.classes[0]]}')_"
                f"{self.classes[1]}('{self.labels[self.classes[1]]}')")


def make_association(class1: Class, class2: Class, label1="", label2="") -> Association:
    global aid
    assoc = Association(aid, class1, class2, label1, label2)
    aid += 1
    return assoc


def get_class_by_name(classes: List[Class], name: str) -> str:
    for c in classes:
        if c.name == name:
            return c
    print(f"WARNING: Class {name} not found.")


def ecore2cdm(ecore: str) -> str:
    #try:
    n = ecore.split('nsPrefix="')[1].split('"')[0]  # project name

    ecore = re.sub('nsURI="(.*?)" nsPrefix', f'nsURI="{n}" nsPrefix', ecore)
    ecore = (ecore
        .replace('<?xml version="1.0" encoding="UTF-8"?>\n', "")
        .replace("ecore:EPackage", "classdiagram:ClassDiagram", 2)
        .replace('xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore"',
                'xmlns:classdiagram="http://cs.mcgill.ca/sel/cdm/1.0"', 1)
        .replace(f'name="{n}" nsURI="{n}" nsPrefix="{n}"', f'name="{n}"', 1)
        .replace('<eClassifiers xsi:type="ecore:EDataType" name="int" instanceClassName="int" />', "")
    )

    root = etree.fromstring(ecore)

    class_names: List[str] = []
    assoc_pairs: List[str] = []

    classes: List[Class] = []
    associations: List[Association] = []

    # make the classes and the associations 
    for e in root:
        if "ecore:EClass" in e.attrib.values():
            class_name = e.attrib["name"]

            for sf in e:
                # some one dir associations are missing from the ecore source
                if "ecore:EReference" in sf.attrib.values() and "eOpposite" in sf.attrib:  
                    other_class, assoc_name = sf.attrib["eOpposite"].replace("_", "").replace("#//", "").split("/")
                    if "_" in sf.attrib["eOpposite"]:
                        print(f"WARNING: {sf.attrib['eOpposite']} contains underscores, which have been removed.")
                    if f"{other_class}_{class_name}" in assoc_pairs:
                        # we already processed the association(s) in the other direction
                        continue
                    assoc_pairs.append(f"{class_name}_{other_class}")

                    if class_name in class_names:
                        class1 = get_class_by_name(classes, class_name)
                    else:
                        class_names.append(class_name)
                        class1 = Class(class_name)
                        classes.append(class1)
                        
                    if other_class in class_names:
                        class2 = get_class_by_name(classes, other_class)
                    else:
                        class_names.append(other_class)
                        class2 = Class(other_class)
                        classes.append(class2)

                    assoc = make_association(class1, class2, assoc_name)
                    print(class1, class2)
                    class1.associations[f"{other_class}_{assoc_name}"] = assoc
                    class2.associations[f"{class_name}_{assoc_name}"] = assoc
                    associations.append(assoc)


    print(classes, "\n", associations)

    exit(0)

    cdm_class_nodes = []


    # make classes with attributes
    for e in root:
        if "ecore:EClass" in e.attrib.values():
            cdm_class_node = etree.Element("classes", xsitype="ecore:EClass", name=e.attrib["name"])
            for sf in e:
                if "ecore:EAttribute" in sf.attrib.values():
                    cdm_attr_node = etree.SubElement(cdm_class_node, "attributes")
                    cdm_attr_node.set("name", sf.attrib["name"])
                    cdm_attr_node.set("type", TYPES[sf.attrib["eType"]])

            print(etree.tostring(cdm_class_node))
            cdm_class_nodes.append(cdm_class_node)
            print()

    print(cdm_class_nodes)

    "".replace("xsitype", "xsi:type")  # Do this before returning result
    return '<?xml version="1.0" encoding="ASCII"?>\n' + ""  # whatever the result is
    # except Exception as e:
    #     print()
    #     return ""


def transform(files: List[str]):
    for fn in files:
        with open(fn) as f:
            cdm = ecore2cdm(f.read())
            #print(cdm)


if __name__ == "__main__":
    transform([IN])
