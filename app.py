from flask import Flask, request, jsonify
import models

app = Flask(__name__)

models.init_db()

@app.route('/check_serial', methods=['POST'])
def check_serial():
    data = request.json
    serial_number = data.get('serial_number')

    if not serial_number:
        return jsonify({'error': 'Serial number is required'}), 400

    result = models.check_serial(serial_number)

    if result:
        return jsonify({'description': result[0]})
    else:
        return jsonify({'error': 'Serial number not found'}), 404

if __name__ == '__main__':
    #models.reset_db()
    models.import_from_excel('/home/angel/Documents/db_verfication_via_telegram/data.xlsx')
    app.run(host='0.0.0.0', port=5000, debug=True)


