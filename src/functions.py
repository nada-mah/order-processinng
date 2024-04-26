from config import db

def get_order(id):
    from bson.objectid import ObjectId
    try:
        order = list(db.orders.find({'userid':ObjectId(id)}))
    except Exception as e:
        print(e)
    if order:
        return order[0]
    else:
        return False
        
def Check_inventory(order):
    productbyid = list(db.Products.find({'_id':order['product_id']}))
    if int(productbyid[0]['quantity']) >= int(order['quantity']):
        stripe_price_id =productbyid[0]['price']
        return stripe_price_id,int(order['quantity'])
    else:
        return False

def update_inventory(order):
    productbyid = list(db.Products.find({'_id':order['product_id']}))
    response = db.Products.update_one(
        {'_id':order['product_id']},
        { "$set": { 'quantity' : int(productbyid[0]['quantity'])-int(order['quantity']) } }
    )
    complete = db.orders.update_one(
        {'userid':order['userid']},
        { "$set": { 'status' :'paid' } }
    )
    print(complete)

def send_mail(order):
    import smtplib 
    from dotenv import load_dotenv
    load_dotenv()
    from os import environ
    from email.message import EmailMessage

    email_sender = 'burrnermail556@gmail.com'
    email_password = environ.get('EMAIL_PASSWORD')
    # Creating the object
    MSG = EmailMessage() 

    # Your Email
    MSG['From'] = email_sender

    # Email you want to send it to
    MSG['To']   = 'lomah38627@togito.com'

    # Email Subject
    MSG['Subject'] = "Order Confirmation!!" 
    
    body = f''' Payment sucsessful for orderID/maybe
            for {order['proudectname']} x {order['quantity']}
                OrderID: {order['_id']}
            '''
    
    # Email Subject
    MSG.set_content(body)

    # Connecting to Gmail
    S = smtplib.SMTP('smtp.gmail.com', 587) 
    S.ehlo()
    S.starttls() 

    # Here goes your Email & Password
    S.login(email_sender, email_password)

    #Shooting out the Email
    TEXT = MSG.as_string() 
    S.sendmail(email_sender, 'lomah38627@togito.com', TEXT) 
    S.quit() 
    
