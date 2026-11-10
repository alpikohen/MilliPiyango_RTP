def calculate_tax(prize_amount):
    tax_free_limit = 66935
    tax_rate = 0.20
    if prize_amount <= tax_free_limit:
        return 0
    taxable_amount = prize_amount - tax_free_limit
    return round(taxable_amount * tax_rate, 2)
