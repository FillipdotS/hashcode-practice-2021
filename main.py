import operator
from datetime import time, datetime


class Delivery:
    def __init__(self, amount, pizzas):
        self.amount = amount
        self.pizzas = pizzas


class Pizza:
    def __init__(self, pk, amount, ingredients):
        self.pk = pk
        self.amount = amount
        self.ingredients = ingredients
        self.uniqueness_factor = 0

    def __str__(self):
        return "PK: " + str(self.pk)


def calculate_unique_ingredients(pizzas):
    """Return the number of unique ingredients between all pizzas in the given list"""
    unique_ingredients = set()
    for p in pizzas:
        for ing in p.ingredients:
            if ing not in unique_ingredients:
                unique_ingredients.add(ing)

    return len(unique_ingredients)


def solve(input_name):
    start_time = datetime.now()
    print("### Starting " + input_name + " ###")

    input_file = open("data/" + input_name + ".in", "r")

    basic_info = input_file.readline().split()

    total_pizzas = int(basic_info[0])
    team_amounts = list(map(int, basic_info[1:]))
    remaining_pizzas = []
    ingredient_uniqueness = {}

    magic_factor = 1.1

    for i in range(0, total_pizzas):
        pizza_info = input_file.readline().split()
        new_pizza = Pizza(i, int(pizza_info[0]), pizza_info[1:])
        remaining_pizzas.append(new_pizza)

        # Collect data about ingredients (lower is better)
        for ing in new_pizza.ingredients:
            try:
                ingredient_uniqueness[ing] += 1
            except KeyError:
                ingredient_uniqueness[ing] = 1

    # uniqueness_factor is defined as =
    #   ((total ingredient uniqueness) / total ingredients) - (total ingredients * magic_factor)
    #
    # The lower the uniqueness_factor, the better

    for pizza in remaining_pizzas:
        total_ingredient_uniqueness = 0
        for ing in pizza.ingredients:
            total_ingredient_uniqueness += ingredient_uniqueness[ing]

        pizza.uniqueness_factor = (total_ingredient_uniqueness / pizza.amount) - (pizza.amount * magic_factor)

    # Sorted from best (lowest factor) to worst (highest factor)
    remaining_pizzas.sort(key=operator.attrgetter("uniqueness_factor"))

    deliveries = []

    print("Beginning deliveries...")
    while True:
        # Algorithm:
        # Take next two pizzas (three if we have no two people groups and so on), get their unique ingredient count,
        # if it falls within a certain threshold (i.e. these two pizzas have 90% of all ingredients available), then
        # we deliver those two, however if it lacks ingredients, we'll add another pizza, and recalculate.
        #
        # Hindsight: This gives the exact same score as just making as many 4-group deliveries as possible, then
        # 3-group and finally 2-group deliveries.

        if team_amounts[0] > 0 and len(remaining_pizzas) >= 2:
            next_pizzas = remaining_pizzas[:2]
            remaining_pizzas = remaining_pizzas[2:]
        elif team_amounts[1] > 0 and len(remaining_pizzas) >= 3:
            next_pizzas = remaining_pizzas[:3]
            remaining_pizzas = remaining_pizzas[3:]
        elif team_amounts[2] > 0 and len(remaining_pizzas) >= 4:
            next_pizzas = remaining_pizzas[:4]
            remaining_pizzas = remaining_pizzas[4:]
        else:
            break

        while len(next_pizzas) < 4 and len(remaining_pizzas) > 0:
            next_pizzas_coverage = calculate_unique_ingredients(next_pizzas) * len(ingredient_uniqueness) * 100
            if next_pizzas_coverage > 80.0:
                break
            else:
                next_pizzas = remaining_pizzas[:1]
                remaining_pizzas = remaining_pizzas[1:]

        # Hack: Index 0 is amount of two person teams, so if delivering X pizzas, take away from team at index 2 - X
        team_amounts[len(next_pizzas) - 2] -= 1

        new_delivery = Delivery(len(next_pizzas), next_pizzas)
        deliveries.append(new_delivery)

    # Output
    output_file = open("output/" + input_name + "_out_" + ".txt", "w")

    output_file.write(str(len(deliveries)))

    pizzas_delivered = 0

    for d in deliveries:
        result = "\n" + str(d.amount) + " "
        for p in d.pizzas:
            pizzas_delivered += 1
            result += str(p.pk) + " "

        output_file.write(result)

    stats = "Completed " + input_name + " in " + str(datetime.now() - start_time) + "\n"
    stats += "Stats: \nTotal deliveries " + str(len(deliveries)) + "\n"
    stats += str(pizzas_delivered) + " out of " + str(total_pizzas) + " pizzas used ("
    stats += str(pizzas_delivered / total_pizzas * 100) + "%).\n"
    stats += "Teams: Two - " + str(team_amounts[0]) + " Three - " + str(team_amounts[1]) + " Four - " + str(team_amounts[2]) + "\n"
    stats += str(len(ingredient_uniqueness)) + " unique ingredients in this set"

    print(stats)


solve("a_example")
solve("b_little_bit_of_everything")
solve("c_many_ingredients")
solve("d_many_pizzas")
solve("e_many_teams")
