
import sys
import flet as ft
import string
from time import sleep

from lib_s_validate import *

return_value = 0
not_adjudicated = True
caught = False


class ButtonControl(ft.Text):
    def __init__(self, text):
        super().__init__()
        self.value = text
        # self.border = border.all(1, colors.BLACK54)
        # self.border_radius = 3
        # self.bgcolor = "0x09000000"

        self.size = 80
        self.weight = ft.FontWeight.W_100
        self.color = 0x0

        # self.visible = False



def main(page: ft.Page):

    # add/update controls on Page
    # pass
    page.title = "JAWWJ"
    background_color = page.bgcolor
    page.update()


    def close_adjudication(e):
        adjudication_modal.open = False
        page.update()



    adjudication_modal = ft.AlertDialog(
        # modal=True,

        title=ft.Text("The play is VALID",style=ft.TextThemeStyle.DISPLAY_MEDIUM),
        content=ft.Text(""),

        # actions=[ft.TextButton("OK", on_click=close_adjudication),],

        actions_alignment=ft.MainAxisAlignment.CENTER)

    c1 = ft.Container(
        expand=True, padding=50
    )

    # how_many_prompt: ft.TextField = ft.TextField(label="Enter number of words to challenge and press ENTER",
    # input_filter=ft.InputFilter(allow=True, regex_string="[1-8]"))
    def make_adjudicate(e):

        global not_adjudicated

        word_list = []
        for _ in range(words_to_adjudicate):
            word_list.append(words[_].value)

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        validate_message = ft.Text("The play is NOT VALID",text_align=ft.TextAlign.CENTER,color=ft.colors.BLACK,size=50, weight=ft.FontWeight.W_500)

        page.bgcolor = ft.colors.RED_500

        # page.theme = ft.theme.Theme(color_scheme_seed="red")

        if validate(word_list):
            validate_message = ft.Text("The play is VALID",text_align=ft.TextAlign.CENTER,color=ft.colors.BLACK,size=50, weight=ft.FontWeight.W_500)
            page.bgcolor = ft.colors.GREEN_500

        page.clean()
        page.vertical_alignment = "center"
        page.add(ft.Row([validate_message], alignment=ft.MainAxisAlignment.CENTER))
        words_checked = ft.Text("\n".join(word_list), text_align=ft.TextAlign.CENTER, color=ft.colors.WHITE, size=30)
        page.add(ft.Row([words_checked], alignment=ft.MainAxisAlignment.CENTER))

        # page.dialog = adjudication_modal
        # page.clean()
        page.scroll = None
        # page.add(c1)
        # page.dialog = adjudication_modal
        # adjudication_modal.open = True

        # while not adjudication_modal.open:
        #     page.dialog = adjudication_modal
        #     adjudication_modal.open = True
        #     page.update()

        page.update()
        timer = 8

        while timer:
            sleep(1)
            timer -= 1

        page.dialog = adjudication_modal
        adjudication_modal.open = False
        # page.controls.pop()
        page.update()
        not_adjudicated = False
        # page.clean()

        print(f'we are here {not_adjudicated} {adjudication_modal.open}(should be False)')


    def cancel_word_entry(e):
        global not_adjudicated
        not_adjudicated = False

    adjudicate_button: ft.ElevatedButtonButton = ft.ElevatedButton(text="ADJUDICATE", disabled=True,
                                                                    style=ft.ButtonStyle(bgcolor={
                                                                    ft.MaterialState.HOVERED: ft.colors.GREEN,
                                                                    ft.MaterialState.FOCUSED: ft.colors.GREEN,
                                                                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                                                    ft.MaterialState.DISABLED: ft.colors.GREY,
                                                                },
                                                                        color={ft.MaterialState.HOVERED: ft.colors.WHITE70,
                                                                               ft.MaterialState.FOCUSED: ft.colors.WHITE70,
                                                                               ft.MaterialState.DEFAULT: ft.colors.BLUE,
                                                                               ft.MaterialState.DISABLED: ft.colors.BLACK,

                                                                        }

                                                                   ), on_click=make_adjudicate)
    cancel_button: ft.ElevatedButton = ft.ElevatedButton(text="Cancel",
                                                         style=ft.ButtonStyle(bgcolor={
                                                             ft.MaterialState.HOVERED: ft.colors.RED_900,
                                                             ft.MaterialState.FOCUSED: ft.colors.RED_900,
                                                         },
                                                         color= {ft.MaterialState.HOVERED: ft.colors.WHITE70,
                                                             ft.MaterialState.FOCUSED: ft.colors.WHITE70,}
                                                         ), on_click=cancel_word_entry)

    def all_entered(e: ft.ControlEvent):  #turns on adjudicate if word is entered in all fields
        entries = []
        entries = [x.value for x in words]
        # for word in words:
        #     entries.append(word.value)
        print(entries)
        if all(x.value for x in words):
            adjudicate_button.disabled = False
        else:
            adjudicate_button.disabled = True
        page.update()

    def get_number():  # get number of words to adjudicate

        page.bgcolor = background_color
        global caught
        caught = False  # flag to see if we've already captured a number to adjudicate


        def on_number_press(e: ft.KeyboardEvent):

            global return_value, caught
            return_value = 0
            print("hello!")
            while pressed_box.visible:

                e.key = e.key[-1]
                if e.key in "12345678" and not caught:
                    pressed_box.value = e.key
                    pressed_box.visible = True
                    page.update()
                    caught = True # don't get two numbers
                    sleep(1)
                    pressed_box.visible = False
                    print(e.key)
                    return_value = int(e.key)

        how_many_prompt: ft.Text = ft.Text('Enter number of words to adjudicate', size=50, weight=ft.FontWeight.W_500)

        pressed_box = ButtonControl("")

        page.clean()
        page.on_keyboard_event = on_number_press
        page.vertical_alignment = "center"
        page.add(ft.Row([how_many_prompt], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Row([pressed_box], alignment=ft.MainAxisAlignment.CENTER))

        while return_value == 0:
            pass
        page.remove()

        ## instead of return, send this value to function to create grid of words
        return return_value


## start of code loop
    def on_esc_quit(e):
        global not_adjudicated

        print(e.key)
        if e.key == "Escape":
            not_adjudicated = False

    page.on_keyboard_event = on_esc_quit

    while True:
        global not_adjudicated
        adjudication_modal.open = False
        page.update()

        page.scroll = None
        words_to_adjudicate = get_number()

        # none
        
        page.clean()
        page.scroll = ft.ScrollMode.AUTO

        words = []

        page.add(ft.Row([ft.Text("CHALLENGER: Use TAB and SHIFT-TAB to move between boxes.\nOPPONENT: Highlight ADJUDICATE or CANCEL and press ENTER\n", size=25, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.START),)

        for _ in range(words_to_adjudicate):
            words.append(ft.TextField(label=f"Enter Word {_ + 1} to be Challenged",
                                      input_filter=ft.InputFilter(allow=True, regex_string="[a-zA-Z]"),
                                      capitalization=ft.TextCapitalization.CHARACTERS))
            page.add(words[_])
            words[_].on_change = all_entered # turns on validate if all words are entered

        page.add(ft.Row([adjudicate_button, cancel_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY))

        words[0].focus()

        not_adjudicated = True

        while not_adjudicated:
            # print("looping")
            pass


# get number of words
# get words -> adj or cancel
#


# ft.app(view=ft.AppView.WEB_BROWSER, assets_dir="assets", target=main)
ft.app(target=main, assets_dir="assets")