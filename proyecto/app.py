from flask import Flask, render_template, request, redirect, url_for, session
from classes.user_manager import UserManager
from classes.account_manager import AccountManager
from classes.transaction_manager import TransactionManager
from classes.currency_manager import CurrencyManager
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            user = UserManager.verify_credentials(username, password)
            if user:
                session['user_id'] = user.UserId
                return redirect(url_for('dashboard'))
            return render_template('login.html', error='Credenciales incorrectas. Inténtelo de nuevo.')
        except Exception as e:
            print(e)
            return render_template('login.html', error='Error de conexión. Inténtelo de nuevo más tarde.')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        try:
            account = AccountManager.get_account_balances(session['user_id'])
            if account:
                return render_template('dashboard.html', 
                                     saldo_usd=account.BalanceUSD,
                                     saldo_eur=account.BalanceEUR,
                                     saldo_pen=account.BalancePEN)
            return render_template('dashboard.html', 
                                 error='No se encontró información de cuenta para este usuario.')
        except Exception as e:
            print(e)
            return render_template('dashboard.html', 
                                 error='Error al recuperar información de la cuenta.')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/cotizar', methods=['GET', 'POST'])
def cotizar():
    if request.method == 'POST':
        try:
            monto = float(request.form['monto'])
            divisa_origen = request.form['divisa_origen']
            divisa_destino = request.form['divisa_destino']
            
            tasa_conversion, monto_convertido = CurrencyManager.convert_currency(
                monto, divisa_origen, divisa_destino)
            
            if tasa_conversion and monto_convertido:
                return render_template('cotizar_resultado.html',
                                     monto=monto,
                                     divisa_origen=divisa_origen,
                                     divisa_destino=divisa_destino,
                                     monto_convertido=monto_convertido)
            return render_template('cotizar.html',
                                 error='Las divisas seleccionadas no tienen una tasa de conversión definida.')
        except Exception as e:
            print(e)
            return render_template('cotizar.html',
                                 error='Error al realizar la cotización.')
    
    return render_template('cotizar.html')

@app.route('/conversion', methods=['GET', 'POST'])
def conversion():
    if request.method == 'POST':
        try:
            monto = Decimal(request.form['monto'])
            divisa_origen = request.form['divisa_origen']
            divisa_destino = request.form['divisa_destino']
            
            tasa_conversion, monto_convertido = CurrencyManager.convert_currency(
                monto, divisa_origen, divisa_destino)
            
            if not (tasa_conversion and monto_convertido):
                return render_template('conversion.html',
                                     error='Las divisas seleccionadas no tienen una tasa de conversión definida.')
            
            # Actualizar saldos
            if AccountManager.update_balances(
                session['user_id'], divisa_origen, divisa_destino, monto, monto_convertido):
                
                # Registrar transacción
                TransactionManager.register_transaction(
                    session['user_id'], divisa_origen, divisa_destino,
                    monto, tasa_conversion, monto_convertido)
                
                return render_template('conversion_resultado.html',
                                     monto=monto,
                                     divisa_origen=divisa_origen,
                                     divisa_destino=divisa_destino,
                                     monto_convertido=monto_convertido)
            
            return render_template('conversion.html',
                                 error='Saldo insuficiente para realizar la conversión.')
            
        except Exception as e:
            print(f"Error inesperado: {e}")
            return render_template('conversion.html',
                                 error='Error al realizar la conversión.')
    
    return render_template('conversion.html')

@app.route('/historial')
def historial():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    try:
        transactions = TransactionManager.get_user_transactions(session['user_id'])
        return render_template('historial.html', transactions=transactions)
    except Exception as e:
        print(f"Error inesperado: {e}")
        return render_template('historial.html',
                             error='Error al cargar el historial de transacciones.')

if __name__ == '__main__':
    app.run(debug=True)