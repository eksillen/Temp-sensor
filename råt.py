from flask import Flask, request, render_template
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk



y1= np.array([-70021,-132364,-94906,-126077,-31092.46,68500,-42487,-23173,-17243.14,-12949.14,-7380,-5632.09,-1374,-1100.34,-810.311,-680.03,-378.2,-238.7,-500,-84,-80])
x1= np.array([1270021,1260599,874506.6975,793577,656514,574087.51,489292,419073.5,360243,310749.41,233580,203432.09,99574.5,88100.34,78110.31,69388.03845,55078.20641,44038.7,34002,27285,22280])
y2 =np.array([-160.42357,-152.42108,-99.58618,-76.395,-23.5473,])
x2 =np.array([342.42357,342.42108,343.58618,342.395049743,345.5473275])

#Data-set för att approximera höga värden eller låga värden på utspänningen,.


error1 = np.polyfit(x1,y1,2)
error2 = np.polyfit(x2,y2,2)





p1 = np.poly1d(error1)
p2 = np.poly1d(error2)

#Gör om dessa set data med hjälp av polynom approximation.


def Res_from_voltage(x):
        
        Circuit_function = (4100*x/4793 + 396/4793)/(12/1400 - ((4100*x/4793 + 396/4793)*(1/1400 + 1/500)))
        if x > 3.522213:

#Värden har valts efter provomgångar, dvs för extrema värden där circuit_function inte fungerar
            
            return Circuit_function + p1(Circuit_function)
        elif x< 1.6902:                
            return Circuit_function + p2(Circuit_function)

#Värden har valts efter provomgångar, dvs för extrema värden där circuit_function inte fungerar
        else:
            return Circuit_function
        

#print("R = "+str(Res_from_voltage(3)))




def Stienhart_equation(R):
        
        A = np.array([[1,np.log(10000),(np.log(10000))**3],[1,np.log(1200),(np.log(1200))**3],[1,np.log(190),(np.log(190))**3]]) 
        B = np.array([[1/(25+273.15)],[1/(81+273.15)],[1/(153+273.15)]])
        C = np.linalg.solve(A,B)
        T = 1/(9.41587553e-04 + 2.70580244e-04*np.log(R)-1.02016606e-07*(np.log(R))**3)    
        return round(T -273.15,2)


ngrok config add-authtoken 2Ksid4LPzpnX7DB4oFZB1ojMKKX_3N75mnaeNnt8wtBfcj7g5


from flask import Flask, request, render_template,jsonify
app = Flask(__name__)
def do_something(Vout):
    Vout = Vout
    if float(Vout) >= 1.685 and float(Vout) <= 3.594:      
        combine = str(round(Res_from_voltage(float(Vout))))
        combine2 = str(Stienhart_equation(Res_from_voltage(float(Vout))))
        return combine+ str("    ")+str("R"), str("     ")+combine2 +str("    ")+str("C")
    else:
        return str("Fel")

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    Vout = request.form['Vout']
    word = request.args.get('Vout')
    combine = do_something(Vout)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
if __name__ == '__main__':
    app.run(debug=False, host='192.168.1.85', port=5000)