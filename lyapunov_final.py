import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import state_space as ss

def reconstruction(data,tau,m):
    d = len(data)
    d = d - (m-1)*tau
    reconstructed_data = np.zeros((d,m*len(data[0])))
    for i in range(d):
        for j in range(m):
            for k in range(len(data[0])):
                reconstructed_data[i][j*len(data[0])+k] = data[i+j*tau][k]
    return reconstructed_data
        
def kantz_lyapunov(reconstructed_data,epsilon):
    plot_data = []
    for i in range(len(reconstructed_data)):
        print(i)
        epsilon_space=[]
        vector_locations = []
        epsilon_space_next = []
        for j in range(len(reconstructed_data)):
            if i != j:
                dist = np.linalg.norm(reconstructed_data[i]-reconstructed_data[j])
                if dist<epsilon:
                    epsilon_space.append(dist)
                    vector_locations.append(j)
        if i!=len(reconstructed_data)-1:
            for j in vector_locations:
                if(j!=len(reconstructed_data)-1):
                    epsilon_space_next.append(np.linalg.norm(reconstructed_data[i+1]-reconstructed_data[j+1]))
                else:
                    k = vector_locations.index(j)
                    epsilon_space.pop(k)
                    vector_locations.pop(k)

            for j in range(len(epsilon_space)):
                if epsilon_space[j]!=0:
                    epsilon_space[j] = np.log(epsilon_space_next[j]/epsilon_space[j])
            plot_data.append([np.mean(epsilon_space)])
    plot_data = np.array(plot_data)
    plot_data = plot_data[~np.isnan(plot_data)]
    plot_data = plot_data[plot_data>-1e308]
    plot_data = plot_data[plot_data<1e308]
    plot_data = np.reshape(plot_data,(1,-1))[0]
    return plot_data
def rosenstein_lyapunov(reconstructed_data,min_step):
    neighbors = []
    for i in range(len(reconstructed_data)):
        print(i)
        closest_dist = -1
        for j in range(len(reconstructed_data)):
           if(i!=j and abs(j-i)>min_step):
               dist = np.linalg.norm(reconstructed_data[i]-reconstructed_data[j])
               if closest_dist == -1 or dist < closest_dist:
                   closest_dist = dist
        if(closest_dist>0):
            neighbors.append(np.log(closest_dist))
        elif closest_dist == 0:
            neighbors.append(0)
        else:
            print(closest_dist)

    neighbors=np.array(neighbors)
    neighbors=neighbors[~np.isnan(neighbors)]
    neighbors = neighbors[neighbors>-1e308]
    neighbors = neighbors[neighbors<1e308]
    return neighbors
    
    

def plot_growth_factors(lyap_exponents):
    """Plot Lyapunov exponents."""
    plt.figure(figsize=(10, 10))
    plt.plot(lyap_exponents, color='skyblue')
    #plt.bar(range(len(lyap_exponents)), lyap_exponents, color='skyblue')
    plt.xlabel('time')
    plt.ylabel('log of mean value of stretching factor')
    plt.show()
def plot_lyapunov_exponents(frequencies_centralised,exponents_centralised,frequencies_distributed,exponents_distributed):
    plt.figure(figsize=(10, 10))
    plt.plot(frequencies_centralised,exponents_centralised, 'bo',label="centralised")
    plt.legend()
    plt.xlabel('Frequencies')
    plt.ylabel('Largest Lyapunov exponent')
    plt.title("Largest Lyapunov exponent vs Frequencies")
    plt.plot(frequencies_distributed,exponents_distributed, 'ro',label="distributed")
    plt.legend(loc="upper left")
    plt.axhline(0, color='grey')
    plt.show()

def exponent(tau,m,epsilon,min_steps, filename,xval, exponents, xvalues):
    #load data and format
    df = pd.read_csv(filename)
    pdata = df[['px','py','pz']]
    data=pdata.values

    #reconstruction through time delay
    reconstructed_data = reconstruction(data,tau,m)
    print("data has been reconstructed")
    #calculate lyapunov exponents with rosenstein metscphod 
    # exponent = rosenstein_lyapunov(reconstructed_data,min_steps)
    # plot_growth_factors(exponent)
    # print(np.polyfit(exponent,range(len(exponent)),1))
    

    data = kantz_lyapunov(reconstructed_data,epsilon)
    plot_growth_factors(data)
   

    #append exponent of this data set to the list of exponents
    #exponents.append(exponent[0])
    #xvalues.append(xval)
    print(exponent)
def main():
    #parameters
    tau = 3
    m = 3
    epsilon = 0.01
    min_steps = 10
    

    #initialize lists
    exponents_centralised=[]
    frequencies_centralised = []

    exponents_distributed = []
    frequencies_distributed = []

    exponent(tau,m,epsilon,min_steps, "lorentz_data.csv", 140,exponents_centralised,frequencies_centralised)
    
    # #load data and format for centralsed control
    #print("Centralised")
    #exponent(tau,m,epsilon,min_steps, "clean_data/centralised/140Hz.csv", 140,exponents_centralised,frequencies_centralised)
    #print("140Hz")
    # exponent(tau,m,epsilon,min_steps ,"clean_data/centralised/220Hz.csv", 220,exponents_centralised,frequencies_centralised)
    # print("220Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/centralised/350Hz.csv", 350,exponents_centralised,frequencies_centralised)
    # print("350Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/centralised/370Hz.csv", 370,exponents_centralised,frequencies_centralised)
    # print("370Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/centralised/400Hz.csv", 400,exponents_centralised,frequencies_centralised)
    # print("400Hz")
    
    # #load data and format for distributed control
    # print("Distributed")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/140Hz.csv", 140,exponents_distributed,frequencies_distributed)
    # print("140Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/220Hz.csv", 220,exponents_distributed,frequencies_distributed)
    # print("220Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/350Hz.csv", 350,exponents_distributed,frequencies_distributed)
    # print("350Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/370Hz.csv", 370,exponents_distributed,frequencies_distributed)
    # print("370Hz")
    # exponent(tau,m,epsilon,min_steps ,"clean_data/distributed/400Hz.csv", 400,exponents_distributed,frequencies_distributed)
    # print("400Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/500Hz.csv", 500,exponents_distributed,frequencies_distributed)
    # print("500Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/600Hz.csv", 600,exponents_distributed,frequencies_distributed)
    # print("600Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/800Hz.csv", 800,exponents_distributed,frequencies_distributed)
    # print("800Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/1000Hz.csv", 1000,exponents_distributed,frequencies_distributed)
    # print("1000Hz")
    # exponent(tau,m,epsilon,min_steps ,"clean_data/distributed/1120Hz.csv", 1120,exponents_distributed,frequencies_distributed)
    # print("1120Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/1200Hz.csv", 1200,exponents_distributed,frequencies_distributed)
    # print("1200Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/1440Hz.csv", 1440,exponents_distributed,frequencies_distributed)
    # print("1440Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/1800Hz.csv", 1800,exponents_distributed,frequencies_distributed)
    # print("1800Hz")
    # exponent(tau,m,epsilon,min_steps, "clean_data/distributed/2000Hz.csv", 2000,exponents_distributed,frequencies_distributed)
    # print("2000Hz")

    #plot_lyapunov_exponents(frequencies_centralised,exponents_centralised,frequencies_distributed,exponents_distributed)
if __name__ == "__main__":
    main()  