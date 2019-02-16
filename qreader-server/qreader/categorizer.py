QUEUE_MORNING = 'QUEUE_MORNING'
QUEUE_REST = 'QUEUE_REST'
WEEKDAY_MORNING = 'WEEKDAY_MORNING'
WEEKDAY_REST = 'WEEKDAY_REST'
WEEKEND_MORNING = 'WEEKEND_MORNING'
WEEKEND_REST = 'WEEKEND_REST'
COMMUTE_MORNING = 'COMMUTE_MORNING'
COMMUTE_EVENING = 'COMMUTE_EVENING'
WALK_DRIVING_MORNING = 'WALK_DRIVING_MORNING'
WALK_DRIVING_REST = 'WALK_DRIVING_REST'
COFFEE_SHOP = 'COFFEE_SHOP'
TRAVELLING = 'TRAVELLING'
LATE_NIGHT = 'LATE_NIGHT'

category_table = {
    'short_positive_easy': [QUEUE_MORNING, COMMUTE_MORNING],
    'short_positive_average': [WEEKDAY_MORNING, COMMUTE_MORNING],
    'short_positive_difficult': [WEEKDAY_MORNING],
    'short_neutral_easy': [QUEUE_REST, QUEUE_MORNING, COMMUTE_EVENING],
    'short_neutral_average': [WEEKDAY_MORNING, COMMUTE_EVENING],
    'short_neutral_difficult': [WEEKDAY_MORNING],
    'short_negative_easy': [WEEKDAY_REST, QUEUE_REST],
    'short_negative_average': [TRAVELLING, WEEKDAY_REST],
    'short_negative_difficult': [WEEKDAY_REST],

    'medium_positive_easy': [COMMUTE_MORNING, WEEKEND_MORNING, WALK_DRIVING_MORNING],
    'medium_positive_average': [COMMUTE_MORNING, WEEKEND_MORNING],
    'medium_positive_difficult': [COFFEE_SHOP, WEEKEND_MORNING],
    'medium_neutral_easy': [COMMUTE_EVENING, WALK_DRIVING_MORNING, WALK_DRIVING_REST],
    'medium_neutral_average': [COMMUTE_EVENING, TRAVELLING],
    'medium_neutral_difficult': [COFFEE_SHOP],
    'medium_negative_easy': [WALK_DRIVING_REST, WEEKEND_REST, WEEKDAY_REST],
    'medium_negative_average': [TRAVELLING, WEEKEND_REST, WEEKDAY_REST],
    'medium_negative_difficult': [WEEKEND_REST, WEEKDAY_REST],

    'long_positive_easy': [WEEKEND_MORNING, WALK_DRIVING_MORNING],
    'long_positive_average': [WEEKEND_MORNING, LATE_NIGHT, TRAVELLING],
    'long_positive_difficult': [LATE_NIGHT, WEEKEND_MORNING, COFFEE_SHOP],
    'long_neutral_easy': [WALK_DRIVING_MORNING, WALK_DRIVING_REST],
    'long_neutral_average': [TRAVELLING, LATE_NIGHT],
    'long_neutral_difficult': [LATE_NIGHT, COFFEE_SHOP],
    'long_negative_easy': [WALK_DRIVING_REST, WEEKEND_REST],
    'long_negative_average': [TRAVELLING, WEEKEND_REST],
    'long_negative_difficult': [WEEKEND_REST],
}


def categories(m, r, t):
    length = t / 60
    if length < 10:
        length = 'short'
    elif 10 <= length <= 30:
        length = 'medium'
    else:
        length = 'long'
        pass

    key = '%s_%s_%s' % (length, m, r)

    return category_table[key] if key in category_table else []
