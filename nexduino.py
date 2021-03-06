import time
import re
import pyperclip
import pyautogui

pyautogui.FAILSAFE = True

COMPONENT_TYPES = {
    "0": "NexWaveform",       # Waveform
    "1": "NexSlider",         # Slider
    "51": "NexTimer",         # Timer
    "52": "NexVariable",      # Variable
    "53": "NexDSButton",      # Dual / Dual-state Button
    "54": "NexNumber",        # Number
    "55": "NexScrolltext",    # Scrolling text
    "56": "NexCheckbox",      # Checkbox
    "57": "NexRadio",         # Radio
    "58": "QRCode",           # QRCode Not implemented in Nextion arduino lib
    "98": "NexButton",        # Button
    "106": "NexProgressBar",  # Progress bar
    "109": "NexHotspot",      # Touch Area / Hotspot
    "112": "NexPicture",      # Picture
    "113": "NexCrop",         # Crop
    "116": "NexText",         # Text
    "121": "NexPage",         # Page
    "122": "NexGauge"         # Gauge
}

COMPONENT_PREFIXES = {
    "NexWaveform": "wf",
    "NexSlider": "slider",
    "NexTimer": "tm",
    "NexVariable": "var",
    "NexDSButton": "dsbtn",
    "NexNumber": "num",
    "NexScrolltext": "stxt",
    "NexCheckbox": "cbox",
    "NexRadio": "radio",
    "QRCode": "qr",
    "NexButton": "btn",
    "NexProgressBar": "pbar",
    "NexHotspot": "hotspot",
    "NexPicture": "pic",
    "NexCrop": "crop",
    "NexText": "txt",
    "NexPage": "pg",
    "NexGauge": "gauge"
}

COORD_PAGE = (605, 175)
COORD_LIST_COMPONENTES = (670, 380)
COORD_OJBNAME_OR_TYPE_LABEL = (610, 430)
COORD_ID = (670, 405)
COORD_OJBNAME = (670, 430)
COORD_TYPE = (670, 450)
COORD_SCOPE = (670, 475)

OUTPUT_LOCAL = "{TYPE} {PREFIX}_{NAME} = {TYPE}({PG_ID}, {C_ID}, \"{NAME}\");"
OUTPUT_GLOBAL = "{TYPE} {PREFIX}_{NAME} = {TYPE}({PG_ID}, {C_ID}, \"{PG_NAME}.{NAME}\");"

re_default_names = re.compile(r"(page|t|g|n|b|j|p|q|m|z|s|h|tm|va|bt|c|r|qr)\d+")

time.sleep(2)


def reset_layout():
    """Resets the layout to default."""
    pyautogui.moveTo(110, 45)
    pyautogui.click()
    pyautogui.moveTo(140, 95, duration=0.15)
    pyautogui.click()


def home():
    """Selects first page"""
    pyautogui.moveTo(COORD_PAGE)
    pyautogui.click()
    
    # sends "up" key a lot of times to be sure it is on the first page
    pyautogui.typewrite(['up']*30)
    pyautogui.moveTo(COORD_LIST_COMPONENTES)
    pyautogui.click()
    pyautogui.typewrite(['home'])
    pyautogui.typewrite(['enter'])


def set_up(janela: pyautogui.Window):
    """Initial configuration"""
    janela.maximize()
    janela.resizeTo(800, 600)
    janela.moveTo(0, 0)
    janela.focus()
    reset_layout()
    home()


def next_component():
    """Goes to the next component."""
    pyautogui.moveTo(COORD_LIST_COMPONENTES)
    pyautogui.click()

    # moves so that the cursor isn't slecting hovering a component name
    pyautogui.moveTo(20, 20)

    pyautogui.typewrite(['right', 'enter'])
    time.sleep(0.1)


def some_component_selected():
    """Returns True if there is a component selected,
    returns False otherwise."""
    pyperclip.copy('')
    pyautogui.moveTo(COORD_OJBNAME_OR_TYPE_LABEL, duration=0.15)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'c')
    return True if pyperclip.paste() in ['type', 'objname'] else False


def get_id():
    """
    Returns the ID of the selected component.
    Returns empty string if there is not component selected.
    """
    pyperclip.copy('')
    pyautogui.moveTo(COORD_ID)
    pyautogui.doubleClick()
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def get_name():
    """
    Returns object name of the selected.
    Returns empty string if there is not component selected.
    If the selected component is a page it return its type number (121).
    """
    pyperclip.copy('')
    pyautogui.moveTo(COORD_OJBNAME)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def get_type():
    """
    Returns the number of the type.
    Returns empty string if there is not component selected.
    """
    pyperclip.copy('')
    pyautogui.moveTo(COORD_TYPE)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def get_scope():
    """
    Returns the scope of the component as a string.
    Returns empty string if there is not component selected.
    """
    pyperclip.copy('')
    pyautogui.moveTo(COORD_SCOPE)
    pyautogui.click()
    pyautogui.typewrite(['enter'])
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def page_name(pg_number):
    """Goes to page of number pg_number and returns the name of the page."""
    posicao_rename = 7

    # navigates to n-th page
    pyautogui.moveTo(COORD_PAGE)
    pyautogui.click()
    pyautogui.typewrite(['down']*pg_number)

    # opens contextual menu and select rename
    time.sleep(0.2)
    pyautogui.hotkey('shift', 'f10')
    time.sleep(0.2)
    pyautogui.typewrite(['down']*posicao_rename)

    # selects, copies and returns page name
    pyautogui.typewrite(['enter'])
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.typewrite(['enter'])
    return pyperclip.paste()


def output(c_name, pg_name, page_id):
    """Returns the delcaration string for the current component"""
    if c_name == '121':
        c_id = "0"
        component_type = COMPONENT_TYPES['121']
        prefix = COMPONENT_PREFIXES[component_type]
        return (OUTPUT_LOCAL.format(TYPE=component_type,
                                  PREFIX=prefix, NAME=pg_name,
                                  PG_ID=page_id, C_ID=c_id))
    else:
        c_id = get_id()
        component_type = COMPONENT_TYPES[get_type()]
        prefix = COMPONENT_PREFIXES[component_type]
        scope = get_scope()
        if scope == "local":
            return OUTPUT_LOCAL.format(TYPE=component_type,
                                       PREFIX=prefix, NAME=c_name,
                                       PG_ID=page_id, C_ID=c_id)
        elif scope == "global":
            return OUTPUT_GLOBAL.format(TYPE=component_type,
                                        PREFIX=prefix, NAME=c_name,
                                        PG_ID=page_id, C_ID=c_id,
                                        PG_NAME=pg_name)


def _main(first_page_id, last_page_id):
    """Lists the delcaration for each component in the page range"""
    for page_id in range(first_page_id, last_page_id+1):
        pg_name = page_name(page_id)
        print("\n/**\n * components for page {}\n */".format(pg_name))
        while some_component_selected():
            c_name = get_name()
            if not re_default_names.match(c_name) and not c_name.startswith('_'):
                print(output(c_name, pg_name, page_id))
            next_component()

if __name__ == '__main__':
    nextion = pyautogui.getWindowsWithTitle("Nextion Editor")[0]

    if not nextion:
        raise Exception("Nextion Windows not found!")
    set_up(nextion)
    time.sleep(1.2)  # to make sure that it won't be a double click
    _main(0, 5)
