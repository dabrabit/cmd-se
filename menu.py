import json
from os import getcwd as directory
from tkinter import Tk
from tkinter import messagebox as msg
from tkinter import simpledialog as dialog
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile

from ExpertSystems import ExpertSystem

# ======================== FUNCIONES ===========================
base = {}
status = False
newBase = False
filename = './bases/default.json'
rejectedAtributeName = []
rejectedAtributeCount = 0


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
                attributes = dialog.askstring("Atributos", f"Ingrese los atributos para {object}"
                                                           f" separados por una coma y sin espacios.\n(Ej. a,b,c):")

                # Read advice
                advice = dialog.askstring("Recomendacion",
                                          "Ingrese la recomendación.\n(Ej. Ver los procesos activos.):")

                attributes = attributes.split(",")  # Attributes in array

                knowledgeBase[object] = {'attrs': attributes, 'advice': advice}  # Adding attributes to object

            else:
                msg.showwarning("Objeto existente", f"El objeto {object} ya existe en la base de conocimientos.")

        return knowledgeBase


def consultSE(knowledgeBase):
    if len(knowledgeBase) == 0:
        msg.showerror("Base de conocimientos vacia", "La base de conocimientos no contiene ningun dato.")
        return
    global rejectedAtributeName, rejectedAtributeCount
    rejectedAtributeName.clear()
    objects = [*knowledgeBase]  # Obtains keys from knowledge base (los comandos)

    wasResultFound = False  # Found some result flag
    result = objects[0]  # We assume that the result is the first object
    myES = ExpertSystem(knowledgeBase)  # Creating expert system

    msg.showinfo("Consultar", "Para encontrar su comando, responda S o N a las siguientes preguntas:")

    # Iterate while there's objects and there isn't a result
    wasCanceled = False
    while objects and not wasResultFound:
        currentObject = objects.pop(0)  # We get the head object
        # If object has rejected attributes or doesn't have required attributes, ignore it
        if myES.hasCertainTypeOfAttributes(currentObject, False) or not myES.hasCertainTypeOfAttributes(currentObject,
                                                                                                        True):
            continue

        rejectedAttributeFound = False
        currentObjectAttributes = myES.getObjectAttributes(currentObject).copy()
        numberOfAttributesInObject = len(currentObjectAttributes)
        acceptedAttributes = 0

        # Validate attributes while there are left and there hasn't been a rejected
        # attribute and there hasn't been a result found
        if wasCanceled is False:
            while currentObjectAttributes and not rejectedAttributeFound and not wasResultFound:
                attr = currentObjectAttributes.pop(0)  # Get an attribute

                # Check if already asked this attribute
                if myES.wasAttributeAskedFor(attr):  # If true add a check
                    acceptedAttributes += 1
                else:  # If false then ask for it
                    response = dialog.askstring("Responda S/N", f"Experto: ¿Maneja {attr}?")

                    # Add asked attribute and its value
                    if response is not None:
                        response = response.upper()
                        myES.setAskedAttribute(attr, response == "S")

                        if response == "S":  # If the object has it then make a check
                            acceptedAttributes += 1
                        else:  # If the object doesn't have it then reject it
                            rejectedAtributeName.append("\n\t*" + attr)
                            rejectedAtributeCount += 1
                            rejectedAttributeFound = True

                        # If already found a result then save it
                        if acceptedAttributes == numberOfAttributesInObject:
                            result = currentObject
                            wasResultFound = True
                    else:
                        wasCanceled = True
                        break
        else:
            break

    return result if wasResultFound else None


# ======================== FUNCIONES ===========================

def retriveKnowledgeBaseState():
    return status


def menu(master, option):
    option = int(option)
    global base, status, newBase, filename, rejectedAtributeName, rejectedAtributeCount

    expertSystem = ExpertSystem({})

    """
        1. Introducir objetos a la BC
        2. Consultar al SE
        3. Guardar la BC
        4. Usar una BC existente
        5. Salir
    """

    if option == 1:
        # Introducir objetos a la BC
        if status is not True:
            question = msg.askyesno("Base de datos no cargada", "No has cargado ninguna base de conocimientos aún,"
                                                                " todos los datos introducidos se irán a una nueva base"
                                                                " de conocimientos, ¿Desea continuar?")
            if question:
                base = addObjectsToKnowledgeBase(base)
                status = True
                newBase = True

    elif option == 2:
        # Consultar base de conocimientos.
        if status is not True:
            with open(filename, 'r') as selectedBase:
                base = json.load(selectedBase)
            msg.showwarning("Base de datos por defecto cargada",
                            "No has cargado ninguna base de conocimientos, pero no te preocupes, "
                            "Hemos cargado el archivo por defecto para que puedas realizar tus consultas.")
            status = True

        resultingObject = consultSE(base)

        if resultingObject is not None:
            msg.showinfo("Se ejecuto exitosamente",
                         "=======================================\n"
                         + f"El comando resultante es: {resultingObject}"
                         + "\n=======================================")
            tmp = ""
            for el in base[resultingObject]['attrs']:
                tmp += "\t*" + el + "\n"
            msg.showinfo("Se ejecuto exitosamente",
                         "=======================================\n"
                         + f"La lista de atributos del comando son:\n{tmp}"
                         + "\n=======================================")
            msg.showinfo("Se ejecuto exitosamente",
                         "=======================================\n"
                         + f"La funcionalidad del comando es la siguiente:\n{base[resultingObject]['advice']}"
                         + "\n=======================================")
        else:
            rejectedAtributeName = list(set(rejectedAtributeName))
            msg.showerror("Objeto no encontrado",
                          "=======================================\n"
                          + f"No se encontró el comando dado que"
                          + format(''.join(rejectedAtributeName))
                          + "\nno " + f"{'fue válido' if rejectedAtributeCount == 0 else 'fueron válidos'}."
                          + "\n=======================================")

    elif option == 3:
        # Guardar base de conocimientos.
        if status is not True or newBase:
            files = [('JSON File', '*.json')]
            filename = asksaveasfile(initialdir=directory() + "\\bases\\", filetypes=files, defaultextension=files)
            if filename is None:
                msg.showwarning("No se guardaron los cambios", "Se canceló el guardado.")
                filename = './bases/default.json'
            else:
                newBase = False
                filename = filename.name
                with open(filename, 'w') as outfile:
                    json.dump(base, outfile)
                msg.showinfo("Guardado correcto",
                             "=======================================\n"
                             + "Base de conocimientos guardada correctamente."
                             + "\n=======================================")

    elif option == 4:
        # Cargar base de conocimientos.
        filename = askopenfilename()

        Tk().withdraw()
        if len(filename) > 0:
            name = filename.split("/")
            with open(filename, 'r') as selectedBase:
                base = json.load(selectedBase)
            status = True
            msg.showinfo("Carga exitosa", f"Se ha cargado correctamente la base de conocimiento {name[-1]}.")
        else:
            filename = './bases/default.json'
