import json
from ExpertSystems import ExpertSystem
from tkinter import simpledialog as dialog
from tkinter import messagebox as msg
from tkinter import Tk


# ======================== FUNCIONES ===========================
base = {}

def addObjectsToKnowledgeBase(knowledgeBase):
    # Ask for objects
    objects = dialog.askstring("Crear base de conocimiento",
                               "Ingrese los comandos separados por una coma y sin espacios. (Ej. a,b,c):")
    if objects is not None:
        objects = objects.split(",")  # Objects in array

        # Add attributes to objects
        for object in objects:
            if object not in knowledgeBase:
                # Read attributes
                attributes = dialog.askstring("Atributos", "Ingrese los atributos para " + object +
                                          " separados por una coma y sin espacios.\n(Ej. a,b,c):")

                # Read advice
                advice = dialog.askstring("Recomendacion", "Ingrese la recomendación.\n(Ej. Ver los procesos activos.):")

                attributes = attributes.split(",")  # Attributes in array

                knowledgeBase[object] = {'attrs': attributes, 'advice': advice}  # Adding attributes to object

            else:
                msg.showwarning("Objeto existente", "El objeto " + object + " ya existe en la base de conocimientos.")

        return knowledgeBase


def consultSE(knowledgeBase):
    objects = [*knowledgeBase]  # Obtains keys from knowledge base (los comandos)

    wasResultFound = False  # Found some result flag
    result = objects[0]  # We assume that the result is the first object
    myES = ExpertSystem(knowledgeBase)  # Creating expert system

    msg.showinfo("Para encontrar su comando, responda S o N a las siguientes preguntas:")

    # Iterate while there's objects and there isn't a result
    while objects and not wasResultFound:
        currentObject = objects.pop(0) # We get the head object

        # If object has rejected attributes or doesn't have required attributes, ignore it
        if myES.hasCertainTypeOfAttributes(currentObject, False) or not myES.hasCertainTypeOfAttributes(currentObject, True):
            continue

        rejectedAttributeFound = False
        currentObjectAttributes = myES.getObjectAttributes(currentObject).copy()
        numberOfAttributesInObject = len(currentObjectAttributes)
        acceptedAttributes = 0

        # Validate attributes while there are left and there hasn't been a rejected
        # attribute and there hasn't been a result found
        while currentObjectAttributes and not rejectedAttributeFound and not wasResultFound:
            attr = currentObjectAttributes.pop(0) # Get an attribute

            # Check if already asked this attribute
            if myES.wasAttributeAskedFor(attr): # If true add a check
                acceptedAttributes += 1
            else: # If false then ask for it
                response = dialog.askstring("Responda S/N", "Experto: ¿Maneja " + attr + "?")

                # Add asked attribute and its value
                myES.setAskedAttribute(attr, response == "S")

                if response == "S": # If the object has it then make a check
                    acceptedAttributes += 1
                else: # If the object doesn't have it then reject it
                    rejectedAttributeFound = True

            # If already found a result then save it
            if acceptedAttributes == numberOfAttributesInObject:
                result = currentObject
                wasResultFound = True

    return result if wasResultFound else None


# ======================== FUNCIONES ===========================


def menu(master, option):
    option = int(option)
    global base
    print(base)
    expertSystem = ExpertSystem({})

    """
        1. Introducir objetos a la BC
        2. Consultar al SE
        3. Guardar la BC
        4. Usar una BC existente
        5. Salir
    """
    print("Opcion " + str(option))

    if option == 1:
        addObjectsToKnowledgeBase(base)

    elif option == 2:
        resultingObject = consultSE(base)
        print("Si inicio")

        msg.showinfo("Se ejecuto exitosamente",
                     "============================================\n"
                     + "El comando resultante es: " + resultingObject
                     + "\n============================================")

    elif option == 3:
        # Base de conocimientos guardada.
        with open('./bases/default.json', 'w') as outfile:
            json.dump(base, outfile)

    elif option == 4:
        # Base de conocimientos cargada.
        with open('./bases/default.json', 'r') as selectedBase:
            base = json.load(selectedBase)
        Tk().withdraw()
        msg.showinfo("Carga exitosa", "Se ha cargado correctamente la base de conocimiento")
