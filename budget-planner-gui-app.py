from infrastructure.Budget import Budget
from infrastructure.Record import Record
import PySimpleGUI as sg
import pickle

STORAGE_ADDRESS = r"D:\005_Python_Courses\budget-planner-gui\resources\storage.pkl"


def application_load():
    try:
        with open(STORAGE_ADDRESS, "rb") as file:
            budgets_dict = pickle.load(file)
    except (EOFError, FileNotFoundError):
        budgets_dict = {
            'Jan-23': Budget('Jan-23'),
            'Feb-23': Budget('Feb-23'),
            'Mar-23': Budget('Mar-23'),
            'Apr-23': Budget('Apr-23'),
            'May-23': Budget('May-23'),
            'Jun-23': Budget('Jun-23'),
            'Jul-23': Budget('Jul-23'),
            'Aug-23': Budget('Aug-23'),
            'Sep-23': Budget('Sep-23'),
            'Oct-23': Budget('Oct-23'),
            'Nov-23': Budget('Nov-23'),
            'Dec-23': Budget('Dec-23'),
        }
    return budgets_dict


def application_save(obj):
    with open(STORAGE_ADDRESS, "wb") as file:
        pickle.dump(obj, file)


def add_method(item, record, type):
    if type == "Budget":
        item.add_income(record)
    elif type == "Wishes":
        item.add_wish_expenses(record)
    elif type == "Expenses":
        item.add_expense(record)
    elif type == "Savings":
        item.add_saving(record)


def refresh_input_fields(window):
    window['-Copy to-'].update(value="")
    window['-Id-'].update(value="")
    window['-Edit Title-'].update(value="")
    window['-Edit Value-'].update(value="")
    window['-Edit Description-'].update(value="")
    window['-Add Title-'].update(value="")
    window['-Add Value-'].update(value="")
    window['-Add Description-'].update(value="")


def event_handling(window, event, values, budgets_dict):
    if event == 'Save':
        application_save(budgets_dict)
    elif event in budgets_dict.keys():
        values['-DETAILS-'] = "Budget"
        item = budgets_dict[event]
        refresh_headers(item, window)
        window['-DETAILS-'].update(values=item.show_budget())
        window['-Text Details-'].update(value=f"Budget {item.title}")

        while True:
            sub_event, sub_values = window.read()
            if sub_event == 'Save':
                application_save(budgets_dict)

            elif sub_event in budgets_dict.keys():
                event_handling(window, sub_event, sub_values, budgets_dict)

            elif sub_event == sg.WIN_CLOSED or sub_event == 'Cancel':
                exit()

            elif sub_event == "Budget":
                values['-DETAILS-'] = sub_event
                try:
                    window['-DETAILS-'].update(values=item.show_budget())
                    window['-Text Details-'].update(value=f"{sub_event} {item.title}")
                except UnboundLocalError:
                    sg.popup("Noting to display!")

            elif sub_event == "Wishes":
                values['-DETAILS-'] = sub_event
                try:
                    window['-DETAILS-'].update(values=item.show_wishes())
                    window['-Text Details-'].update(value=f"{sub_event} {item.title}")
                except UnboundLocalError:
                    sg.popup("Noting to display!")

            elif sub_event == "Expenses":
                values['-DETAILS-'] = sub_event
                try:
                    window['-DETAILS-'].update(values=item.show_expenses())
                    window['-Text Details-'].update(value=f"{sub_event} {item.title}")
                except UnboundLocalError:
                    sg.popup("Noting to display!")

            elif sub_event == "Savings":
                values['-DETAILS-'] = sub_event
                try:
                    window['-DETAILS-'].update(values=item.show_savings())
                    window['-Text Details-'].update(value=f"{sub_event} {item.title}")
                except UnboundLocalError:
                    sg.popup("Noting to display!")

            elif sub_event == "Add Income":
                try:
                    record = Record(sub_values['-Add Title-'],
                                    float(sub_values['-Add Value-']),
                                    sub_values['-Add Description-'])
                    add_method(item, record, "Budget")
                    refresh_headers(item, window)
                    refresh_input_fields(window)
                    values['-DETAILS-'] = "Budget"
                    window['-Text Details-'].update(value=f"Budget {item.title}")
                    window['-DETAILS-'].update(values=item.show_budget())
                except ValueError:
                    sg.popup("Insert valid value!", any_key_closes=True)

            elif sub_event == "Add Expense":
                try:
                    record = Record(sub_values['-Add Title-'],
                                    float(sub_values['-Add Value-']),
                                    sub_values['-Add Description-'])
                    add_method(item, record, "Expenses")
                    refresh_headers(item, window)
                    refresh_input_fields(window)
                    values['-DETAILS-'] = "Expenses"
                    window['-Text Details-'].update(value=f"Expenses {item.title}")
                    window['-DETAILS-'].update(values=item.show_expenses())
                except ValueError:
                    sg.popup("Insert valid value!", any_key_closes=True)

            elif sub_event == "Add Wish":
                try:
                    record = Record(sub_values['-Add Title-'],
                                    float(sub_values['-Add Value-']),
                                    sub_values['-Add Description-'])
                    add_method(item, record, "Wishes")
                    refresh_headers(item, window)
                    refresh_input_fields(window)
                    values['-DETAILS-'] = "Wishes"
                    window['-Text Details-'].update(value=f"Wishes {item.title}")
                    window['-DETAILS-'].update(values=item.show_wishes())
                except ValueError:
                    sg.popup("Insert valid value!", any_key_closes=True)
            elif sub_event == "Add Saving":
                try:
                    record = Record(sub_values['-Add Title-'],
                                    float(sub_values['-Add Value-']),
                                    sub_values['-Add Description-'])
                    add_method(item, record, "Savings")
                    refresh_headers(item, window)
                    refresh_input_fields(window)
                    values['-DETAILS-'] = "Savings"
                    window['-Text Details-'].update(value=f"Savings {item.title}")
                    window['-DETAILS-'].update(values=item.show_savings())
                except ValueError:
                    sg.popup("Insert valid value!", any_key_closes=True)

            elif sub_event == "-DETAILS-":
                fill_edit_fields(sub_values, window)

            elif sub_event == "Edit Entry":
                try:
                    type = values['-DETAILS-']
                    record = Record(sub_values['-Edit Title-'],
                                    float(sub_values['-Edit Value-']),
                                    sub_values['-Edit Description-'])
                    id = int(sub_values['-Id-'])
                    edit_method(item, id, record, type, window)
                    refresh_headers(item, window)
                    refresh_input_fields(window)
                except (ValueError):
                    sg.popup("Insert valid value!", any_key_closes=True)

            elif sub_event == "Delete Entry":
                try:
                    type = values['-DETAILS-']
                    id = int(sub_values['-Id-'])
                    delete_method(item, id, type, window)
                    refresh_headers(item, window)
                    refresh_input_fields(window)
                except (ValueError):
                    sg.popup("Insert valid value!", any_key_closes=True)

            elif sub_event == "Copy Entry to":
                try:
                    type = values['-DETAILS-']
                    month = sub_values['-Copy to-']
                    if month in budgets_dict.keys():
                        item_to_copy = budgets_dict[month]
                        record = Record(sub_values['-Edit Title-'],
                                        float(sub_values['-Edit Value-']),
                                        sub_values['-Edit Description-'])
                        add_method(item_to_copy, record, type)
                        refresh_input_fields(window)
                        refresh_headers(item, window)
                    else:
                        raise ValueError("Data provided not a month")
                except (ValueError):
                    sg.popup("Insert valid value!", any_key_closes=True)

            elif sub_event == "-50-":
                item.savings_percentage = 0.2
                item.expences_percentage = 0.5
                item.wish_percentage = 0.3
                refresh_headers(item, window)

            elif sub_event == "-40-":
                item.savings_percentage = 0.3
                item.expences_percentage = 0.4
                item.wish_percentage = 0.3
                refresh_headers(item, window)

            elif sub_event == "-30-":
                item.savings_percentage = 0.4
                item.expences_percentage = 0.3
                item.wish_percentage = 0.3
                refresh_headers(item, window)


def delete_method(item, id, type, window):
    try:
        if type == "Budget":
            item.delete_income(id=id)
            window['-DETAILS-'].update(values=item.show_budget())
        elif type == "Wishes":
            item.delete_wish(id=id)
            window['-DETAILS-'].update(values=item.show_wishes())
        elif type == "Expenses":
            item.delete_expense(id=id)
            window['-DETAILS-'].update(values=item.show_expenses())
        elif type == "Savings":
            item.delete_saving(id=id)
            window['-DETAILS-'].update(values=item.show_savings())
    except (ValueError, KeyError):
        sg.popup("Insert valid value!", any_key_closes=True)


def edit_method(item, id, record, type, window):
    if type == "Budget":
        item.edit_income(id=id, record=record)
        window['-DETAILS-'].update(values=item.show_budget())
    elif type == "Wishes":
        item.edit_wish_expense(id=id, record=record)
        window['-DETAILS-'].update(values=item.show_wishes())
    elif type == "Expenses":
        item.edit_expense(id=id, record=record)
        window['-DETAILS-'].update(values=item.show_expenses())
    elif type == "Savings":
        item.edit_saving(id=id, record=record)
        window['-DETAILS-'].update(values=item.show_savings())


def fill_edit_fields(sub_values, window):
    try:
        body = sub_values['-DETAILS-'][0]
        val_list = body.split(';')
        record_id = body.split('.')[0]
        record_title = val_list[0].split(':')[1].strip()
        record_value = val_list[1].split(':')[1].strip()
        record_description = val_list[2].split(':')[1].strip()
    except (IndexError, AttributeError):
        record_description = record_id = record_value = record_title = ""
    window['-Add Title-'].update(value=record_title)
    window['-Edit Title-'].update(value=record_title)
    window['-Add Value-'].update(value=record_value)
    window['-Edit Value-'].update(value=record_value)
    window['-Add Description-'].update(value=record_description)
    window['-Edit Description-'].update(value=record_description)
    window['-Id-'].update(value=record_id)


def refresh_headers(item, window):
    recommanded_wishes = round((item.total_income) * (item.wish_percentage), 2)
    recommanded_expences = round((item.total_income) * (item.expences_percentage), 2)
    recommanded_savings = round((item.total_income) * (item.savings_percentage), 2)
    try:
        wishes_usage = round((item.total_wish_expense / recommanded_wishes) * 100, 2)
        expenses_usage = round((item.total_expenses / recommanded_expences) * 100, 2)
        savings_usage = round((item.total_savings / recommanded_savings) * 100, 2)
    except ZeroDivisionError:
        wishes_usage = 0
        expenses_usage = 0
        savings_usage = 0

    wishes_text = f"Recommended budget: {recommanded_wishes} RON\n\n" \
                  f"Total spent: {item.total_wish_expense} RON\n" \
                  f"Percentage: {wishes_usage} %"
    expenses_text = f"Recommended budget: {recommanded_expences} RON\n\n" \
                    f"Total spent: {item.total_expenses} RON\n" \
                    f"Percentage: {expenses_usage} %"
    savings_text = f"Recommended budget: {recommanded_savings} RON\n\n" \
                   f"Total spent: {item.total_savings} RON\n" \
                   f"Percentage: {savings_usage} %"
    window['-BUDGET-'].update(value=f"Total income {item.total_income} RON\n")
    window['-WISHES-'].update(value=wishes_text)
    window['-EXPENSES-'].update(value=expenses_text)
    window['-SAVINGS-'].update(value=savings_text)


def run_gui(budgets_dict):
    layout = create_layout()
    sg.theme('DarkTeal11')
    window = sg.Window('Budget planner',
                       layout,
                       finalize=True,
                       size=(1100, 620))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event not in budgets_dict.keys() and event != "Save":
            sg.popup("Please Select a month first!", any_key_closes=True)
        event_handling(window, event, values, budgets_dict)
    window.close()


def create_layout():
    top_left_column = [
        [sg.Text('2023 Calendar', justification="center")],
        [sg.Button(f'{key}', size=(15, 1), ) for key in list(budgets_dict.keys())[:3]],
        [sg.Button(f'{key}', size=(15, 1), ) for key in list(budgets_dict.keys())[3:6]],
        [sg.Button(f'{key}', size=(15, 1), ) for key in list(budgets_dict.keys())[6:9]],
        [sg.Button(f'{key}', size=(15, 1), ) for key in list(budgets_dict.keys())[9:]],
        [sg.Text('Metoda de repartitie a bugetului', justification="center")],
        [sg.Radio("50% expenses, 30% wishes, 20 savings", "monkey",
                  default=True, enable_events=True, key='-50-'), ],
        [sg.Radio("40% expenses, 30% wishes, 30 savings", "monkey",
                  enable_events=True, key='-40-'), ],
        [sg.Radio("30% expenses, 30% wishes, 40 savings", "monkey",
                  enable_events=True, key='-30-'), ],
    ]
    bottom_left_column = [
        [sg.Text("Add Entry")],
        [sg.Text("Title"),
         sg.In(size=(30, 1), enable_events=True, key="-Add Title-"),
         sg.Text("Value"),
         sg.In(size=(10, 1), enable_events=True, key="-Add Value-"),
         ],
        [sg.Text("Description"),
         sg.In(size=(30, 15), enable_events=True, key="-Add Description-"),
         ],
        [sg.Button('Add Income'), sg.Button('Add Expense'), sg.Button('Add Wish'), sg.Button('Add Saving')],
        [sg.Text("Edit / Delete / Copy Entry")],
        [sg.Text("Title"),
         sg.In(size=(30, 1), enable_events=True, key="-Edit Title-"),
         sg.Text("Value"),
         sg.In(size=(10, 1), enable_events=True, key="-Edit Value-"),
         ],
        [sg.Text("Description"),
         sg.In(size=(30, 1), enable_events=True, key="-Edit Description-"),
         sg.Text("Id"),
         sg.In(size=(8, 1), disabled=True, key="-Id-"),

         ],
        [sg.Button('Edit Entry'), sg.Button('Delete Entry'), sg.Button('Copy Entry to'),
         sg.In(size=(8, 1), enable_events=True, key='-Copy to-'), ],
    ]
    bottom_right_column = [
        [sg.Text('Details', key='-Text Details-')],
        [sg.Listbox(values=[], enable_events=True, background_color="LightGray", size=(65, 14), key="-DETAILS-")],
    ]
    info_left_column = [
        [sg.Button('Budget', size=(15, 1), )],
        [sg.Text(text="", size=(28, 6), key="-BUDGET-")],
        [sg.Button('Savings', size=(15, 1), )],
        [sg.Text(text="", size=(28, 6), key="-SAVINGS-")],
    ]
    info_right_column = [
        [sg.Button('Wishes', size=(15, 1), )],
        [sg.Text(text="", size=(28, 6), key="-WISHES-")],
        [sg.Button('Expenses', size=(15, 1), )],
        [sg.Text(text="", size=(28, 6), key="-EXPENSES-")],
    ]
    layout = [
        [
            sg.Column(top_left_column, background_color="LightGray", size=(500, 280), vertical_alignment='center',
                      justification='center', k='-C-'),
            sg.Column(info_left_column, background_color="LightGray", size=(245, 280), vertical_alignment='top',
                      justification='center', k='-C-'),
            sg.Column(info_right_column, background_color="LightGray", size=(245, 280), vertical_alignment='top',
                      justification='center', k='-C-'),
        ],
        [
            sg.Column(bottom_left_column, background_color="LightGray", size=(500, 280), vertical_alignment='top',
                      justification='center', k='-C-'),
            sg.Column(bottom_right_column, background_color="LightGray", size=(500, 280), vertical_alignment='top',
                      justification='center', k='-C-'),
        ],
        [sg.Button('Save', size=(15, 1), ), sg.Button('Cancel', size=(15, 1), )],
    ]
    return layout


if __name__ == '__main__':
    budgets_dict = application_load()
    run_gui(budgets_dict)
