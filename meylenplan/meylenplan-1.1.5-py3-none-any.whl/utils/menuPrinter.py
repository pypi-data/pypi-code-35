import datetime

from tabulate import tabulate


def print_menu(menu, date):
    output_day = next((day for day in menu.days if day.id == date.weekday()), None)

    if date > menu.valid_to.date:
        # Menu is outdated
        if date.weekday() in range(0,5):
            # and it is already [monday, friday]
            print("Leider wurde für die aktuelle Woche noch keine neue Tageskarte zur Verfügung gestellt.")
            return
        if date.weekday() in range(5,7):
            # but we are still in the same week waiting for an update
            print("Leider wurde für die kommende Woche noch keine neue Tageskarte zur Verfügung gestellt.")
            return

    if date < menu.valid_from.date:
        # There is already a new menu for the upcoming week.
        # Change output day to monday
        output_day = next((day for day in menu.days if day.id == 0), None)

    if output_day is None:
        print("Heute ist nicht.")
        return

    table = []
    for meal in output_day.meals:
        table.append([meal.name, '{:.2f}€'.format(meal.price.intern), '{:.2f}€'.format(meal.price.extern)])
    print(tabulate(table, headers=['Essen', 'Preis Intern', 'Preis Extern'], tablefmt='orgtbl'))
