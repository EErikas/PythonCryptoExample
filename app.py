from flask import Flask, render_template, request
from Crypto_Examples.DES import run_des
from Crypto_Examples.AES import AES

app = Flask(__name__, template_folder='templates', static_folder='static')


# Check if entered value is hex:
def is_hex(string):
    try:
        int(string, 16)
        return True
    except ValueError:
        return False


# Get hex value from entered string
def get_hex(text):
    text_byte_array = list(map(bin, bytearray(text, encoding='utf-8')))
    text_byte_array_string = ''.join([foo[2:] for foo in text_byte_array])
    return str(hex(int(text_byte_array_string, 2))[2:].upper())


def get_hex_array(string):
    return [int(string[i:i + 2], 16) for i in range(0, len(string), 2)]


def fixed_len_hex(string):
    return '{0:#034x}'.format(int(string, 16))[2:]


# Display Home page:
@app.route('/')
def load_home_page():
    return render_template('index.html')


# Display data from DES calculations:
@app.route('/des/', methods=['POST', 'GET'])
def des_page():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']

        # Errors:
        # 1 - empty message or key field
        # 2- key is not hex value

        if message or key is not None:

            if not is_hex(key):
                return render_template('des_page.html', error_no='2')
            else:
                errors = list()
                if not is_hex(message):
                    message = get_hex(message)
                    errors.append('Message was not hex so it was converted to hex value which is: {}'.format(message))
                if len(key) > 16:
                    key = key[:16]
                    errors.append('Key was longer than 16 symbols, it was shortened to: {}'.format(key))
                # Check if there are errors:
                errors = None if len(errors) == 0 else errors
                action = request.form['action_options']
                print(action)
                if action == 'encrypt':
                    encryption_values = run_des(message, key, action)
                    return render_template('des_page.html',
                                           print_action=action,
                                           message=message,
                                           key=key,
                                           encryption_values=encryption_values,
                                           errors=errors)
                elif action == 'decrypt':
                    decryption_values = run_des(message, key, action)
                    return render_template('des_page.html',
                                           print_action=action,
                                           message=message,
                                           key=key,
                                           decryption_values=decryption_values,
                                           errors=errors)
                else:
                    encryption_values = run_des(message, key, 'encrypt')
                    decryption_values = run_des(encryption_values['Cipher'], key, 'decrypt')
                    return render_template('des_page.html',
                                           print_action='both',
                                           message=message,
                                           key=key,
                                           encryption_values=encryption_values,
                                           decryption_values=decryption_values,
                                           errors=errors)
        else:
            return render_template('des_page.html', error_no='1')
    else:
        return render_template('des_page.html')


# Display data from AES calculations:
@app.route('/aes/', methods=['POST', 'GET'])
def aes_page():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']

        # Errors:
        # 1 - empty message or key field
        # 2 - key is not hex value
        # 3 - message is not hex value

        if message or key is not None:

            if not is_hex(key):
                return render_template('aes_page.html', error_no='2')
            elif not is_hex(message):
                return render_template('aes_page.html', error_no='3')
            else:
                message = fixed_len_hex(message)
                key = fixed_len_hex(key)
                aes = AES()
                aes_data = aes.do_rounds(message=get_hex_array(message), key=get_hex_array(key))
                return render_template('aes_page.html', message=message, key=key, data=aes_data)
        else:
            return render_template('aes_page.html', error_no='1')
    else:
        return render_template('aes_page.html')


if __name__ == '__main__':
    app.run()
