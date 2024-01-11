import os
import sys
import io
import pygetwindow as gw
from pywinauto import Application
from pynput import mouse

def enumerate_subtree(control, indent=0):
    """Recursively print the control and all its descendants."""
    print(" " * indent + str(control))
    for child in control.children():
        enumerate_subtree(child, indent + 2)

def write_control_identifiers(window: any, windowtitle: str):
    # Redirect the output to a string buffer

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    # Print control identifiers to the buffer
    window.print_control_identifiers()
    # Reset standard output
    sys.stdout = old_stdout

    # Get the string from the buffer
    output = buffer.getvalue()

    #sanitize the window title
    windowtitle = windowtitle.replace(" ", "_")
    windowtitle = windowtitle.replace(":", "_")
    windowtitle = windowtitle.replace("\\", "_")
    windowtitle = windowtitle.replace("/", "_")
    windowtitle = windowtitle.replace("*", "_")
    windowtitle = windowtitle.replace("?", "_")
    windowtitle = windowtitle.replace("\"", "_")
    windowtitle = windowtitle.replace("<", "_")
    windowtitle = windowtitle.replace(">", "_")
    windowtitle = windowtitle.replace("|", "_")

    # Write the output to a file creating a new folder if necessary
    if not os.path.exists(os.path.join(os.getcwd(),"output")):
        os.makedirs(os.path.join(os.getcwd(),"output"))
    outputfile = os.path.join(os.getcwd(),"output", f"file_{windowtitle}.txt")
    print(f"Writing output to {outputfile}")
    with open(outputfile, "w", encoding='utf-8') as f:
        f.write(output)

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        # quitte le programme si le bouton droit de la souris est cliqué
        if button == mouse.Button.right:
            print("Vous avez cliqué sur le bouton droit de la souris.")
            return False
        # Trouve la fenêtre à cette position
        window = gw.getWindowsAt(x, y)
        # Vérifie si une fenêtre a été trouvée
        if window:
            selected_window = window[0]
            print("Vous avez sélectionné la fenêtre : " + selected_window.title)
            try:
                app = Application().connect(title=selected_window.title)
                window = app.window(title=selected_window.title)
                write_control_identifiers(window, selected_window.title)

                for i, child in enumerate(window.children()):
                    if child.is_visible():
                        if child.friendly_class_name() == "Edit" or child.friendly_class_name() == "Static":
                            print(f"Child {i}: {child.friendly_class_name()} - {child.window_text()}")
                        elif child.friendly_class_name() == "ComboBox" or child.friendly_class_name() == "Button":
                            print(f"Child {i}: {child.friendly_class_name()} - {child.texts()}")
                        else:
                            print(f"Child {i}: {child.friendly_class_name()} - {child.window_text()}")

            except Exception as e:
                print("Une exception s'est produite : " + str(e))
                print("Exception passed.")
                pass
        else:
            print("Aucune fenêtre n'a été trouvée à cette position.")


# Création d'un "listener" qui appelle la fonction on_click à chaque clic de souris
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
