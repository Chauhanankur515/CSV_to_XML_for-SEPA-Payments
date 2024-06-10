from decimal import Decimal, ROUND_HALF_EVEN

payment_str = 1
payment = Decimal(payment_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)  # Round to two decimal places, even ties
print(f"payment: {payment}")
# controlSum += payment