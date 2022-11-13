from datetime import datetime

def translate_month(month):
    return (month.replace("January","janeiro").replace("February","fevereiro").replace("March","março").
        replace("April", "abril").replace("May", "maio").replace("June", "junho").replace("July", "julho").
        replace("August", "agosto").replace("September", "setembro").replace("October", "outubro").
        replace("November", "novembro").replace("December", "dezembro"))
