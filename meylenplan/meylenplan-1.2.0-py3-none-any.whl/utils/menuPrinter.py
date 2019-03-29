import datetime

from tabulate import tabulate

def print_menu(menu, date, args):
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
        row = [meal.name]
        if args.allergens:
            row.append(meal.allergens)
        if not args.no_internal:
            row.append('{:.2f}€'.format(meal.price.intern))
        if not args.no_external:
            row.append('{:.2f}€'.format(meal.price.extern))
        table.append(row)

    headers = ['Tageskarte für ' + str(date)]
    if args.allergens:
        headers.append('Allergene')
    if not args.no_internal:
        headers.append('Preis Intern')
    if not args.no_external:
        headers.append('Preis Extern')
    print(tabulate(table, headers=headers, tablefmt='orgtbl'))
    if args.allergens:
        print(menu.allergens_legend)

