import math


def statement(invoice, plays):
    def total_volume_credits(data):
        return sum([perf['volume_credits'] for perf in data['performances']])

    def total_amount(data):
        return sum([perf['amount'] for perf in data['performances']])

    def volume_credits_for(a_performance):
        result = 0
        # add volume credits
        result += max(a_performance['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == a_performance["play"]["type"]:
            result += math.floor(a_performance['audience'] / 5)
        return result

    def amount_for(a_performance):
        if a_performance["play"]['type'] == "tragedy":
            result = 40000
            if a_performance['audience'] > 30:
                result += 1000 * (a_performance['audience'] - 30)
        elif a_performance["play"]['type'] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance['audience'] - 20)

            result += 300 * a_performance['audience']

        else:
            raise ValueError(f'unknown type: {a_performance["play"]["type"]}')
        return result

    def play_for(a_performance):
        return plays[a_performance['playID']]

    def enrich_performance(a_performance):
        result = a_performance.copy()
        result['play'] = play_for(result)
        result['amount'] = amount_for(result)
        result['volume_credits'] = volume_credits_for(result)
        return result

    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data['performances'] = list(map(enrich_performance, invoice['performances']))
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)
    return render_plain_text(statement_data, plays)


def render_plain_text(data, plays):
    def usd(amount):
        return f"${amount / 100:0,.2f}"

    result = f'Statement for {data['customer']}\n'
    for perf in data['performances']:
        # print line for this order
        result += f' {perf["play"]["name"]}: {usd(perf['amount'])} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {usd(data['total_amount'])}\n'
    result += f'You earned {data['total_volume_credits']} credits\n'
    return result
