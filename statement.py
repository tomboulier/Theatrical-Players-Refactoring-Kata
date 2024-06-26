import math


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def usd(amount):
        return f"${amount/100:0,.2f}"

    def play_for(a_performance):
        return plays[a_performance['playID']]

    def amount_for(a_performance):
        if play_for(a_performance)['type'] == "tragedy":
            result = 40000
            if a_performance['audience'] > 30:
                result += 1000 * (a_performance['audience'] - 30)
        elif play_for(a_performance)['type'] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance['audience'] - 20)

            result += 300 * a_performance['audience']

        else:
            raise ValueError(f'unknown type: {play_for(a_performance)["type"]}')
        return result

    def volume_credits_for(a_performance):
        result = 0
        # add volume credits
        result += max(a_performance['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play_for(a_performance)["type"]:
            result += math.floor(a_performance['audience'] / 5)
        return result

    for perf in invoice['performances']:
        # print line for this order
        result += f' {play_for(perf)["name"]}: {usd(amount_for(perf))} ({perf["audience"]} seats)\n'
        total_amount += amount_for(perf)

    for perf in invoice['performances']:
        volume_credits += volume_credits_for(perf)

    result += f'Amount owed is {usd(total_amount)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result
