# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:48:38 2024

@author: User
"""

from Load_data import *



#%% 
def Derivative(Time_series,plot=False):
    X1 = Time_series
    D_X1 = []
    D_X1.append(np.float64(0)) # Set initial value
    for i in range(len(X1)-1):
        dx = X1[i+1]-X1[i]
        D_X1.append(dx)
    if plot:
        plt.hist(D_X1,bins="auto",density="True", alpha=1, label='True distribution')
        plt.xlabel("Price changes")
        plt.title(f'Plot of Delta {Time_series}')
        plt.show()
    
    return D_X1

def Precentage_Del(Time_series,plot=False):
    X1 = Time_series
    D_X1 = []
    D_X1.append(np.float64(0)) # Set initial value
    for i in range(len(X1)-1):
        dx_precentage = (X1[i+1]-X1[i])/X1[i]
        D_X1.append(dx_precentage)
    if plot:
        plt.hist(D_X1,bins="auto",density="True", alpha=1, label='True distribution')
        plt.xlabel("Precentage Price changes")
        plt.title(f'Plot of Delta {Time_series}')
        plt.show()
    
    return D_X1

def Random_Walk(D_Time_series, step):
    # Generate random samples based on the histogram
    num_steps = step  # Define the number of steps in the random walk
    samples = np.random.choice(D_Time_series, size=num_steps, replace=True)
    
    # Perform the random walk
    walk = np.cumsum(samples)
    #check_nan_values(samples)

    # Plot the random walk trajectory
    #plt.plot(walk, label='Random Walk')
    #plt.show()
    return walk

def Precentage_Random_Walk(D_Time_series, step):
    # Generate random samples based on the histogram
    num_steps = step  # Define the number of steps in the random walk
    samples = np.random.choice(D_Time_series, size=num_steps, replace=True)
    
    # Perform the random walk
    walk = samples
    #check_nan_values(samples)

    # Plot the random walk trajectory
    #plt.plot(walk, label='Random Walk')
    #plt.show()
    return walk

def Prediction(Time_series,step,N_walk):
    X1 = Time_series
    #D_X1 = Derivative(Time_series)
    D_X1 = Precentage_Del(Time_series)
    
    Walks = []
    for i in range(N_walk):
        #walk = Random_Walk(D_X1, step)
        walk = Precentage_Random_Walk(D_X1, step)
        Walks.append(walk)
    
    Walks = np.array(Walks)
    average_Walk = np.mean(Walks, axis=0) #Checked axis correct
    
    return Walks,average_Walk
    

def Plot_prediction(Time_series,N_walk,T_start,T_Prediction_sample_start,T_Prediction_End,plot_dis=False):
    """ Time_series = time serise of interest, name in data frame in string"""
    """ N_walk = number of random walk"""
    """ T_start = Starting time for plot, in datatime.date"""
    """ T_Prediction_sample_start = Maxmium histor to construct the distribution, in datatime.date """
    """ T_Prediction_End = predict date """
    
    x_axis_label = Time_label
    X1 = data[Time_series].values
    T = data[x_axis_label].values
    
    # Find the index corresponding to T_start
    date_str = T_start.strftime('%Y-%m-%d')
    start_index = int(np.where(T == date_str)[0])

    # Slicing the arrays from T_start onwards
    T_string = T[start_index:]
    X1_Slicied = X1[start_index:]
    # Convert T to matplotlib dates
    T_date = [mdates.datestr2num(str(date)) for date in T_string]
    plt.plot(T_date, X1_Slicied,label="Histroy")
    plt.xlabel(x_axis_label)
    plt.ylabel(Time_series)
    plt.title(f'Plot of {Time_series}, HK0388')
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(base=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    #Find prediction
        
    #Set date
    T_final = datetime.datetime.strptime(T_string[-1], "%Y-%m-%d").date()
    Prediton_date_list = [T_final + datetime.timedelta(days=x) for x in range((T_Prediction_End - T_final).days + 1)] 
    step = len(Prediton_date_list)
    T_prediction = Prediton_date_list
    
    #Get prediction based on the set date
    if type(T_Prediction_sample_start) == str:
        DX_predictions, DX_prediction_averaged = Prediction(X1,step,N_walk)
    else:
        max_date_str = T_Prediction_sample_start.strftime('%Y-%m-%d')
        max_start_index = np.where(T == max_date_str)[0]
        if len(max_start_index) == 0:
            print("No history on this date, please enter another date")
            return  # Stop the function execution
        max_start_index = int(np.where(T == max_date_str)[0])
        restricted_X1 = X1[max_start_index:]
        DX_predictions, DX_prediction_averaged = Prediction(restricted_X1,step,N_walk)
    
    
    #Get average prediction
    X_prediction_ave =[X1[-1]]
    for i in range(len(DX_prediction_averaged)-1):
        current_price = X_prediction_ave[i]*(1+DX_prediction_averaged[i+1])
        X_prediction_ave.append(current_price)
        
    
    #Get prediction from all walks
    X_predictions =[]
    for J in range(N_walk):
        X_prediction =[X1[-1]]
        DX_prediction = DX_predictions[J]
        for I in range(len(DX_prediction)-1):
            current_price = X_prediction[I]*(1+DX_prediction[I+1])
            X_prediction.append(current_price)
        X_predictions.append(X_prediction)
    #X_prediction = DX_prediction_averaged + X1[-1]
    plt.plot(T_prediction, X_prediction_ave,color='r',label="Averaged prediction")
    transparancy = 3/N_walk
    #for K in range(N_walk):
        #plt.plot(T_prediction, X_predictions[K],alpha=transparancy,color='lime')
    plt.ylim(bottom=0)
    plt.axvline(x=T_Prediction_sample_start, linestyle='--', color='r', alpha=0.5, label='Stat Sample Start')
    plt.axvline(x=T_prediction[0], linestyle='--', color="g", alpha=0.5, label='Stat Sample End')
    
    
    
    final_averaged_price = X_prediction_ave[-1]
    print("Number of walk is", N_walk)
    print("final averaged price is ", final_averaged_price)
    
    X_predictions_array = np.array(X_predictions)
    # Calculate the 68% and 95% confidence intervals along the 154 axis
    ci_68 = np.percentile(X_predictions_array, q=[16, 84], axis=0)  # 68% confidence interval
    ci_95 = np.percentile(X_predictions_array, q=[2.5, 97.5], axis=0)  # 95% confidence interval

    plt.plot(T_prediction, ci_68[0],alpha=0.7,color='aqua',label="68% C.L.")
    plt.plot(T_prediction, ci_68[1],alpha=0.7,color='aqua')
    plt.plot(T_prediction, ci_95[0],alpha=0.7,color='lime',label="95% C.L.")
    plt.plot(T_prediction, ci_95[1],alpha=0.7,color='lime')
    plt.legend()
    plt.show()
    
    if plot_dis:
        
        plt.hist(DX_prediction_averaged,bins="auto",density="True", alpha=1, label='True distribution')
        plt.xlabel("Price changes")
        plt.title(f'Plot of Delta {Time_series}, HK0388')
    
        # Get the current plot limits
        x_min, x_max = plt.xlim()
        y_min, y_max = plt.ylim()

        # Calculate the coordinates for the text
        text_x = x_max - 0.6 * (x_max - x_min)
        text_y = y_max - 0.1 * (y_max - y_min)
        plt.text(text_x, text_y, f"Considered histroy from {max_date_str}")
        plt.show()

    return DX_predictions,X_prediction_ave,X_predictions

Starting_date = datetime.date(2020,8,4)
Ending_date = datetime.date(2024,9,30)
Sample_date=datetime.date(2021,8,4)
#D_date = (Starting_date-Ending_date)

XX,YY,ZZ = Plot_prediction(Time_series='Close',N_walk=1000,T_start=Starting_date,T_Prediction_sample_start=Sample_date,T_Prediction_End=Ending_date,plot_dis=False)
