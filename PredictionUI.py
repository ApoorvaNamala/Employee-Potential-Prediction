import pickle
import streamlit as st
from PIL import Image
# loading the trained model
pickle_in = open('C:/Users/User/Desktop/classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)
st.set_page_config(layout="wide")
@st.cache()

# defining the function which will make the prediction using the data which the user inputs 
def predict_potential(satisfaction, evaluation, ProjectCount, averageMonthlyHours, yearsAtCompany, workAccident, promotion, Department):   
 
    # Pre-processing user input    
    switcher = {
        'accounting': 2,
        'hr': 3,
        'IT': 0,
        'management': 4,
        'marketing': 5,
        'product_mng':6,
        'RandD': 1,
        'sales': 1,
        'support': 8,
        'technical': 9,
        
    }
    Department =  switcher.get(Department)
    satisfaction = satisfaction / 100
    evaluation = evaluation / 100
 
    # Making predictions 
    prediction = classifier.predict( 
        [[satisfaction, evaluation, ProjectCount, averageMonthlyHours, yearsAtCompany, workAccident, promotion, Department]])
     
    if prediction == 0:
        pred = 'High potential'
    else:
        pred = 'Not upto mark, replace or train employee for better contribution'
    return pred 
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:#98fb98;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Employee Potential Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
    



    # Import the required module for text
    # to speech conversion
    # This module is imported so that we can
    # play the converted audio
    menu= ["Home","Predict Employee Potential","Rules", "Help"]
    choice= st.sidebar.selectbox("Menu",menu)
    if choice=='Home':
        st.subheader("'You don't build a business. You build people, and people build the business.' - Zig Ziglar")
        image = Image.open('C:/Users/User/Desktop/hr.jpg')
        st.image(image, caption='')
        
    elif choice == 'Predict Employee Potential':

        # following lines create boxes in which user can enter data required to make prediction 
        Satisfaction = st.number_input("Employee Satisfaction") 
        EvaluationScore = st.number_input("Latest Evaluation Score") 
        ProjectCount = st.number_input("No. of projects employee worked on") 
        averageMonthlyHours = st.number_input("Employee monthly work hours")  
        yearsAtCompany = st.number_input("Total years worked for company")
        workAccident = st.number_input("work accidents committed by employee") 
        promotion = st.number_input("No.of times employee got promoted")
        Department = st.selectbox('Department',("IT","RandD","accounting","hr","management","marketing","product_mng","sales","support","technical"))
        result =""
        # when 'Predict' is clicked, make the prediction and store it 
        if st.button("Predict"): 
            result = predict_potential(Satisfaction, EvaluationScore, ProjectCount, averageMonthlyHours, yearsAtCompany, workAccident, promotion, Department) 
            st.success('{}'.format(result))
    elif choice == 'Rules':
        st.subheader("Rules and Observations of trends in the data")
        st.text("1.Employees generally produce low outcome when they are underworked (less than 150hr/month or 6hr/day)\n"
                +"2.Employees generally produce high outcome when they are overworked (more than 250hr/month or 10hr/day)\n"
                +"3.Employees with either really high or medium evaluations should be taken into consideration for high turnover rate\n"
                +"4.Employees with low to medium salaries are the bulk of employee turnover\n"
                +"5.Employees that had medium project count was at risk of loe potential\n"
                +"6.Employee satisfaction is the highest indicator for employee turnover.\n"
                +"7.Employee that had 4 and 5 yearsAtCompany should be taken into consideration for high turnover rate\n"
                +"8.Employee satisfaction, yearsAtCompany, and evaluation were the three biggest factors in determining turnover.\n")
    elif choice == 'Help':
        st.text("Contact us in case of any queries.")
     
if __name__=='__main__': 
    main()