def averageWaitingTime(customers):

    time_available_at = 0
    total_wait = 0
    for item in customers:
        time_available_at = max(time_available_at,item[0]) + item[1]
        total_wait += time_available_at - item[0]

    return total_wait/len(customers)

customers = [[1,2],[2,5],[4,3]]
print(averageWaitingTime(customers))