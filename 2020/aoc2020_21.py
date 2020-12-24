
import aoctools
import re

# MO[1] -> a string containing all allergens separated by ', '
ALLERGENS_RE = re.compile(r' \(contains (.+(, )?)+\)')


def parse_foods(raw):
    """
    Parse the raw puzzle input into a dict, keyed by the string of each
    row, whose value is another dict with keys 'ingredients' and
    'allergens' (whose values are sets of strings).
    """
    def parse_food(food):
        mo = ALLERGENS_RE.search(food)
        allergens = mo[1].split(', ')
        ingredients = food[:mo.start()].split(' ')

        return ingredients, allergens

    foods_raw = raw.split('\n')
    foods = {}
    for food in foods_raw:
        f_ingredients, f_allergens = parse_food(food)
        foods[food] = {'ingredients': f_ingredients, 'allergens': f_allergens}

    return foods


def deduce_allergens(foods: dict):
    """
    Deduce which ingredients contain which allergen (if any).
    :param foods: A nested dict of foods, as returned by
    `parse_all_foods()`.
    :return: A dict, keyed by ingredient, with values of which allergen
    each contains (which may be None).
    """
    allergens_rough = {}
    ingredients = {}
    for food in foods.values():
        f_ingredients, f_allergens = food['ingredients'], food['allergens']
        for ing in f_ingredients:
            # For all ingredients, initially specify that each has no allergens.
            # (Will specify otherwise after deducing allergens.)
            ingredients.setdefault(ing, None)
        for alrgn in f_allergens:
            allergens_rough.setdefault(alrgn, set(f_ingredients))
            allergens_rough[alrgn] = allergens_rough[alrgn].intersection(set(f_ingredients))

    # Iteratively filter from allergens_rough into allergens_clean.
    allergens_clean = {}
    while len(allergens_rough) > 0:
        # If an allergen has been cleaned, remove it from rough.
        for al in allergens_clean.keys():
            if al in allergens_rough:
                allergens_rough.pop(al)

        # If a rough allergen has a single item as its definition, it is clean.
        for al, defins in allergens_rough.items():
            if len(defins) == 1:
                allergens_clean[al] = defins.pop()

        # Remove from each rough definition all clean definitions.
        used = set(allergens_clean.values())
        for al, defin in allergens_rough.items():
            allergens_rough[al] = defin - used

    # Now that we know which allergens are caused by which ingredient, specify
    # that for the appropriate ingredients. (The rest will remain `None`.)
    for alrgn, ingred in allergens_clean.items():
        ingredients[ingred] = alrgn

    return ingredients


def part1(raw):
    foods = parse_foods(raw)
    ingredients = deduce_allergens(foods)

    safe_ingredients = [
        ing for ing, alrgn in ingredients.items() if alrgn is None
    ]
    c = 0
    for food in foods.values():
        f_ingredients = food['ingredients']
        for ing in f_ingredients:
            c += 1 if ing in safe_ingredients else 0
    return c


def part2(raw):
    foods = parse_foods(raw)
    ingredients = deduce_allergens(foods)

    unsafe_ingredients = [
        ing for ing, alrgn in ingredients.items() if alrgn is not None
    ]
    unsafe_ingredients.sort(key=lambda x: ingredients[x])
    return ','.join(unsafe_ingredients)


puz_in = aoctools.puzzle_input(2020, 21)
test_data = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''

print(part1(test_data))

aoctools.test(1, part1, test_data, 5)
aoctools.test(2, part2, test_data, 'mxmxvkd,sqjhc,fvjkl')

aoctools.submit(1, part1, puz_in)
aoctools.submit(2, part2, puz_in)
