#!/usr/bin/env python3

import re
import os
from collections import OrderedDict
from lxml import etree
from typing import Dict, List


IN = "data/ideal.ecore"


# map ecore to cdm types
TYPES: Dict[str, str] = {
    "ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//EString": "//@types.6",
    "ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//EInt" : "//@types.4",
    "#//int": "//@types.4",
    "ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//EFloat": "//@types.8",
    "#//Time": "//@types.1",
    "#//Date": "//@types.1",
    "#//boolean": "//@types.2",
    "#//double": "//@types.3",
    "#//float": "//@types.8",
    "ecore:EDataType http://www.eclipse.org/emf/2002/Ecore#//EDouble": "//@types.3",
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


def get_class_by_name(classes: List[Class], name: str) -> Class:
    for c in classes:
        if c.name == name:
            return c
    print(f"WARNING: Class {name} not found.")


def get_class_layouts(n: int) -> str:
    a = [
        """      <value key="//@classes.0">
        <value x="668.4416" y="48.999725"/>
      </value>""","""
      <value key="//@classes.1">
        <value x="8.000122" y="205.08755"/>
      </value>""","""
      <value key="//@classes.2">
        <value x="423.50012" y="157.96127"/>
      </value>""","""
      <value key="//@classes.3">
        <value x="214.49994" y="517.9472"/>
      </value>""","""
      <value key="//@classes.4">
        <value x="689.4182" y="422.07367"/>
      </value>""","""
      <value key="//@classes.5">
        <value x="1073.9324" y="179.08759"/>
      </value>""","""
      <value key="//@classes.6">
        <value x="1040.4558" y="543.92755"/>
      </value>""","""
      <value key="//@classes.7">
        <value x="208.000122" y="405.08755"/>
      </value>""","""
      <value key="//@classes.8">
        <value x="623.50012" y="357.96127"/>
      </value>""","""
      <value key="//@classes.9">
        <value x="414.49994" y="717.9472"/>
      </value>""","""
      <value key="//@classes.10">
        <value x="889.4182" y="622.07367"/>
      </value>""","""
      <value key="//@classes.11">
        <value x="1273.9324" y="379.08759"/>
      </value>""","""
      <value key="//@classes.12">
        <value x="1240.4558" y="743.92755"/>
      </value>""","""
      <value key="//@classes.13">
        <value x="14.49994" y="317.9472"/>
      </value>""","""
      <value key="//@classes.14">
        <value x="489.4182" y="222.07367"/>
      </value>""","""
      <value key="//@classes.15">
        <value x="1073.9324" y="179.08759"/>
      </value>""","""
      <value key="//@classes.16">
        <value x="740.4558" y="243.92755"/>
      </value>""","""
      <value key="//@classes.17">
        <value x="58.000122" y="5.08755"/>
      </value>""","""
      <value key="//@classes.18">
        <value x="123.50012" y="57.96127"/>
      </value>"""
    ]

    result = """  <layout>
    <containers key="/">
      """

    for i in range(n):
        result += a[i]

    return result + """    </containers>
  </layout>"""


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
            if class_name not in class_names:
                class_names.append(class_name)
                classes.append(Class(class_name))
            
            #print(class_name)

            for sf in e:
                if "ecore:EReference" in sf.attrib.values():
                    other_class = sf.attrib["eType"].replace("#//", "")

                    if "eOpposite" in sf.attrib:
                        if "_" in sf.attrib["eOpposite"]:
                            print(f"WARNING: {sf.attrib['eOpposite']} contains underscores, which have been removed.")
                        assoc_name = sf.attrib["eOpposite"].replace("_", "").replace("#//", "").split("/")[1]
                    else:
                        assoc_name = aid  # to still have a unique id
                    
                    if f"{other_class}_{class_name}" in assoc_pairs and "eOpposite" in sf.attrib:
                        # if f"{other_class}_{class_name}" == "League_User":
                        #     print(f"Already processed {other_class}_{class_name}, so won't process {class_name}_{other_class}")
                        #     print(sf.attrib)
                            #exit()
                        # we already processed the association(s) in the other direction
                        continue

                    if "eOpposite" in sf.attrib:
                        # only track associations with an explicit other class (ignore those styled as attributes)
                        # if f"{class_name}_{other_class}" == "League_User":
                        #     print(f"Appending {class_name}_{other_class}")
                        assoc_pairs.append(f"{class_name}_{other_class}")

                    # Need to add classes here as well, since we might need a class ahead of its iteration order
                    # eg, if our classes are ABCD and A-D is an association, we will need to create class D at
                    # the time we are iterating at class A
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
                    #print(class1, class2)
                    class1.associations[f"{other_class}_{assoc_name}"] = assoc
                    class2.associations[f"{class_name}_{assoc_name}"] = assoc
                    associations.append(assoc)


    # print(classes)
    # [print(a) for a in associations]

    # print(get_class_by_name(classes, "User").associations)

    # exit(0)

    cdm_class_nodes = {}
    cdm_assoc_nodes = []

    # make classes with attributes and link associations to them
    for e in root:
        if "ecore:EClass" in e.attrib.values():
            cdm_class_node = etree.Element("classes", xsitype="classdiagram:Class", name=e.attrib["name"])
            clazz = get_class_by_name(classes, e.attrib["name"])
            
            i = 0
            for sf in e:
                if "ecore:EAttribute" in sf.attrib.values():
                    cdm_attr_node = etree.SubElement(cdm_class_node, "attributes")
                    cdm_attr_node.set("name", sf.attrib["name"])
                    cdm_attr_node.set("type", TYPES.get(sf.attrib.get("eType"), "//@types.2"))
                if "ecore:EReference" in sf.attrib.values():
                    cdm_assoc_node = etree.SubElement(cdm_class_node, "associationEnds")
                    cdm_assoc_node.set("name", sf.attrib["name"])
                    # print(sf.attrib)
                    # print(i, clazz.name, clazz.associations)
                    assoc = list(clazz.associations.values())[i]
                    cdm_assoc_node.set("assoc", f"//@associations.{assoc.aid}")
                    cdm_assoc_node.set("upperBound", "-1")  # TODO Handle multiplicities
                    i += 1

            #print(etree.tostring(cdm_class_node))
            cdm_class_nodes[e.attrib["name"]] = cdm_class_node
            #print()

    for a in associations:
        # print(a.classes[0], a.classes[0].associations)
        # print(a.classes[1], a.classes[1].associations)

        a_node = etree.Element("associations", name=f"{a.classes[0]}_{a.classes[1]}",
            ends=f"//@classes.{class_names.index(a.classes[0].name)}/"
                 f"@associationEnds.{list(a.classes[0].associations.values()).index(a)} "  # this space is intentional
                 f"//@classes.{class_names.index(a.classes[1].name)}/"
                 f"@associationEnds.{list(a.classes[1].associations.values()).index(a)}")
        cdm_assoc_nodes.append(a_node)
        #print(etree.tostring(a_node))

    result = ecore.split("<eClassifiers")[0]
    for c in class_names:
        result += etree.tostring(cdm_class_nodes[c]).decode("utf-8") + "\n"

    result += """
  <types xsi:type="classdiagram:CDVoid"/>
  <types xsi:type="classdiagram:CDAny"/>
  <types xsi:type="classdiagram:CDBoolean"/>
  <types xsi:type="classdiagram:CDDouble"/>
  <types xsi:type="classdiagram:CDInt"/>
  <types xsi:type="classdiagram:CDLong"/>
  <types xsi:type="classdiagram:CDString"/>
  <types xsi:type="classdiagram:CDByte"/>
  <types xsi:type="classdiagram:CDFloat"/>
  <types xsi:type="classdiagram:CDChar"/>
  """

    for c in cdm_assoc_nodes:
        result += etree.tostring(c).decode("utf-8") + "\n"

    result += get_class_layouts(len(class_names))

    result = result.replace("xsitype", "xsi:type")  # Do this before returning result
    return '<?xml version="1.0" encoding="ASCII"?>\n' + result + "\n</classdiagram:ClassDiagram>"
    # except Exception as e:
    #     print()
    #     return ""


def transform(files: List[str]):
    for fn in files:
        with open(fn) as f:
            cdm = ecore2cdm(f.read())
            with open("data/res2.cdm", "w") as g:
                g.write(cdm)


def transform2():
    global aid
    i = 0
    for filename in os.listdir("dataset/umple_files"):
        aid = 0
        if filename.endswith(".ecore"):
            try:
                with open(f"dataset/umple_files/{filename}") as f:
                    cdm = ecore2cdm(f.read())
                    with open(f"out/{i}.cdm", "w") as g:
                        print(f"{i}.cdm <- {filename}")
                        g.write(cdm)
                        i += 1
            except Exception as e:
                print(f"\nFailed to transform {filename}, with {type(e)}:\n{e}\n")


if __name__ == "__main__":
    #transform(["dataset/umple_files/assignment2.ecore"])
    transform2()
