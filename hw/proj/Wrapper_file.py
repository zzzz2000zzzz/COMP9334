import numpy as np
import math
import time, threading
import sys
from matplotlib import pyplot as plt
import trace_simulation
import random_simulation
#import range

def plot(x_list,y_list):
    # x_list = []
    # y.list = []
    plt.xlabel("number of jobs")
    plt.ylabel("mean response time")
    plt.plot(x_list,y_list)
    plt.show()

def readfile(filename):
    '''''Print a file to the standard output.'''
    f = open(filename,'r')
    result = []
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        result.append(line)
    f.close()
    if len(result) == 1:
        return result[0]
    else:
        return result

def main():
    # mrt_list =[]
    # for n in range(0,30):
    #seed = 1
    seed = 1
    np.random.seed(seed)
    #num_test = [float(l.split()[0]) for l in open('num_tests.txt')]
    num_test = int(readfile('num_tests.txt'))
    for i in range(0,num_test):
        mean_response_time = 0
        num = i + 1
        #mode_file = [float(l.split()[0]) for l in open('mode_'+str(i+1)+'.txt')]
        para_file = [float(l.split()[0]) for l in open('para_'+str(num)+'.txt')]
        arrival_file = [float(l.split()[0]) for l in open('arrival_'+str(num)+'.txt')]
        service_file = [float(l.split()[0]) for l in open('service_'+str(num)+'.txt')]


        mode_file = readfile('mode_'+str(num)+'.txt')
        #
        # para_file = readfile('para_'+str(i+1)+'.txt')
        # arrival_file = readfile('arrival_'+str(i+1)+'.txt')
        # service_file =  readfile('service_'+str(i+1)+'.txt')

        #arrival = readfile('arrival_' + str(i + 1) + '.txt')
        #service = readfile('service_' + str(i + 1) + '.txt')
        #job_num = len(arrival)
        # get the number of servers  m:
        m = int(para_file[0])

        # get the number of setup time:
        setup_time = float(para_file[1])

        # get the number of delayedoff time Tc:
        Tc = float(para_file[2])

        # get the input string type:
        if mode_file == "random":

            # mode is random has time_end and Lambda ， Mu  :
            time_end = float(para_file[3])
            Lambda = arrival_file[0]

            Mu = service_file[0]

            arrival =[]
            departure_time=[]
            result = random_simulation.simulation(m, setup_time, Tc, Lambda, Mu, time_end)

            for i in result:
                if i[1] <= time_end:

                    arrival.append(i[0])
                    departure_time.append(i[1])
            mrt= 0
            x_list = []
            y_list = []
            total = 0
            for i in range(len(arrival)):
                total = total + departure_time[i]-arrival[i]
                mrt= total /(i+1)

                x_list.append(i)
                y_list.append(mrt)

            plot(x_list,y_list)



            #arrival = random_simulation.simulation(m, setup_time, Tc, Lambda, Mu, time_end)[1]
            #print('len1=', len(arrival))
            # for i in range(len(departure_time)):
            #     if departure_time[i] > time_end:
            #         departure_time.remove(departure_time[i])
            #         arrival.remove(arrival[i])
            # index = 0
            # for i in departure_time:
            #     index += 1
            #     if i > time_end:
            #         departure_time.remove(i)
            #         arrival.remove(arrvial[index])
            #print(len(departure_time))


        elif mode_file == "trace":
            arrival_list = arrival_file.copy()
            service_list = service_file.copy()
            arrival = arrival_list.copy()

            time_end = float('inf')
            departure_time = trace_simulation.simulation(m, setup_time, Tc, arrival_list, service_list,time_end)
            #print(arrival_list)
            #print('de=',departure_time)

        for j in range(0,len(arrival)):
            mean_response_time = mean_response_time +float(departure_time[j]) - float(arrival[j])

        mean_response_time = mean_response_time / len(arrival)
        #print(mean_response_time)
        #print(departure_time)
        # if mode_file == "random":
        #     mrt_list.append(mean_response_time)
        # region write file:
        #mean response time file:
        filename = 'mrt_'+str(num)+'.txt'
        with open(filename, 'w') as f:
            f.write('{:.3f}'.format(mean_response_time))
        f.close()

        #departure file:
        filename = 'departure_'+str(num)+'.txt'
        departure_temp1 = []
        for k in range(0, len(arrival)):
            departure_temp1.append((arrival[k],departure_time[k]))
        #print(departure_temp1)
        departure_temp2 = sorted(departure_temp1, key=lambda d: d[1])
        #print(departure_temp2)

        with open(filename, 'w') as f:
            for k in range(0,len(arrival)):

                f.write('{:.3f}'.format(float(departure_temp2[k][0]))+'\t'+'{:.3f}'.format(float(departure_temp2[k][1]))+'\n')
        f.close()
        # endregion
        arrival_list = []
        service_list = []
        arrival = []
        departure_time = []
        departure_temp1 = []
        departure_temp2 = []
# n = 30
# print(mrt_list)
# T_hat = 0
# S_hat = 0
# for i in range(n):
#     T_hat = mrt_list[i] + T_hat
# T_hat = T_hat / n
# for i in range(n):
#     S_hat = (T_hat - mrt_list[i])*(T_hat - mrt_list[i]) + S_hat
# S_hat = math.sqrt(S_hat / (n - 1 ))
#
# t_n_1 = 2.045
# down = T_hat - 2.045 * S_hat / (math.sqrt(n))
# upper = T_hat + 2.045 * S_hat / (math.sqrt(n))
# print([down, upper])

if __name__ == "__main__":
    main()