import numpy as np
import math
import time, threading
import sys

def random_mode(number,parameter):

    a = np.random.rand(number)
    b = []
    for u in a:
        x = -math.log(1 - u) / float(parameter)  # lambda = 2; x = -log(1-u)/lambda;
        b.append(x)
    if len(b) == 1:
        return b[0]
    else:
        return b[0] + b[1] + b[2]

def consistency_check():

    count_setup = 0
    count_marked = 0
    for i in server_status:
        if float(i) == 1:
            count_setup += 1
    for i in queue:
        if float(i) == 1:  # 'MARKED'
            count_marked += 1
    if count_marked != count_setup:
        print("error consistency check!")

# def generate_arrival(arrival_time, Lambda, Mu):
#     arrival_time = arrival_time + random_mode(1, Lambda)
#     arrival_list.append(arrival_time)
#     service_list.append(random_mode(3, Mu))
#     arrival.append(arrival_time)
#     return arrival_time, arrival_list, service_list, arrival


def simulation(m, setup_time, Tc, Lambda, Mu ,time_end):
    master_clock = 0
    # OFF: 0  SETUP:1  Busy :2  Delayed:3

    server_status = [0] * m
    queue = []
    extra_queue=[] #(arrival time, service time)
    count_job=0

    setup_list=[]

    departure_list=[]

    delayoff_list=[]

    departure_time = []

    result = []

    arrival = []
    arrival_list = []
    service_list = []
    arrival_time = 0
    service_time = random_mode(3, Mu)
    arrival_time = arrival_time + random_mode(1, Lambda)
    arrival_list.append(arrival_time)
    service_list.append(service_time)
    #arrival.append(arrival_time)


    #print(arrival_list)
    #print(min(arrival_list))
    while (master_clock < time_end):
        if arrival_list:
            a=min(arrival_list)
        else:
            a=float('inf')
        if setup_list:
            b=min(setup_list)
        else:
            b=float('inf')
        if departure_list:
            c=min(departure_list)
        else:
            c=float('inf')
        if delayoff_list:
            d=min(delayoff_list)
        else:
            d=float('inf')

        clock =  min (a,b,c,d)
        #print('clock,a,b,c,d', clock,a,b,c,d)
        # clock = min(min(arrival_list),min(setup_list),min(departure_list),min(delayoff_list))
        # print(clock)

        if clock == float('inf'):
            #temp_tuple = (departure_time, arrival)
            return result

        for i in arrival_list:
            if float(i) == clock:
                master_clock = arrival_list.pop(0)
                next_event_type = 'arrival'
        for i in setup_list:
            if float(i) == clock:
                master_clock = setup_list.pop(0)
                next_event_type = 'setup'
        for i in departure_list:
            if float(i) == clock:
                master_clock = departure_list.pop(0)
                #print('output=',master_clock)
                departure_time.append(master_clock)

                next_event_type = 'departure'
        for i in delayoff_list:
            if float(i) == clock:
                master_clock = delayoff_list.pop(0)
                next_event_type = 'delay'

        if next_event_type == 'arrival':

            if 3 in server_status:#find delay server
                delayoff_list.remove(max(delayoff_list))
                server_status.remove(3)
                server_status.append(2)#one status from delay to busy

                time = master_clock +  service_list[0]
                service_list.pop(0)
                departure_list.append(time)

                result.append((master_clock,time))
                # print('server_status=', server_status)
                # print('queue=', queue)

            else:
                if 0 in server_status: #find off server
                    server_status.remove(0)
                    server_status.append(1)  # one status from off to setup
                    time = master_clock + float(setup_time)
                    setup_list.append(time)
                    queue.append(1) #job 'MARKED'

                    extra_queue.append((master_clock,service_list.pop(0)))
                    #print(extra_queue)
                    count_job += 1
                    # print('server_status=', server_status)
                    #print('queue=', queue)

                else:#only setup or busy server
                    queue.append(0)#'UNMARKED'
                    extra_queue.append((master_clock,service_list.pop(0)))
                    # extra_queue[count_job][0] = master_clock
                    # extra_queue[count_job][1] = float(service_list.pop(0))
                    count_job+=1
                    # print('server_status=', server_status)
                    # print('queue=', queue)
            #print('1queue=', queue)
            service_time = random_mode(3, Mu)
            arrival_time = arrival_time + random_mode(1, Lambda)
            if (arrival_time + service_time) <= time_end:
                arrival_list.append(arrival_time)
                service_list.append(service_time)



        elif next_event_type == 'setup':

            if len(queue)!=0:
                server_status.remove(1)
                server_status.append(2)
                sign = 0
                queue.pop(0)

                time = master_clock + float(extra_queue[0][1])
                result.append((extra_queue[0][0],time))
                extra_queue.pop(0)
                departure_list.append(time)



                #arrival.append(master_clock)
                # print('server_status=', server_status)
                # print('queue=', queue)

            else:
                server_status.remove(1)
                server_status.append(3)
                time = master_clock + float(Tc)
                delayoff_list.append(time)
                # print('server_status=', server_status)
                # print('queue=', queue)
            #print('2queue=', queue)

        elif next_event_type == 'departure':

            if len(queue) != 0:
                # server_status.remove(1)
                # server_status.append(2)
                sign = 0
                queue.pop(0)
                time = master_clock + float(extra_queue[0][1])
                result.append((extra_queue[0][0],time))
                extra_queue.pop(0)
                departure_list.append(time)
                #arrival.append(master_clock)
                #print('extra_queue=',extra_queue)

                temp_count_setup = 0
                temp_count_marked = 0
                for i in server_status:
                    if 1 in server_status:
                        temp_count_setup += 1

                for i in range(len(queue)):
                    if queue[i] == 1:  # MARKED
                        temp_count_marked += 1
                    elif queue[i] == 0:
                        sign = 1  # find unmarked job
                if temp_count_marked != temp_count_setup:
                    if sign == 1:
                        queue.remove(0)
                        queue.append(1)

                    else:
                        if len(setup_list)!=0:
                            setup_list.remove(max(setup_list))
                            server_status.remove(1)
                            server_status.append(0)
                # print('server_status=', server_status)
                # print('queue=', queue)

            else:
                server_status.remove(2)
                server_status.append(3)
                time = master_clock + float(Tc)
                delayoff_list.append(time)
                # print('server_status=', server_status)
                # print('queue=', queue)
            #print('3queue=', queue)


        elif next_event_type == 'delay':
            #print('4queue=', queue)
            server_status.remove(3)
            server_status.append(0)
            # print('server_status=',server_status)
            # print('queue=', queue)
        #print('extra_queue=', extra_queue)

    #temp_tuple = (departure_time,arrival)
    #print(result)
    return result

