from config import *
from flask import render_template, url_for,request ,redirect, jsonify,flash
import stripe
from dotenv import load_dotenv
load_dotenv()
from os import environ
import json
from functions import Check_inventory ,send_mail, update_inventory,get_order

# %----------------------------------------------%
stripe.api_key = environ.get('STRIPE_SECRET_KEY')
# %----------------------------------------------%
@app.route("/review/<userId>")
def review(userId):
    order=get_order(userId)
    if order:
        if Check_inventory(order):
            stripe_price_id,quantity = Check_inventory(order)
            price=int(stripe.Price.retrieve(stripe_price_id)['unit_amount_decimal'])*0.01
            outofstock = False
            return render_template('review.html',order=order,pricepreitem=price,userId=userId,outofstock=outofstock)
        else:
            outofstock = True
            return render_template('review.html',order=order,outofstock=outofstock,userId=userId)
    else:
        return render_template('base.html')



@app.route("/checkout/<userId>")
def checkout(userId):    
    return render_template('checkout.html',userId=userId)

@app.route('/stripe_pay/<userId>')
def stripe_pay(userId): 
    order=get_order(userId)
    stripe_price_id,quantity = Check_inventory(order)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{ 
            'price': stripe_price_id,
            'quantity': quantity,
        }],
        mode='payment',
        success_url=url_for('thanks',userId=userId, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('review',userId=userId, _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': environ.get('STRIPE_PUBLIC_KEY')
    }
    
@app.route('/thanks/<userId>')
def thanks(userId):
    if request.args.get('session_id'):
        order=get_order(userId)
        update_inventory(order)
        send_mail(order)
        return redirect("thanks")
    return render_template('thanks.html')

if __name__ == '__main__':
    '''run flask on 0.0.0.0, port 5000'''
    app.run(host='0.0.0.0', port=5000, debug=True)
