from ExpertSystems import ExpertSystem
import json

# ======================== FUNCIONES ===========================
def addObjectsToKnowledgeBase(knowledgeBase):
    # Ask for objects
    print("Ingrese los comandos separados por una coma y sin espacios. (Ej. a,b,c):")
    objects = input()
    objects = objects.split(",") # Objects in array

    print("") # Format

    # Add attributes to objects
    for object in objects:
        if object not in knowledgeBase:
            # Read attributes
            print("Ingrese los atributos para " + object + " separados por una coma y sin espacios.")
            print("(Ej. a,b,c):")
            attributes = input()
            print("") # Format

            # Read advice
            print("Ingrese la recomendación.")
            print("(Ej. Ver los procesos activos.):")
            advice = input()
            print("") # Format

            attributes = attributes.split(",") # Attributes in array

            knowledgeBase[object] = {'attrs': attributes, 'advice': advice} # Adding attributes to object

        else:
            print("El objeto " + object + " ya existe en la base de conocimientos.")

    return knowledgeBase

def consultSE(knowledgeBase):
    objects = [*knowledgeBase] # Obtains keys from knowledge base (los comandos)

    wasResultFound = False # Found some result flag
    result = objects[0] # We assume that the result is the first object
    myES = ExpertSystem(knowledgeBase) # Creating expert system

    print("Para encontrar su comando, responda S o N a las siguientes preguntas:")
    print()

    # Iterate while there's objects and there isn't a result
    while objects and not wasResultFound:
        currentObject = objects.pop(0) # We get the head object

        # If object has rejected attributes or doesn't have required attributes, ignore it
        if myES.hasCertainTypeOfAttributes(currentObject, False) or not myES.hasCertainTypeOfAttributes(currentObject, True):
            continue

        rejectedAttributeFound = False
        currentObjectAttributes = myES.getObjectAttributes(currentObject)
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
                print("Experto: ¿Maneja " + attr + "?")
                response = input()

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


option = 0
base = {}
expertSystem = ExpertSystem({})

while option != "5":

    print("")
    print("+---------------------------------------------------+")
    print("| Sistemas Expertos                                 |")
    print("|===================================================|")
    print("| Selecciona una opción para continuar...           |")
    print("|                                                   |")
    print("| 1. Introducir objetos a la BC                     |")
    print("| 2. Consultar al SE                                |")
    print("| 3. Guardar la BC                                  |")
    print("| 4. Usar una BC existente                          |")
    print("| 5. Salir                                          |")
    print("+---------------------------------------------------+")
    print("")

    option = input()

    if option == "1":
        print("")
        # Esta función tiene prints adentro, así que sería bueno que los tomes en cuenta para
        # la interfaz
        addObjectsToKnowledgeBase(base)

    elif option == "2":
        print("")
        # Esta función tiene prints adentro, así que sería bueno que los tomes en cuenta para
        # la interfaz
        # resultingObject guarda el resultado si encuentra uno, si no, regresa None
        resultingObject = consultSE(base)

        print("")

        if resultingObject != None:
            print("==============================================")
            print("El comando resultante es: " + resultingObject)
            print("==============================================")
        else:
            print("==============================================")
            print("No se encontraron comandos con esa descripción")
            print("==============================================")

    elif option == "3":
        print("")
        with open('./bases/default.json', 'w') as outfile:
            json.dump(base, outfile)
        
        print("Base de conocimientos guardada.")

    elif option == "4":
        print("")
        with open('./bases/default.json', 'r') as selectedBase:
            base = json.load(selectedBase)

        print("Base de conocimientos cargada.")

    elif option == "5":
        print("")
    else:
        # Este no es necesario ponerlo en la GUI
        print("")
        print("La opción introducida no es válida")
